Write-Host "Installing Poetry env..."
poetry install
Write-Host "Poetry env installed"
Write-Host "starting Streamlit app..."
poetry run streamlit run src\app.py
Write-Host "Streamlit app started" 