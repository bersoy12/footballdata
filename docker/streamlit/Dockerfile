FROM python:3.11-slim

WORKDIR /app

# RUN apk update && apk add --no-cache \
#     build-base \
#     curl \
#     git \
#     postgresql-dev


RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    software-properties-common \
    git \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt watchdog

RUN mkdir -p /app/streamlit-app

WORKDIR /app/streamlit-app

EXPOSE 8501

HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

ENTRYPOINT ["streamlit"]

CMD ["run", "app.py", "--server.port=8501", "--server.address=0.0.0.0", "--server.runOnSave=true", "--server.fileWatcherType=poll"]