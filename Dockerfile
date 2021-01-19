FROM tiangolo/uvicorn-gunicorn-fastapi:python3.7

# Copy the files into the Docker image
COPY requirements.txt /app/requirements.txt
COPY ./main.py /app/main.py

EXPOSE 8000

# Install dependencies
RUN pip install -r /app/requirements.txt
