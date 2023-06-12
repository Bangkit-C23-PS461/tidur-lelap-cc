# Use an official Python runtime as the base image
FROM python:3.10-alpine

# Install ffmpeg
RUN apk --no-cache add ffmpeg

# Set the working directory in the container
WORKDIR /app

# Copy the application code to the container
COPY . .

# Install pipenv
RUN pip install --user pipenv

# Install dependencies
RUN python3 -m pipenv install --system --deploy

# Expose the port that the Flask app will listen on
EXPOSE 5000

# Run the Flask application
CMD ["python3", "-m", "flask", "--app", "app", "run", "--host=0.0.0.0"]