FROM python:3.10-slim

WORKDIR /app

COPY requirements-prod.txt .
RUN pip install --no-cache-dir -r requirements-prod.txt

COPY . .

RUN mkdir -p instance && chown -R 1000:1000 /app

EXPOSE 7860

CMD ["gunicorn", "--bind", "0.0.0.0:7860", "run:app"]

