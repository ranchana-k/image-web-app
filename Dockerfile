# Use the official Python image.
FROM python:3.9-slim

# Set the working directory in the container.
WORKDIR /app

# Copy the requirements file and install dependencies.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code.
COPY . .

# Set the environment variable for the bucket name.
ENV BUCKET_NAME=image-web-app

# Expose the port that Flask listens on.
EXPOSE 8080

# Run the Flask application.
CMD ["python", "main.py"]