FROM python:3.8.5

WORKDIR /app

COPY ./api_foodgram/requirements.txt .
RUN pip3 install -r requirements.txt --no-cache-dir

COPY api_foodgram .

CMD ["gunicorn", "api_foodgram.wsgi:application", "--bind", "0:8000" ]