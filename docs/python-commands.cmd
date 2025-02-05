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