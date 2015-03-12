import asyncio


def main():
    loop = asyncio.get_event_loop()
    try:
        loop.run_forever()
    finally:
        loop.close()
