import asyncio
import logging
import queue
import json
from datetime import datetime
from websockets import server


class WebSocketServer:

    def __init__(self, host='localhost', port=28765):
        logging.basicConfig(level=logging.INFO)
        self.__connected_clients = set()
        self.__queue = queue.Queue()
        self.host = host
        self.port = port


    # message braodcast
    async def __queue_handling(self):
        while True:
            # logging.info(f"__queue_handling started")
            if not self.__queue.empty():
                message = self.__queue.get()
                logging.info(f"Received messages in queue: {message}")
                if type(message) is not str:
                    message = str(message)
                if self.__connected_clients:   
                    await asyncio.wait([client.send(message) for client in self.__connected_clients])

            # check queue every 0.3 second
            await asyncio.sleep(0.3)    
        

    # server time
    async def __server_time(self):
        while True:
            res = {
                "eventType": "SERVER_TIME",
                "eventTime": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "serverTime": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            }
            self.broadcast(json.dumps(res, indent=4));
            await asyncio.sleep(10)


    # client handling
    async def __client_handling(self, websocket, path):
        logging.info(f"Client connected from: {websocket.remote_address}")
        client_ip, _ = websocket.remote_address
        self.__connected_clients.add(websocket)
        try: 
            async for message in websocket:
                logging.info(f"Received message from {client_ip}: {message}")
                await websocket.send(f"Hello! I've received your message from {client_ip}: {message}")
        except Exception as e:
            logging.error(e)
        finally:
            logging.info(f"Client disconnected")
            self.__connected_clients.remove(websocket)


    async def __start_server(self):
        # no Future task will be completed so that it will run forever
        # async with server.serve(self.__client_handling, host=self.host, port=self.port) as websocket:
        async with server.serve(self.__client_handling, port=self.port) as websocket:
            await asyncio.Future()      


    # broadcast message
    def broadcast(self, msg):
        self.__queue.put(msg)


    # tasks
    async def main(self):
        task_list = [
            asyncio.create_task(self.__start_server(), name='start_server'),
            asyncio.create_task(self.__server_time(),  name='server_time'),
            asyncio.create_task(self.__queue_handling(), name='queue_handling'),
        ]
        done, pending = await asyncio.wait(task_list)
        logging.info(f"done: {done}")
        return done, pending


    def start(self):
        try:
            logging.info(f"server is up at ws://{self.host}:{self.port}")
            asyncio.run(self.main())   # run forever
        except KeyboardInterrupt:
            logging.info(f"server is down at ws://{self.host}:{self.port}")
        except Exception as e:
            logging.error(e)
        finally:
            logging.info(f"server is down at ws://{self.host}:{self.port}")

