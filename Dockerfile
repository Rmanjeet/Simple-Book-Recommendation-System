FROM python:alpine
WORKDIR /app
COPY . /app
RUN pip install -r requirements.txt
CMD gunicorn app:app --bind 0.0.0.0:$PORT --reload