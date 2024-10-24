# Use a minimal base image
FROM python:3.9-slim AS builder

# Set the working directory to /app
WORKDIR /app


# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libffi-dev \
    libssl-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy only requirements.txt initially to leverage Docker caching
COPY requirements.txt .

# Install required Python packages with specific versions
RUN pip install --no-cache-dir -r requirements.txt

# Second stage, copy only necessary files from builder stage
FROM python:3.9-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    libssl-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy installed packages from the builder stage
COPY --from=builder /usr/local/lib/python3.9/site-packages/ /usr/local/lib/python3.9/site-packages/

# Copy the rest of the application
COPY . .

# Make port 8949 available to the world outside this container
EXPOSE 8949

# Run main.py when the container launches
CMD ["python", "app/main.py"]
