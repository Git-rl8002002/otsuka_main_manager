import asyncio
import websockets

async def handle_client(websocket, path):
    # 当有新的 WebSocket 连接时，执行这个回调函数
    print(f"新的 WebSocket 连接：{websocket.remote_address}")

    try:
        while True:
            # 接收客户端发送的消息
            message = await websocket.recv()
            print(f"接收到消息：{message}")

            # 发送消息给客户端
            response = f"收到了你的消息：{message}"
            await websocket.send(response)

    except websockets.exceptions.ConnectionClosedError:
        print(f"WebSocket 连接关闭：{websocket.remote_address}")

# 启动 WebSocket 服务器
start_server = websockets.serve(handle_client, "localhost", 8765)

# 进入事件循环，保持服务器运行
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()