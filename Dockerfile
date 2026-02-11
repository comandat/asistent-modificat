FROM python:3.11-bookworm

WORKDIR /app

# 1. Install System Dependencies
RUN apt-get update && apt-get install -y \
    curl \
    git \
    nodejs \
    npm \
    golang-go \
    libnss3 \
    libnspr4 \
    libatk1.0-0 \
    libatk-bridge2.0-0 \
    libcups2 \
    libdrm2 \
    libxkbcommon0 \
    libxcomposite1 \
    libxdamage1 \
    libxfixes3 \
    libxrandr2 \
    libgbm1 \
    libasound2 \
    libpango-1.0-0 \
    libcairo2 \
    make \
    && rm -rf /var/lib/apt/lists/*

# 2. Install Nanobot (Build from Source)
# We clone the official repo or use the one provided. 
# Since we don't have the source in THIS repo, we clone it.
RUN git clone https://github.com/nanobot-ai/nanobot.git /tmp/nanobot-src \
    && cd /tmp/nanobot-src \
    && make \
    && mv bin/nanobot /usr/local/bin/nanobot \
    && rm -rf /tmp/nanobot-src

# 3. Install Python Dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# 4. Install Playwright Browsers
RUN playwright install chromium

# 5. Copy Project Files
COPY . .

EXPOSE 8501

# 6. Run Dashboard
CMD ["streamlit", "run", "dashboard.py", "--server.address=0.0.0.0", "--server.port=8501"]
