FROM python:3.13-slim

# Set the working directory in the container
WORKDIR /app

# Install uv for package management
RUN pip install uv

# Copy the dependency files
COPY pyproject.toml uv.lock ./

# Install dependencies using uv
RUN uv sync --frozen --no-dev

# Copy the rest of the application code
COPY . .

# Create non-root user
RUN useradd -m -u 1000 mcpuser && \
    chown -R mcpuser:mcpuser /app

# Switch to non-root user
USER mcpuser

# The server expects the following environment variables to be set at runtime:
# - CYLERA_USERNAME
# - CYLERA_PASSWORD
# - CYLERA_BASE_URL
#
# Example of how to run the container with these variables:
# docker run -e CYLERA_USERNAME=your_user -e CYLERA_PASSWORD=your_pass -e CYLERA_BASE_URL=your_url mcp-cylera-server

# Command to run the application
CMD ["uv", "run", "server.py"]
