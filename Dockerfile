# Use an official Miniconda base image
FROM continuumio/miniconda3:latest

# Set the working directory
WORKDIR /

# Update the package list and install any dependencies
RUN apt-get update && apt-get install -y \
    curl git \
    && rm -rf /var/lib/apt/lists/*

# Create a new conda environment with Python 3.10
RUN conda create --name xmen python=3.10 -y

# Activate the environment and ensure it persists
SHELL ["conda", "run", "-n", "xmen", "/bin/bash", "-c"]

# Copy the application code and requirements file into the container
COPY requirements.txt .
COPY *.py .

# Install binary dependencies from conda
RUN conda install -c conda-forge nmslib cymem murmurhash -y

# Install pip dependencies
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5000

# Define the command to run the server with parameters
CMD ["/opt/conda/envs/xmen/python", "run_snomed_german_recommender.py", "--no-gpu", "--port", "5000", "index"]