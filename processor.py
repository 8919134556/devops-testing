import asyncio
import aioredis
import os

def hex_to_string(hex_string):
    try:
        return bytes.fromhex(hex_string).decode('utf-8')
    except Exception as e:
        print(f"Error converting hex to string: {e}")
        return None

async def process_redis_data(redis_host, redis_port):
    redis = await aioredis.create_redis_pool((redis_host, redis_port))
    
    while True:
        _, data = await redis.brpop('data_queue')
        if data:
            processed_data = hex_to_string(data.decode())
            if processed_data:
                print(f"Processed Data: {processed_data}")
                # Any further processing or handling of the data can be added here.
            else:
                print(f"Failed to process data: {data.decode()}")
        await asyncio.sleep(1)

    redis.close()
    await redis.wait_closed()

if __name__ == "__main__":
    REDIS_HOST = os.getenv('REDIS_HOST', 'localhost')
    REDIS_PORT = int(os.getenv('REDIS_PORT', 6379))

    try:
        asyncio.run(process_redis_data(REDIS_HOST, REDIS_PORT))
    except KeyboardInterrupt:
        pass
