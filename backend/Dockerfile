FROM python:3.13.6-slim

WORKDIR /stenos_api

COPY requirements.txt .
COPY .env .

RUN pip install --no-cache-dir -r requirements.txt

COPY ./stenos_api ./stenos_api

CMD ["uvicorn", "stenos_api.main:stenos_application", "--host", "0.0.0.0", "--port", "8000", "--reload", "--log-level", "debug"]