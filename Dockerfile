# Use a minimal base image with Python 3.9 installed
FROM python:3.9-slim

# Set environment variables to prevent interactive prompts
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory inside the container to /app
WORKDIR /app

# Copy all files (including apiroute.env) into the container
COPY . .

# Install Python dependencies
RUN pip3 install --no-cache-dir -r requirements.txt

# Install dotenv to read .env files inside app.py
RUN pip3 install python-dotenv

# Expose the port Streamlit uses
EXPOSE 8501

# Define the command to run the Streamlit app
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0", "--server.enableXsrfProtection=false"]
