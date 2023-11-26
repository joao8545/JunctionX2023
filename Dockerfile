# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Make port 80 available to the world outside this container
EXPOSE 5000

# Set environment variables
ENV MONGODB_ADDRESS="mongodb://localhost:27017/mydatabase"
ENV NTFY_BASE_URL="https://ntfyserv.joaoanastacio.com/"

# Run app.py when the container launches
CMD ["python", "app.py"]
