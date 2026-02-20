from server import server
from adapter.dooray import DoorayApiTokenContainer
from utils import pyloader
import argparse
import anyio
import os

TOKEN=None
parser = argparse.ArgumentParser()

def main():
    if TOKEN is None or TOKEN == '':
        raise DoorayApiTokenContainer.TokenNotAvailableException

    DoorayApiTokenContainer(TOKEN)
    pyloader.import_all_modules_from("adapter")
    pyloader.import_all_modules_from("context")

    from mcp.server.stdio import stdio_server

    async def async_run():
        async with stdio_server() as streams:
            await server.run(streams[0], streams[1], server.create_initialization_options())

    anyio.run(async_run)

if __name__ == "__main__":
    TOKEN = os.environ.get('DOORAY_API_KEY') or os.environ.get('DOORAY_API_TOKEN')
    if TOKEN is None or TOKEN == '':
        raise DoorayApiTokenContainer.TokenNotAvailableException
    main()
