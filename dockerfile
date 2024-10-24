# First stage: Install dependencies
FROM python:3.9-slim AS builder

# Set the working directory
WORKDIR /app

# Install system dependencies and Python build tools
RUN apt-get update && apt-get install -y \
    build-essential \
    libffi-dev \
    libssl-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy only requirements.txt to leverage Docker cache
COPY requirements.txt .

# Install Python dependencies in the builder stage
RUN pip install --no-cache-dir -r requirements.txt

# Second stage: Create the final image
FROM python:3.9-slim

WORKDIR /app

# Install necessary system dependencies
RUN apt-get update && apt-get install -y \
    libssl-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy installed packages from the builder stage
COPY --from=builder /usr/local/lib/python3.9/site-packages/ /usr/local/lib/python3.9/site-packages/

# Copy the rest of the application
COPY . .

# Expose the necessary port
EXPOSE 8949

# Command to run your application (make sure this is the correct path)
CMD ["python", "app/main.py"]
