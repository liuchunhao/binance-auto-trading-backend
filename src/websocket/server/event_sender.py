import asyncio
import logging
import queue

from websockets import server

WEBSOCKET_HOST = "0.0.0.0"
WEBSOCKET_PORT = 18765

logging.basicConfig(level=logging.INFO)

__queue = queue.Queue()

connected_clients = set()


def publish(msg):
    __queue.put(msg)


# queue handling
async def __queue_handling():
    while True:
        if not __queue.empty():
            message = __queue.get()
            logging.info(f"Received messages in queue: {message}")
            if connected_clients:   # if there are connected clients
                await asyncio.wait([client.send(message) for client in connected_clients])
        # await asyncio.sleep(1)    # check queue every 1 second
    

# client handling
async def __client_handling(websocket, path):
    client_ip, _ = websocket.remote_address
    connected_clients.add(websocket)
    try: 
        async for message in websocket:
            logging.info(f"Received message from {client_ip}: {message}")
            await websocket.send(f"Hello! I've received your message from {client_ip}: {message}")
    except Exception as e:
        logging.error(e)
    finally:
        logging.info(f"Client disconnected")
        connected_clients.remove(websocket)


async def main():
    async with server.serve(__client_handling, host=WEBSOCKET_HOST, port=WEBSOCKET_PORT) as websocket:
        # no Future task will be completed so that it will run forever
        await asyncio.Future()          


def start():
    logging.info(f"Websocket server starting at ws://{WEBSOCKET_HOST}:{WEBSOCKET_PORT}")
    asyncio.get_event_loop().create_task(__queue_handling())
    asyncio.run(main())
    logging.info(f"Websocket server started at ws://{WEBSOCKET_HOST}:{WEBSOCKET_PORT}")
