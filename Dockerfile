FROM python:3.9-alpine3.16

# Install postgres and build dependencies
RUN apk add --no-cache postgresql-client build-base postgresql-dev

# Setup the working directory
WORKDIR /service

# Install Python dependencies
COPY requirements.txt /service/
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy the project code
COPY . /service

# Create a non-root user and switch to it
RUN adduser --disabled-password --gecos '' service-user
USER service-user

# Expose the port the app runs on
EXPOSE 8000
