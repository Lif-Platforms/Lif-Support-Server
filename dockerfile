# Use the official Python image as the base image
FROM python:3.10.2

# Set the working directory inside the container
WORKDIR /

# Copy the entire contents of the src directory to the container's working directory
COPY src/ /

# Install all dependencies from the project directory using -r flag
RUN pip install -r requirements.txt

# Expose the port that Flask app runs on (if you're using a different port, change it here)
EXPOSE 8003

# Command to run your Python app (replace 'app.py' with the main Python file name)
CMD ["python", "main.py"]
