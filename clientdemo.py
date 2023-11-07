import asyncio
import os

class SocketClient:
    def __init__(self, host, port):
        self.host = host
        self.port = port

    async def send_data(self, data):
        reader, writer = await asyncio.open_connection(self.host, self.port)
        
        print(f"Sending data: {data}")
        writer.write(data.encode())

        received_data = await reader.read(100)
        print(f"Received: {received_data.decode()}")

        writer.close()
        await writer.wait_closed()

def main():
    HOST = os.getenv('SERVER_HOST', '127.0.0.1')
    PORT = int(os.getenv('SERVER_PORT', 8089))
    RAW_DATA = "436c69656e745f312c204c617469747564653d31392e3638333937302c204c6f6e6769747564653d37382e373531323734"

    client = SocketClient(HOST, PORT)
    asyncio.run(client.send_data(RAW_DATA))

if __name__ == "__main__":
    main()
