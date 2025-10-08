FROM python:3.9-slim

WORKDIR /app

COPY . .

# Install any dependencies (in this case, we don't have external dependencies)
# RUN pip install --no-cache-dir -r requirements.txt

# Expose the port the app runs on
EXPOSE 8000

# Command to run the application
CMD ["python", "server.py"]
