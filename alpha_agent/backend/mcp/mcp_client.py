import json
import requests

class MCPClient:
    """
    A client for interacting with MCP (Model Context Protocol) servers.
    """
    def __init__(self, mcp_server_url):
        """
        Initializes a new MCPClient.

        Args:
            mcp_server_url (str): The URL of the MCP server.
        """
        self.mcp_server_url = mcp_server_url

    def list_tools(self):
        """
        Lists the available tools on the MCP server.

        Returns:
            list: A list of available tools, or None if an error occurs.
        """
        try:
            response = requests.get(f"{self.mcp_server_url}/tools", timeout=10)
            response.raise_for_status()
            return response.json().get("tools", [])
        except requests.exceptions.RequestException as e:
            print(f"Error listing tools from {self.mcp_server_url}: {e}")
            return None

    def use_tool(self, tool_name, **kwargs):
        """
        Uses a tool on the MCP server.

        Args:
            tool_name (str): The name of the tool to use.
            **kwargs: The arguments for the tool.

        Returns:
            dict: The result from the tool, or None if an error occurs.
        """
        try:
            payload = {"tool": tool_name, "args": kwargs}
            response = requests.post(f"{self.mcp_self.mcp_server_url}/use", json=payload, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error using tool {tool_name} on {self.mcp_server_url}: {e}")
            return None
