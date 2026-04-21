FROM python:3.10-slim

WORKDIR /app

# Copy the entire workspace into the container
COPY . /app/

# Install system dependencies
RUN apt-get update && apt-get install -y gcc git python3-dev && rm -rf /var/lib/apt/lists/*

# Install specific versions and requirements
RUN pip install --no-cache-dir --upgrade pip

# Install the local EvoAgentX library directly
RUN if [ -d "EvoAgentX" ]; then pip install --no-cache-dir -e ./EvoAgentX; fi

# Install the rest of the SuperKI requirements
RUN pip install --no-cache-dir -r requirements_superki.txt
RUN pip install --no-cache-dir llama-index llama-index-graph-stores-neo4j

# Expose the port Cloud Run provides
EXPOSE 8080

# Command to run the application
CMD ["python", "SuperKI_MiniServer.py"]
