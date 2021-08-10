FROM tiangolo/meinheld-gunicorn-flask:python3.8

COPY . /app
RUN pip install -r /app/requirements.txt
