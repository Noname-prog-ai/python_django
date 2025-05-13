   FROM python:3.9

   ENV PYTHONUNBUFFERED 1
   WORKDIR /app

   # Установите зависимости
   COPY requirements.txt .
   RUN pip install -r requirements.txt

   # Копируйте все файлы приложения
   COPY . .

   CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
