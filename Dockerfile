# Use the official Python image from the Docker Hub as a base image
FROM python:3.10-slim as base

# Create a virtual environment for the application
RUN python -m venv /opt/venv

# Install the dependencies in a separate stage to leverage Docker layer caching
FROM base as builder

# Install build dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy the requirements file
COPY requirements.txt .

# Install the dependencies into the virtual environment
RUN /opt/venv/bin/pip install --no-cache-dir -r requirements.txt

# Create a non-root user and group
RUN addgroup --system appgroup && adduser --system --ingroup appgroup appuser

# Copy the dependencies from the builder stage
FROM base

# Copy the virtual environment from the builder stage
COPY --from=builder /opt/venv /opt/venv

# Set environment variables
ENV PATH="/opt/venv/bin:$PATH"

# Set the working directory
WORKDIR /app

# Copy the FastAPI app code
COPY . .

# Change ownership to the non-root user (use numerical IDs to avoid issues)
RUN chown -R 1000:1000 /app

# Switch to the non-root user (use numerical IDs to avoid issues)
USER 1000:1000

# Expose the port the app runs on
EXPOSE 8000

# Command to run the FastAPI app with uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
