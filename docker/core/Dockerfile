FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    ca-certificates \
    wget \
    gnupg \
    unzip \
    xvfb \
    libxi6 \
    build-essential \
    curl \
    git \
    jq \
    && mkdir -p /etc/apt/keyrings \
    && wget -q -O /etc/apt/keyrings/google-linux-signing-key.gpg https://dl.google.com/linux/linux_signing_key.pub \
    && echo "deb [arch=amd64 signed-by=/etc/apt/keyrings/google-linux-signing-key.gpg] http://dl.google.com/linux/chrome/deb/ stable main" > /etc/apt/sources.list.d/google.list \
    && apt-get update \
    && apt-get install -y google-chrome-stable \
    && rm -rf /var/lib/apt/lists/*

RUN CHROME_VERSION_FULL=$(google-chrome --version | awk '{print $3}') \
    && CHROME_MAJOR=$(echo $CHROME_VERSION_FULL | cut -d'.' -f1) \
    && echo "Detected Chrome version: $CHROME_VERSION_FULL (major: $CHROME_MAJOR)" \
    # Use the Chrome-for-Testing known-good list to pick a matching chromedriver for the installed major version
    && CFT_JSON_URL="https://googlechromelabs.github.io/chrome-for-testing/known-good-versions-with-downloads.json" \
    && DRIVER_VERSION=$(wget -qO- "$CFT_JSON_URL" | jq -r --arg major "$CHROME_MAJOR" '.versions[] | select(.version | startswith($major+".")) | .version' | head -n1) \
    && echo "Resolved driver version: $DRIVER_VERSION" \
    && DRIVER_URL=$(wget -qO- "$CFT_JSON_URL" | jq -r --arg ver "$DRIVER_VERSION" '.versions[] | select(.version==$ver) | .downloads.chromedriver[] | select(.platform=="linux64") | .url') \
    && echo "Downloading chromedriver from: $DRIVER_URL" \
    && wget -q "$DRIVER_URL" -O chromedriver-linux64.zip \
    && unzip chromedriver-linux64.zip \
    && mv chromedriver-linux64/chromedriver /usr/local/bin/chromedriver \
    && chmod +x /usr/local/bin/chromedriver \
    && rm -rf chromedriver-linux64.zip chromedriver-linux

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV DISPLAY=:99
ENV PYTHONUNBUFFERED=1

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]