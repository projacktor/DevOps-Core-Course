FROM python:3.13-slim

RUN groupadd -r app && useradd -r -g app app
WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
RUN chown -R app:app /app

USER app

EXPOSE 8080
CMD ["python", "app.py"]