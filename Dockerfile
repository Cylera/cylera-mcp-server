FROM python:3.13-slim

# Set the working directory in the container
WORKDIR /app

# Install uv for package management
COPY --from=ghcr.io/astral-sh/uv:0.8.14 /uv /bin/uv

# Copy the dependency files
COPY pyproject.toml uv.lock ./

# Install dependencies using uv
RUN uv sync --frozen --no-dev --no-build

# Copy the rest of the application code
COPY server.py .

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
#
# Or, hosted for many people (remote mode), signing each in through WorkOS
# AuthKit, with no Cylera password:
# - CYLERA_MCP_MODE=remote
# - CYLERA_BASE_URL: the region's Partner API
# - WORKOS_AUTHKIT_DOMAIN
# - MCP_PUBLIC_BASE_URL: this server's public URL, without /mcp
# - MCP_HOST=0.0.0.0, so the container's port is reachable
# docker run -p 8124:8124 -e CYLERA_MCP_MODE=remote -e MCP_HOST=0.0.0.0 -e CYLERA_BASE_URL=your_url \
#   -e WORKOS_AUTHKIT_DOMAIN=your_domain -e MCP_PUBLIC_BASE_URL=your_public_url mcp-cylera-server
EXPOSE 8124

# Command to run the application
CMD ["uv", "run", "--frozen", "--no-build", "server.py"]
