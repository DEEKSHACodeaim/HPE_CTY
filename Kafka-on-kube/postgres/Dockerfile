# Use the official Python image as the base image
FROM python:3.7-slim

ENV PYTHONDONTWRITEBYTECODE=1

RUN pip3 install psycopg2-binary
RUN pip3 install flask

# Copy the rest of the application code into the container
COPY try.py .
COPY dump.sql .
# Expose port 5000 for the Flask application
EXPOSE 5000

# Start the Flask application when the container starts
CMD ["python3", "-u", "./try.py"]
