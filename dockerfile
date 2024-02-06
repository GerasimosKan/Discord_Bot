# Use an official Python runtime as a parent image
FROM python:3.9

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app/

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Make port 8949 available to the world outside this container
EXPOSE 8949

# Define environment variable
#ENV BOT_TOKEN=NTkwOTE4OTAzNzc4MjQ2NjU2.G3pVYn.F3XrcVInVoal4wErb_mWfK3p2LiA6N_neUD41Y

# Run main.py when the container launches
CMD ["python", "app/main.py"]
