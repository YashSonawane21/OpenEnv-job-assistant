FROM python:3.10

WORKDIR /app

COPY . .

RUN pip install -r requirements.txt

EXPOSE 7860

# Use tail to keep container running and capture all output
CMD ["sh", "-c", "uvicorn inference:app --host 0.0.0.0 --port 7860 --timeout-keep-alive 60 --access-log"]