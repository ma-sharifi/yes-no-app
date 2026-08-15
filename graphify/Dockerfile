# Graphify knowledge-graph service for this project.
#
# Builds and serves a queryable code knowledge graph using the "graphifyy"
# package (CLI command: `graphify`). The project is bind-mounted at /workspace
# by docker-compose, so the same image is used both to extract the graph and
# to serve it over the MCP HTTP transport.
FROM python:3.12-slim

# git: graphify honors .gitignore and may shell out to git.
RUN apt-get update \
    && apt-get install -y --no-install-recommends git \
    && rm -rf /var/lib/apt/lists/*

# PyPI package name is "graphifyy" (double y); the CLI it installs is "graphify".
RUN pip install --no-cache-dir graphifyy

WORKDIR /workspace

# Default action for this image: serve the prebuilt graph over MCP HTTP.
# The `graphify-build` service overrides the entrypoint to run extraction.
EXPOSE 8080
ENTRYPOINT ["python", "-m", "graphify.serve"]
CMD ["graphify-out/graph.json", "--transport", "http", "--host", "0.0.0.0", "--port", "8080"]
