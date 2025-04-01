# server.py
from mcp.server.fastmcp import FastMCP
import urllib.request

remote_server = "192.168.1.7:5000"

# Create an MCP server
mcp = FastMCP("Demo")

# Add an addition tool
@mcp.tool()
def add(a: int, b: int) -> int:
    """Add two numbers"""
    return a + b

@mcp.tool()
def light_switch(on: bool):
    """Turn on or turn off the light"""
    try:
        if on:
            urllib.request.urlopen("http://" + remote_server + "/led/on")
            return {"status": "The light is turned on"}
        else:
            urllib.request.urlopen("http://" + remote_server + "/led/off")
            return {"status": "The light is turned off"}
    except Exception as e:
        return {"status": "error", "message": str(e)}

@mcp.tool()
def query_cpu_temperature():
    """Query temperature of the CPU in degree celsius"""
    try:
        with urllib.request.urlopen("http://" + remote_server + "/cpu/temperature") as res:
            return res.read()
    except Exception as e:
        return {"status": "error", "message": str(e)}

# Add a dynamic greeting resource
@mcp.resource("greeting://{name}")
def get_greeting(name: str) -> str:
    """Get a personalized greeting"""
    return f"Hello, {name}!"