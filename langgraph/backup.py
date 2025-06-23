import os, uuid
from typing import Annotated
from typing_extensions import TypedDict
from dotenv import load_dotenv

from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langchain.chat_models import init_chat_model
from langgraph.checkpoint.memory import MemorySaver, InMemorySaver
from langgraph.store.memory import InMemoryStore

load_dotenv()

class State(TypedDict):
    messages: Annotated[list, add_messages]
    
llm = init_chat_model(
    "azure_openai:gpt-4o-mini"
)

def chatbot(state: State):
    return {"messages": [llm.invoke(state["messages"])]}

workflow = StateGraph(State)
workflow.add_node("llmchatbot", chatbot)
workflow.add_edge(START, "llmchatbot")
workflow.add_edge("llmchatbot", END)

in_memory_store = InMemoryStore()
user_id = "1"
namespace_for_memory = (user_id, "memories")
memory_id = str(uuid.uuid4())
memory = {"food_preference" : "I like pizza"}
in_memory_store.put(namespace_for_memory, memory_id, memory)

# memories = in_memory_store.search(namespace_for_memory)
# print("Memories for user:", memories[-1].dict())

checkpointer = InMemorySaver()

graph = workflow.compile(
    checkpointer=checkpointer, 
    store=in_memory_store
)

config = {"configurable": {"thread_id": "1", "user_id": user_id}}

while True:
    user_input = input("You: ")
    
    if user_input.lower() in ["exit", "quit"]:
        print("Exiting the chatbot.")
        break
    
    # response = graph.invoke(
    #     {
    #         "messages": [
    #             {"role": "user", "content": user_input}
    #         ]
    #     },
    #     config=config
    # )
    
    # First let's just say hi to the AI
    for chunk in graph.stream(
        {"messages": [{"role": "user", "content": user_input}]}, config, stream_mode="values"
    ):
        chunk["messages"][-1].pretty_print()
    
    # get the latest state snapshot
    # latest_snapshot = graph.get_state(config)
    # print("Latest state snapshot:", latest_snapshot)
    
    # get all state snapshots
    # all_snapshots = list(graph.get_state_history(config))
    # for snapshot in all_snapshots:
    #     print(snapshot)
    
    # print("Bot:", response["messages"][-1].content)