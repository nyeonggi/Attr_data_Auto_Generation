# Base image with CUDA support
FROM nvidia/cuda:12.2.0-base-ubuntu20.04

# Set environment variables
ENV DEBIAN_FRONTEND=noninteractive

# Install system dependencies
RUN apt-get update && apt-get install -y \
    python3-pip \
    git \
    zip htop screen libgl1-mesa-glx \
    libglib2.0-0 libsm6 libxrender1 libxext6 libgtk2.0-0 \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

    

    # Set Python alias
RUN ln -s /usr/bin/python3 /usr/bin/python

# Copy YOLOv7 files into the container
WORKDIR /yolov7
COPY . /yolov7

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose a default command (you can modify this later)
CMD ["bash"]
