# ----------------------------------------------------------------------
# STAGE 1: Build Stage (Used to install dependencies efficiently)
# ----------------------------------------------------------------------
FROM python:3.10-slim AS builder

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install Python dependencies. 
# We use 'no-cache-dir' and 'upgrade pip' for a cleaner and faster install.
# Note: Ensure all packages like Flask, numpy, pandas, and scikit-learn are listed.
RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# ----------------------------------------------------------------------
# STAGE 2: Production/Runtime Stage (The final, minimal image)
# ----------------------------------------------------------------------
FROM python:3.10-slim

# Set the same working directory as the builder
WORKDIR /app

# Copy only the installed dependencies from the builder stage
# This makes the final image smaller as it avoids build-time tools.
COPY --from=builder /usr/local/lib/python3.10/site-packages /usr/local/lib/python3.10/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# Copy your application code and ML artifacts
# This includes app.py, the src/ directory, and the templates/ directory.
COPY app.py .
COPY src /app/src
COPY templates /app/templates
# NEW: Copy the essential 'artifact' folder containing the model and preprocessor
COPY artifact /app/artifact 

# Expose the port that Flask runs on (default is 5000)
EXPOSE 5000

# Set an environment variable for Flask (Good practice)
ENV FLASK_APP=app.py

# Command to run the application when the container starts.
# We use Gunicorn, a production-ready WSGI server, instead of the Flask development server.
# It runs 4 worker processes and binds to port 5000 on all interfaces.
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]