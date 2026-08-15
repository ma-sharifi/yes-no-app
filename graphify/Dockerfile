# Graphify knowledge-graph CLI for this project.
#
# Builds and queries a queryable code knowledge graph using the "graphifyy"
# package (CLI command: `graphify`). The project is bind-mounted at /workspace
# by docker-compose. This image runs the CLI only — there is no MCP server.
FROM python:3.12-slim

# git: graphify honors .gitignore and may shell out to git.
RUN apt-get update \
    && apt-get install -y --no-install-recommends git \
    && rm -rf /var/lib/apt/lists/*

# PyPI package name is "graphifyy" (double y); the CLI it installs is "graphify".
RUN pip install --no-cache-dir graphifyy

WORKDIR /workspace

# The entrypoint is the CLI itself, so any subcommand can be passed as the
# compose command / `docker compose run` arguments:
#   extract . --force        (default — rebuild the graph)
#   query "..."              (search the graph)
ENTRYPOINT ["graphify"]
CMD ["extract", ".", "--force"]
