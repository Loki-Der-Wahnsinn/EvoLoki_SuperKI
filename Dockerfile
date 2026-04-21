FROM python:3.10-slim

# Set up user to run HuggingFace space (required by HF)
RUN useradd -m -u 1000 user
ENV PATH="/home/user/.local/bin:$PATH"

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y gcc git python3-dev && rm -rf /var/lib/apt/lists/*

# Copy the entire workspace into the container and set ownership
COPY --chown=user . /app/

# Switch to the non-root user
USER user

# Install specific versions and requirements
RUN pip install --no-cache-dir --upgrade pip

# Install the local EvoAgentX library directly
RUN if [ -d "EvoAgentX" ]; then pip install --no-cache-dir -r ./EvoAgentX/requirements.txt && pip install --no-cache-dir -e ./EvoAgentX; fi

# Install the rest of the SuperKI requirements
RUN pip install --no-cache-dir -r requirements_superki.txt
RUN pip install --no-cache-dir llama-index llama-index-graph-stores-neo4j

# Expose HuggingFace Space default port
EXPOSE 7860
ENV PORT=7860

# Command to run the application
CMD ["python", "SuperKI_MiniServer.py"]
