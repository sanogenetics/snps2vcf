# Stage 1: Build environment to download resources
FROM python:3.12-alpine AS builder

WORKDIR /app

# Create a virtual environment and install snps to download resources
RUN python -m venv venv \
  && . venv/bin/activate \
  && pip install --no-cache-dir snps==2.8.2

# Copy and run the script to download resources
COPY docker/setup_container.py .
RUN . venv/bin/activate && python setup_container.py

# Stage 2: Final image
FROM python:3.12-alpine

WORKDIR /app

# Copy the downloaded resources from the build stage
COPY --from=builder /app/resources /app/resources

# Create a virtual environment for the main application
RUN python -m venv venv

# Install requirements
COPY requirements.txt .
RUN . venv/bin/activate && pip install --no-cache-dir -r requirements.txt

# Install the actual code
COPY snps2vcf ./snps2vcf
COPY setup.py .
COPY README.md .
COPY requirements-dev.txt .
RUN . venv/bin/activate && pip install --no-cache-dir .

# Add the wrapper script
COPY docker/run.sh .

CMD ["sh", "run.sh"]
