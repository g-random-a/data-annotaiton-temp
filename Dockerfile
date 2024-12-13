# Use Python image
FROM python:3.11

# Set working directory
WORKDIR /app

# Copy requirements.txt and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application source code
COPY . .

# Run Flask app
# CMD ["gunicorn", "app.routes.upload:app", "--bind", "0.0.0.0:5000", "--workers", "4"]
CMD ["flask", "run"]