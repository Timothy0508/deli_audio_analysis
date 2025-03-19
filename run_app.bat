@echo off
echo install Poetry environment...
poetry install
echo Poetry environment has been installed.
echo starting Streamlit app...
poetry run streamlit run src\app.py
echo Streamlit has been closed.
pause