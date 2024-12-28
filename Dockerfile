FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY src/ ./src/
COPY tests/ ./tests/
COPY .env .

# Set Python path
ENV PYTHONPATH=/app

# Default command
# CMD ["python", "src/dexscreener.py"]