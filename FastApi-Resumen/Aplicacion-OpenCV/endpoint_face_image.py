from typing import List, Tuple
import cv2
import numpy as np
from fastapi import FastAPI, File, UploadFile
from pydantic import BaseModel
import uvicorn


app = FastAPI()
cascade_clasifier = cv2.CascadeClassifier()


class Faces(BaseModel):
    faces: List[Tuple[int, int, int, int]]


@app.post("/face-detection", response_model=Faces)
async def face_detection(image: UploadFile = File(...)) -> Faces:
    data = np.fromfile(image.file, dtype=np.uint8)
    image = cv2.imdecode(data, cv2.IMREAD_UNCHANGED)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    faces = cascade_clasifier.detectMultiScale(gray)
    if len(faces) > 0:
        faces_output = Faces(faces=faces.tolist())
    else:
        faces_output = Faces(faces=[])
    return faces_output


@app.on_event('startup')
async def startup() -> None:
    cascade_clasifier.load(
        cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
    )


if __name__ == '__main__':
    uvicorn.run('endpoint_face_image:app', port=8000, reload=True)
