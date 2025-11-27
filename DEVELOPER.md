
## Testing

We have unit tests which essentially verify the REST API client
(test_cylera_client.py) works ok.

In addition, we have tests which verify the MCP server itself works as expected by an
MCP client (test_mcp_server.py). 

Run the testsuite as follows:

    uv run pytest -v -s

We do not run any integration tests directly from an LLM as a) this is too slow b)
cumbersome and c) potentially expensive. Once the tests pass, it is highly
likely there will be no issues plugging in the MCP server into a host such as
Claude.

If changes are made to the Dockerfile, it is important to test the Docker image
as follows from the top-level directory of the repo:

    docker build -t cylera.com/cylera-mcp-server:latest .
    ./test_docker_container.sh

This is just a sanity test to make sure the Docker image has been built and
will run ok.

Once the tests run ok, create a PR. Once merged, record the commit hash to
ensure this latest version is used by the Docker MCP registry.

You may choose to use [MCP
Inspector](https://modelcontextprotocol.io/docs/tools/inspector#npm-package) by
launching this script:

    mcpinspector.sh

## Publishing to the MCP Registry

This information is for Cylera developers who wish to publish a new version to
the Docker MCP Registry.

In compliance with [Docker's guidelines](https://github.com/docker/mcp-registry/blob/main/CONTRIBUTING.md), a fork is maintained by Cylera [fork](https://github.com/Cylera/mcp-registry) of the [Official Docker MCP Registry](https://github.com/docker/mcp-registry).

It is within the fork, that the Cylera team configure how the Cylera MCP server is presented and configured in the MCP Catalog.

Essentially, there is a file called servers/cylera-mcp-server/server.yaml.

The following is an example of the contents of the file:

    name: cylera-mcp-server
    image: mcp/cylera-mcp-server
    type: server
    meta:
      category: productivity
      tags:
        - productivity
    about:
      title: Cylera
      description: |
        Brings context about device inventory, threats, risks and utilization powered by the Cylera Partner API into an LLM.
      icon: https://github.com/Cylera/cylera-mcp-server/blob/main/assets/cylera_logo.png?raw=true
    source:
      project: https://github.com/Cylera/cylera-mcp-server
      commit: 94d6f59bbb07b05da92b5ab02205c5720f3fbe08
    config:
      description: Configure the connection to the official MCP Server for Cylera.
      secrets:
        - name: cylera-mcp-server.cylera.base_url
          env: CYLERA_BASE_URL
          example: "https://partner.us1.cylera.com Or https://partner.uk1.cylera.com/ Or https://partner.demo.cylera.com"
        - name: cylera-mcp-server.cylera.username
          env: CYLERA_USERNAME
          example: "Your username you use to login to Cylera"
        - name: cylera-mcp-server.cylera.password
          env: CYLERA_PASSWORD
          example: "Your password you use to login to Cylera"

The file is pretty self-explanatory. If a new version of the Cylera
MCP server is released, the commit hash corresponding to the new version would
need to be updated.

Note that Docker takes care of building the image. The Cylera team simply maintains the Dockerfile.

We are still seeking documentation from the Docker team for clarity regarding
the process of releasing new versions.

To test changes locally before creating the PR follow these steps within a
clone of the fork:

1. Update the servers/cylera-mcp-server/server.yaml with the new commit hash.
2. Then run these commands on the command line within the mcp-registry
   directory:

       task build -- --tools cylera-mcp-server
       task catalog -- cylera-mcp-server
       docker mcp catalog import $PWD/catalogs/cylera-mcp-server/catalog.yaml

   Now re-launch Docker Desktop and see if cylera-mcp-server is there
   Once tested, Reset your catalog in Docker Desktop with

       task reset

