# Binance Websocket API
import asyncio
import logging

from service.binance.websocket.ws_futures import FuturesUserDataStream

async def main():
    try:
        user_data_stream = FuturesUserDataStream()
        tasks = [
            asyncio.create_task(user_data_stream.main())
        ]
        done, pending = await asyncio.wait(tasks)
    except KeyboardInterrupt:
        logging.info("Websocket server stopped")
    finally:
        pass


if __name__ == '__main__':
    asyncio.run(main())
    logging.info("Websocket server started")
