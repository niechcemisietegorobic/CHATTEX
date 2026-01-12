FROM python:3.13

WORKDIR /backend

COPY ./requirements.txt /backend/
RUN pip install --no-cache-dir -r requirements.txt

COPY ./ /backend/

EXPOSE 80

CMD ["python3", "-m", "gunicorn", "--bind", "0.0.0.0:80", "-k", "gevent", "-w", "1", "app:app"]

