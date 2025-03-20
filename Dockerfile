# 使用官方 Python 執行環境作為基礎映像檔
FROM python:3.12.9-slim

# 設定容器內的工作目錄
WORKDIR /app

# 複製專案檔案
COPY pyproject.toml poetry.lock* ./
COPY ./src/deli_audio_analysis/deli_audio_analysis.py ./src/deli_audio_analysis/__init__.py ./src/app.py ./
COPY README.md LICENSE ./

# 安裝 Poetry
RUN pip install --no-cache-dir poetry

# 設定 Poetry 不創建虛擬環境並安裝專案依賴
RUN poetry config virtualenvs.create false && poetry install --no-interaction --without dev

# 暴露 Streamlit 應用程式運行的端口
EXPOSE 8501

# 定義啟動應用程式的命令
CMD ["poetry", "run", "streamlit", "run", "./src/app.py"]