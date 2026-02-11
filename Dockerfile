FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY . .

# Install Playwright browsers (for skills)
RUN playwright install --with-deps chromium

# Install Node.js (for frontend skills)
RUN curl -fsSL https://deb.nodesource.com/setup_20.x | bash - \
    && apt-get install -y nodejs

EXPOSE 8501
CMD ["streamlit", "run", "dashboard.py"]
