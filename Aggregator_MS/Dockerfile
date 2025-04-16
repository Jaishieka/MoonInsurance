FROM python:3.9-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the current directory contents (including requirements.txt) into the container
COPY . /app

# Install dependencies from requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Command to run your aggregator.py when the container starts
CMD ["python", "aggregator.py"]
