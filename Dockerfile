# Stage 1: Build Nanobot Engine
FROM golang:1.24-bookworm AS builder

WORKDIR /src
RUN git clone https://github.com/nanobot-ai/nanobot.git .

# Patch: Force go.mod to accept Go 1.24 (since 1.25 docker image is not available)
RUN sed -i 's/^go .*/go 1.24/g' go.mod && \
    sed -i 's/^go .*/go 1.24/g' pkg/tools/flows.go || true

# Build
RUN make

# Stage 2: Runtime Environment
FROM python:3.11-bookworm

WORKDIR /app

# Install System Dependencies (Runtime)
RUN apt-get update && apt-get install -y \
    curl \
    git \
    nodejs \
    npm \
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
    && rm -rf /var/lib/apt/lists/*

# Copy Nanobot Binary from Builder
COPY --from=builder /src/bin/nanobot /usr/local/bin/nanobot

# Install Python Deps
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Install Playwright Browsers
RUN playwright install chromium

COPY . .

EXPOSE 8501
CMD ["streamlit", "run", "dashboard.py", "--server.address=0.0.0.0", "--server.port=8501"]
