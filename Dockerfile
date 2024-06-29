# Use an official Python runtime as a parent image
FROM python:3.6

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory in the container
WORKDIR /usr/src/app

# Install system dependencies
RUN apt-get update && apt-get install -y netcat

# Install Python dependencies
COPY requirements.txt /usr/src/app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy the current directory contents into the container at /usr/src/app
# COPY ./ /usr/src/app/

# Expose the port the app runs on
EXPOSE 8000

# Command to run the application
# CMD ["python", "./new_nm_api/manage.py", "runserver", "0.0.0.0:8000"]

CMD ["/bin/sh", "-c", "python ./new_nm_api/manage.py migrate && python ./new_nm_api/manage.py runserver 0.0.0.0:8000"]