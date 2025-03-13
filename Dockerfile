# Use an official Python base image
FROM python:3.9

# Set the working directory in the container
WORKDIR /app

# Copy all files to the container
COPY . /app

# Install required dependencies
RUN pip install --no-cache-dir pandas rdkit-pypi ttkbootstrap

# Install Tkinter (optional, already included in many Python images)
RUN apt-get update && apt-get install -y python3-tk

# Set the command to run the application
CMD ["python", "base.py"]
