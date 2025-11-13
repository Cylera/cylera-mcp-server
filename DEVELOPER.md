## Publishing to the MCP Registry

This information is not relevant for general usage of the Cylera MCP server.
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

Once the changes have been made, it is committed and pushed up to the Cylera fork and
where a PR is created as part of the process of getting the new version published in the
Docker MCP Registry.

To test changes locally before creating the PR follow these steps within a
clone of the fork:

1. Commit and push the changes to the MCP server up to cylera-mcp-server
2. Record the commit hash
3. Update the servers/cylera-mcp-server/server.yaml with the new commit hash.
4. Then run these commands on the command line within the mcp-registry
   directory:

    task build -- --tools cylera-mcp-server
    task catalog -- cylera-mcp-server
    docker mcp catalog import $PWD/catalogs/cylera-mcp-server/catalog.yaml
    echo "Now re-launch Docker Desktop and see if cylera-mcp-server is there"
    echo "Once tested, Reset your catalog in Docker Desktop with: task reset"

Note that the MCP server is run as a Docker container - and so it is important
to build and test the image locally before submitting the PR.
