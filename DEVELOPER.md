# Testing and development

There are several layers of testing each with their own testing goals. All of
these tests depend on data that resides in the demo environment. The tests will
fail if the environment is not set to point to https://partner.demo.cylera.com/
for both  TEST_CYLERA_BASE_URL and CYLERA_BASE_URL:

    TEST_CYLERA_BASE_URL="https://partner.demo.cylera.com"
    CYLERA_BASE_URL="https://partner.demo.cylera.com/"

In addition, you will need credentials (username,password) for this environment to be configured.

## Unit tests

The goal of the unit tests contained in [test_cylera_client.py](test_cylera_client.py) is to verify the REST API client
`cylera_client.py`. 

The tests are run as follows (note this command will also run the component
tests):

    uv run pytest -v -s

## Component tests

The goal of the components tests contained in
`test_mcp_server.py` is to verify the MCP server itself
`server.py`. In this test, `test_mcp_server.py`
takes on the role of MCP client which is precisely how a host such Claude
Desktop interacts with the MCP server.

The tests are run as follows (note this command will also run the unit
tests):

    uv run pytest -v -s

## Docker image testing

We do not build and publish a Docker image. Docker (the company)
takes care of this for the purpose of publishing within their MCP Registry
making it available within Docker Desktop. We just need to provide a `Dockerfile`.

If changes are made to the Dockerfile, it is important to test the Docker image
using the `test_docker_container.sh` script as follows:

    ./test_docker_container.sh

This is just a smoke test to make sure the Docker image has been built and
will run ok.

## Running unit, component and Docker tests in one command

For convenience, you can run all the tests as follows:

    ./test.sh

This makes it ideal to incorporate into a CI/CD pipeline.

Check the $? variable - if 0, all tests have passed.

Once the tests run ok, create a PR. 

## Debugging

You may choose to use [MCP Inspector](https://modelcontextprotocol.io/docs/tools/inspector#npm-package) by
launching this script:

    mcpinspector.sh

This might be handy for debugging.

## Publishing to the MCP Registry

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
need to be updated. This is handled automatically when we push to the
cylera-mcp-server registry. We would only need to modify the server.yaml if we
want to change other aspects of the MCP server such as the icon used or the
configuration.

To test changes locally:

1. Update the servers/cylera-mcp-server/server.yaml with the new commit hash.
2. Then run these commands on the command line within the mcp-registry
   directory:

       task build -- --tools cylera-mcp-server
       task catalog -- cylera-mcp-server
       docker mcp catalog import $PWD/catalogs/cylera-mcp-server/catalog.yaml

   Now re-launch Docker Desktop and see if cylera-mcp-server is there
   Once tested, Reset your catalog in Docker Desktop with

       task reset

## Integration testing with an LLM

To test with an LLM, use the prompt `test_llm_integration.md`. This will prompt
the LLM to run the tests, verify the response and summarize the test results.

For Claude Desktop, simply drag and drop the `test_llm_integration.md` file
into Claude Desktop.

For Gemini, simply prompt:

    > Read the prompt contained in @test_llm_integration.md

