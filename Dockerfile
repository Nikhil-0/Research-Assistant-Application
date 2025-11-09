# Use Python 3.12 as the base image
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy the application code
COPY . .

# Set environment variables
ENV PORT=8080
ENV HOST=0.0.0.0

# Expose the port the app runs on
EXPOSE 8080

# Command to run the application
CMD streamlit run --server.port $PORT --server.address $HOST app/ResearchApp.py