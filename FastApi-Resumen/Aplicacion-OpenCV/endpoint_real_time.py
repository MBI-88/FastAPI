import asyncio
from typing import List, Tuple
import cv2
import numpy as np
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from pydantic import BaseModel
import uvicorn

app = FastAPI()
cascade_classifier = cv2.CascadeClassifier()


class Faces(BaseModel):
    faces: List[Tuple[int, int, int, int]]


async def recive(websocket: WebSocket, queue: asyncio.Queue) -> None:
    bytes = await websocket.receive_bytes()
    try:
        queue.put_nowait(bytes)
    except asyncio.QueueFull:
        pass


async def detect(websocket: WebSocket, queue: asyncio.Queue) -> None:
    while True:
        bytes = await queue.get()
        data = np.frombuffer(bytes, dtype=np.uint8)
        img = cv2.imdecode(data, 1)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = cascade_classifier.detectMultiScale(gray)
        if len(faces) > 0:
            faces_output = Faces(faces=faces.tolist())
        else:
            faces_output = Faces(faces=[])

        await websocket.send_json(faces_output.dict())


@app.websocket("/face-detection")
async def face_detection(websocket: WebSocket) -> None:
    await websocket.accept()
    queue: asyncio.Queue = asyncio.Queue(maxsize=10)
    detect_task = asyncio.create_task(detect(websocket, queue))
    try:
        while True:
            await recive(websocket, queue)
    except WebSocketDisconnect:
        detect_task.cancel()
        await websocket.close()


@app.on_event('startup')
async def startup() -> None:
    cascade_classifier.load(
        cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
    )


if __name__ == '__main__':
    uvicorn.run('endpoint_real_time:app', port=8000, reload=True)
