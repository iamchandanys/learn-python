@REM Virtual Environment using Anaconda

@REM To create a virtual environment
conda create -p venv python==3.12

@REM To activate a virtual environment
conda activate venv/

@REM To deactivate a virtual environment
conda deactivate

------------------------------------------------------------

@REM Virtual Environment using Python

@REM To create a virtual environment
python -m venv myenv

@REM To activate a virtual environment
myenv\Scripts\activate

@REM To deactivate a virtual environment
deactivate

------------------------------------------------------------

@REM To install the required packages
pip install -r requirements.txt

-------------------------------------------------------------

@REM Virtual Environment using UV package

@REM To init the UV package
uv init

@REM To create a virtual environment
uv venv

@REM To activate a virtual environment
.venv\Scripts\activate

@REM To install the required packages
uv add -r requirements.txt