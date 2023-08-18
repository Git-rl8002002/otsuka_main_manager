import asyncio
import websockets

async def receive_messages():
    uri = "ws://127.0.0.1:8765"
    async with websockets.connect(uri) as websocket:
        while True:
            message = await websocket.recv()
            print(f"收到消息：{message}")

async def send_message():
    uri = "ws://127.0.0.1:8765"
    async with websockets.connect(uri) as websocket:
        while True:
            message = input("输入消息：")
            await websocket.send(message)

async def main():
    await asyncio.gather(receive_messages(), send_message())

if __name__ == "__main__":
    asyncio.run(main())