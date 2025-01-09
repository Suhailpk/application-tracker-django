FROM python:3.9-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Update package list and install dependencies for MySQL/MariaDB and build tools
RUN apt-get update && apt-get install -y \
    pkg-config \
    libmariadb-dev \
    libmariadb-dev-compat \
    build-essential \
    && rm -rf /var/lib/apt/lists/*



# Set work directory
WORKDIR /app

# Copy requirements and install Python dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . /app/

# Expose port
EXPOSE 8000

# Run the application
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
