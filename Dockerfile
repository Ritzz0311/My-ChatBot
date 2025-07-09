# Use the official Python image
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements and app files
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Expose port (Flask default is 5000)
EXPOSE 5000

# Set environment variables for Flask
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0

# Command to run the app
CMD ["flask", "run"]
