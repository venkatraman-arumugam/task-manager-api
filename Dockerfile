FROM python:3.9-slim

WORKDIR /work

RUN groupadd -r appgroup && useradd -r -g appgroup appuser

COPY . /work

RUN pip install --no-cache-dir -r requirements.txt

RUN chown -R appuser:appgroup /work

USER appuser

EXPOSE 5000

CMD ["flask", "run", "--host=0.0.0.0"]
