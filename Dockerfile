# Use the python base image from Docker Hub
FROM python:3.10.6-buster

# Set the working directory in the container to /app
WORKDIR /app
COPY . .
# Copy requirements.txt first for caching pip install step
COPY requirements.txt .



# Upgrade pip and install the required packages
RUN python3 -m pip install -r requirements.txt


# Expose the port for the Streamlit app
EXPOSE 8501

ENTRYPOINT ["streamlit", "run", "home.py", "--server.port=8501", "--server.address=0.0.0.0 "]
