#!/bin/bash

echo "Installing Poetry env..."
poetry install
echo "Poetry env installed"
echo "starting Streamlit app..."
poetry run streamlit run src\\app.py
echo "Streamlit app started" 