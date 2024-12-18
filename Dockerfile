# Use an official Miniconda base image
FROM continuumio/miniconda3:latest

# Set the working directory
WORKDIR /

# Copy the application code and requirements file into the container
COPY requirements.txt .
COPY *.py .

# Update the package list and install any dependencies
RUN apt-get update && apt-get install -y \
    curl git \
    && rm -rf /var/lib/apt/lists/*

# Create a new conda environment with Python 3.10
RUN conda create --name xmen python=3.10 -y
SHELL ["conda", "run", "-n", "xmen", "/bin/bash", "-c"]

# Install binary dependencies from conda
RUN conda install -n xmen -c conda-forge nmslib cymem murmurhash -y

# Install pip dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Download the pre-trained models so they are cached in the Docker image
RUN python download_models.py

EXPOSE 5000

# Define the command to run the server with parameters
CMD ["conda", "run", "--no-capture-output", "-n", "xmen", "python3", "-u", "run_snomed_german_recommender.py", "--no-gpu", "--port", "5000", "index", "--num_recs", "10"]
