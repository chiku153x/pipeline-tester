FROM python:3.9-slim

# Set working directory
WORKDIR /app


COPY . /app

RUN pip install --upgrade pip && \
    if [ -f requirements.txt ]; then pip install -r requirements.txt; fi


CMD ["python3"]
