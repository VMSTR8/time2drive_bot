FROM python:3.13-slim

RUN pip install --upgrade pip

COPY bot/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

COPY bot/ /app
WORKDIR /app

RUN chmod +x entrypoint.sh

CMD ["/app/entrypoint.sh"]
