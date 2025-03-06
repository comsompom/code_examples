FROM python:3.11-alpine

WORKDIR /fast-api

COPY ./requirements.txt /fast-api/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /fast-api/requirements.txt

COPY . /fast-api

CMD ["uvicorn", "main_page:app", "--host", "0.0.0.0", "--port", "8000"]
