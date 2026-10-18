FROM python:3.11-slim

RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir "moto[server]"

EXPOSE 9000

CMD ["moto_server", "-H", "0.0.0.0", "-p", "9000"]