FROM python:3.10-slim

ENV PYTHONPATH=/app
WORKDIR /app
COPY . .

RUN pip install --upgrade pip && \
    pip install -r requirements.txt

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
