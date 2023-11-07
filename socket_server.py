import asyncio
import os
import aioredis

class SocketServer:
    def __init__(self, host, port, redis_host, redis_port):
        self.host = host
        self.port = port
        self.redis_host = redis_host
        self.redis_port = redis_port

    async def handle_client(self, reader, writer):
        print("Handling client connection...")
        data = await reader.read(100)
        print(f"Received data of length: {len(data)} bytes")  # Changed this line

        # Store raw data in Redis
        await self.store_in_redis(data)

        # Send acknowledgment to client
        writer.write(b"Data stored in Redis")
        await writer.drain()
        writer.close()
        await writer.wait_closed()

    async def store_in_redis(self, data):
        redis = await aioredis.create_redis((self.redis_host, self.redis_port))
        await redis.lpush('data_queue', data)
        redis.close()
        await redis.wait_closed()

    async def run(self):
        server = await asyncio.start_server(
            self.handle_client, self.host, self.port
        )
        print(f"Server started on {self.host}:{self.port}")
        async with server:
            await server.serve_forever()

def main():
    HOST = os.getenv('HOST', '0.0.0.0')
    PORT = int(os.getenv('PORT', 8089))
    REDIS_HOST = os.getenv('REDIS_HOST', 'localhost')
    REDIS_PORT = int(os.getenv('REDIS_PORT', 6379))

    server = SocketServer(HOST, PORT, REDIS_HOST, REDIS_PORT)
    asyncio.run(server.run())

if __name__ == "__main__":
    main()
