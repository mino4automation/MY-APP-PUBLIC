# Use a smaller Python base image to reduce image size
# Base image: Python 3.8 on a slim Debian distribution
FROM python:3.8-slim

# Set the working directory inside the container
# Sets /app as the directory for all following commands
WORKDIR /app

# Copy only necessary files to cache dependencies
# Copies requirements code to inside container
COPY requirements.txt /app/
# Installs python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application files
# Copies all source code into the container
COPY . /app

# Expose the Flask port
# Informs Docker that the container listens on port 5000
EXPOSE 5000

# Run the Flask application
# Default command to execute when the container starts
CMD ["python", "app.py"]
