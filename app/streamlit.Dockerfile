# Используем Python 3.12
FROM python:3.12

# Устанавливаем зависимости
WORKDIR /app
COPY requirements_web.txt ./
RUN pip install --no-cache-dir -r requirements_web.txt

# Копируем Streamlit-приложение
COPY streamlit_app.py /app/

# Запуск Streamlit
CMD ["streamlit", "run", "streamlit_app.py", "--server.port=8085", "--server.address=0.0.0.0"]
