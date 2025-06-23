import os, uuid
from typing import Annotated
from typing_extensions import TypedDict
from dotenv import load_dotenv

from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langchain.chat_models import init_chat_model
from langgraph.checkpoint.memory import InMemorySaver
from langchain_core.runnables import RunnableConfig
from langgraph.store.memory import InMemoryStore
from langgraph.store.base import BaseStore

load_dotenv()

class State(TypedDict):
    messages: Annotated[list, add_messages]
    
llm = init_chat_model(
    "azure_openai:gpt-4o-mini"
)

def chatbot(state: State, config: RunnableConfig, *, store: BaseStore):
    user_id = config["configurable"]["user_id"]
    namespace = ("memories", user_id)
    memories = store.search(namespace, query=str(state["messages"][-1].content))
    info = "\n".join([d.value["data"] for d in memories])
    system_msg = f"You are a helpful assistant talking to the user. User info: {info}"
    
    # store.put(namespace, str(uuid.uuid4()), {"data": "user name is chandan"})
    # store.put(namespace, str(uuid.uuid4()), {"data": "user age is 30"})
    
    # Store new memories if the user asks the model to remember
    # last_message = state["messages"][-1]
    # if "remember" in last_message.content.lower():
    #     memory = "User name is Bob"
    #     store.put(namespace, str(uuid.uuid4()), {"data": memory})
    
    response = llm.invoke(
        [{"role": "system", "content": system_msg}] + state["messages"]
    )
    
    print([{"role": "system", "content": system_msg}] + state["messages"])
    
    return {"messages": response}

workflow = StateGraph(State)
workflow.add_node("llmchatbot", chatbot)
workflow.add_edge(START, "llmchatbot")
workflow.add_edge("llmchatbot", END)

checkpointer = InMemorySaver()
store = InMemoryStore()
namespace = ("memories", "1")
store.put(namespace, str(uuid.uuid4()), {"data": "user name is chandan"})
store.put(namespace, str(uuid.uuid4()), {"data": "user age is 30"})

graph = workflow.compile(
    checkpointer=checkpointer,
    store=store,
)

config = {
    "configurable": {
        "thread_id": "22",
        "user_id": "1",
    }
}

while True:
    user_input = input("You: ")
    
    if user_input.lower() in ["exit", "quit"]:
        print("Exiting the chatbot.")
        break
    
    # First let's just say hi to the AI
    for chunk in graph.stream(
        {"messages": [{"role": "user", "content": user_input}]}, config, stream_mode="values"
    ):
        chunk["messages"][-1].pretty_print()