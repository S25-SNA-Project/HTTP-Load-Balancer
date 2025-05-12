FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app

EXPOSE 8888 8080

CMD ["sh", "-c", "uvicorn app1:app --host 0.0.0.0 --port 8888 & uvicorn app2:app --host 0.0.0.0 --port 8080"]
