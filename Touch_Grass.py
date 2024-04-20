# @File     :Touch_Grass.py
# @Software :Vscode

import asyncio
import random
import ssl
import json
import time
import uuid
import os
from loguru import logger
from websockets_proxy import Proxy, proxy_connect
from fake_useragent import UserAgent

user_agent = UserAgent().random

async def connect_to_wss(socks5_proxy, user_id):
    device_id = str(uuid.uuid3(uuid.NAMESPACE_DNS, user_id + socks5_proxy))
    logger.info(device_id)
    while True:
        try:
            await asyncio.sleep(random.randint(1, 10) / 10)
            custom_headers = {
                "User-Agent": user_agent 
            }
            ssl_context = ssl.create_default_context()
            ssl_context.check_hostname = False
            ssl_context.verify_mode = ssl.CERT_NONE
            # main uri
            # uri = "wss://proxy.wynd.network:4650/"

            # # # backup (fallback) uri
            uri = "wss://proxy.wynd.network:4444/"

            #  # # backup (fallback) uri
            # uri = "wss://proxy.dev.getgrass.io:4343"

            server_hostname = "proxy.wynd.network"
            proxy = Proxy.from_url(socks5_proxy)
            async with proxy_connect(
                uri,
                proxy=proxy,
                ssl=ssl_context,
                server_hostname=server_hostname,
                extra_headers=custom_headers,
            ) as websocket:

                async def send_ping():
                    while True:
                        send_message = json.dumps(
                            {
                                "id": str(uuid.uuid4()),
                                "version": "1.0.0",
                                "action": "PING",
                                "data": {},
                            }
                        )
                        logger.debug(send_message)
                        await websocket.send(send_message)
                        await asyncio.sleep(20)

                # asyncio.create_task(send_http_request_every_10_seconds(socks5_proxy, device_id))
                await asyncio.sleep(1)
                asyncio.create_task(send_ping())

                while True:
                    response = await websocket.recv()
                    message = json.loads(response)
                    logger.info(message)
                    if message.get("action") == "AUTH":
                        auth_response = {
                            "id": message["id"],
                            "origin_action": "AUTH",
                            "result": {
                                "browser_id": device_id,
                                "user_id": user_id,
                                "user_agent": custom_headers["User-Agent"],
                                "timestamp": int(time.time()),
                                "device_type": "extension",
                                "version": "4.0.0",
                            },
                        }
                        logger.debug(auth_response)
                        await websocket.send(json.dumps(auth_response))

                    elif message.get("action") == "PONG":
                        pong_response = {"id": message["id"], "origin_action": "PONG"}
                        logger.debug(pong_response)
                        await websocket.send(json.dumps(pong_response))
        except Exception as e:
            # enable logging
            # logger.add("logs.log", level="ERROR")
            logger.error(e)
            logger.error(socks5_proxy)

async def main():
    # Get the directory of the script
    script_dir = os.path.dirname(os.path.abspath(__file__))

    # Load User_id from file
    user_id_path = os.path.join(script_dir, "user_id.txt")
    with open(user_id_path, "r") as user_id_file:
        user_id = user_id_file.read().strip()

    # Load Socks Proxies file
    socks5_proxies_path = os.path.join(script_dir, "socks5_proxies.txt")
    with open(socks5_proxies_path, "r") as f:
        socks5_proxy_list = [line.strip() for line in f]
    tasks = [
        asyncio.ensure_future(connect_to_wss(i, user_id)) for i in socks5_proxy_list
    ]
    await asyncio.gather(*tasks)

if __name__ == "__main__":
    logger.add("touch_grass.log", rotation="10 MB", retention=0, level="DEBUG")
    # Run the Touch Grass function
    asyncio.run(main())