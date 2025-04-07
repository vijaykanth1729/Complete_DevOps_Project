# Use an official lightweight Python image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy only the required files
COPY ./src/requirements.txt requirements.txt

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application files
COPY ./src .

# Expose the port Flask runs on
EXPOSE 5000

# Command to run the application
CMD ["python", "app.py"]
