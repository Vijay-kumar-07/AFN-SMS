# Use a base Python image
FROM python:3.9.7

# Set the working directory in the container
WORKDIR /app


# Copy your Python application files to the container
COPY . .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port your application will listen on
EXPOSE 3000

# Define the command to run your Python application
CMD ["python", "./src/index.py"]
