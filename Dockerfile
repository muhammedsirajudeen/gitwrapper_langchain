# Use the official Python image as the base image
FROM python:3.13-slim

# Set the working directory inside the container
WORKDIR /app

# Install pipenv
RUN pip install pipenv

# Copy Pipfile and Pipfile.lock first to take advantage of Docker cache
COPY Pipfile Pipfile.lock /app/

# Install dependencies from Pipenv
RUN pipenv install --dev

# Copy the FastAPI application code to the container
COPY . /app/

# Expose the port the app will run on
EXPOSE 7000

# Use uvicorn with --reload for automatic reloading of FastAPI app during development
CMD ["pipenv", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "7000", "--reload"]
