FROM python:3.9-slim

WORKDIR /work

RUN groupadd -r appgroup && useradd -r -g appgroup appuser

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY app app

RUN chown -R appuser:appgroup app

USER appuser

EXPOSE 5000

CMD ["flask", "run", "--host=0.0.0.0"]
