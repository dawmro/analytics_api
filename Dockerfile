# Use official Python 3.12 slim base image
FROM python:3.12.5-slim-bullseye

# Create virtual environment in /opt/venv directory
RUN python -m venv /opt/venv

# Add virtual environment binaries to system PATH
ENV PATH=/opt/venv/bin:$PATH

# Ensure latest version of pip is installed in virtual environment
RUN pip install --upgrade pip

# Set Python-related environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install dependencies for mini vm
RUN apt-get update && apt-get install -y \
    # for PostgreSQL client library
    libpq-dev \
    # for image processing with Pillow
    libjpeg-dev \
    # for SVG rendering with CairoSVG
    libcairo2 \
    # compiler for building Python packages
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Create mini vm code directory
RUN mkdir -p /code

# Set working directory to the same directory
WORKDIR /code

# Copy the requirements file into the container
COPY requirements.txt /tmp/requirements.txt

# Copy the project code into the container's working directory
COPY ./src /code

# Install the python project requirements
RUN pip install -r /tmp/requirements.txt

# Make the bash script executable
COPY ./boot/docker-run.sh /opt/run.sh
RUN chmod +x /opt/run.sh

# Clean up apt cache to reduce image size
# Remove build dependencies and cleanup
RUN apt-get remove --purge -y \
    # Remove automatically installed unused dependencies
    && apt-get autoremove -y \
    # Clean package cache
    && apt-get clean \
    # Remove cached package lists
    && rm -rf /var/lib/apt/lists/*

# Run the FastAPI project via the runtime script
# when the container starts
CMD ["/opt/run.sh"]
