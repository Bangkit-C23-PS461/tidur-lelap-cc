# Use an official Python runtime as the base image
FROM python:3.10.12

# Set the working directory in the container
WORKDIR /app

# Copy the application code to the container
COPY . .

# Install additional dependencies
RUN apt-get update

RUN apt-get install -y ffmpeg libmariadb-dev-compat libmariadb-dev

# Install pipenv
RUN python3 -m pip install pipenv

# Install app dependencies
RUN python3 -m pipenv install --system --deploy

# Expose the port that the Flask app will listen on
EXPOSE 5000

# Run the Flask application
CMD ["python3", "-m", "flask", "--app", "app", "run", "--host=0.0.0.0"]