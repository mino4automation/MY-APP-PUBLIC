# Use a smaller Python base image
FROM python:3.8-slim

# Set the working directory
WORKDIR /app

# Copy only necessary files
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application files
COPY . /app

# Expose the Flask port
EXPOSE 5000

# Run the Flask application
CMD ["python", "app.py"]
    