from typing import Union
from fastapi import FastAPI, status, File, UploadFile, Request, WebSocket, WebSocketDisconnect
from fastapi.staticfiles import StaticFiles
from .line.urls import line_app
from .ai.classification import predict, read_imagefile
import cv2
import sys
import os
import uvicorn
# Python version
version = f"{sys.version_info.major}.{sys.version_info.minor}"

# from tortoise.contrib.fastapi import register_tortoise
from fastapi.middleware.cors import CORSMiddleware
# from fastapi.encoders import jsonable_encoder
# from fastapi.responses import JSONResponse

# from .models import Student
# from .serializers import StudentIn_Pydantic, StudentOut_Pydantic

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# register_tortoise(
#     app,
#     db_url='sqlite://db.sqlite3',
#     modules={'models': ['app.main']},
#     generate_schemas=True,
#     add_exception_handlers=True
# )

# LINE Bot
app.include_router(line_app)

@app.get("/")
async def read_root():
    message = f"Hello world! From FastAPI running on Uvicorn with Gunicorn. Using Python {version}"
    return {"message": message}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}

@app.post("/predict/image")
async def predict_api(file: UploadFile = File(...)):
    extension = file.filename.split(".")[-1] in ("jpg", "jpeg", "png")
    if not extension:
        return "圖片請用 jpg、jpeg 或 png 格式!"
    image = read_imagefile(await file.read())
    prediction = predict(image)

    return prediction


# camera = cv2.VideoCapture(0, cv2.CAP_DSHOW)
camera = cv2.VideoCapture(0)

@app.websocket("/ws")
async def get_stream(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            success, frame = camera.read()
            if not success:
                break
            else:
                ret, buffer = cv2.imencode('.jpg', frame)
                await websocket.send_text("some text")
                await websocket.send_bytes(buffer.tobytes())
    except WebSocketDisconnect:
        print("Client disconnected")   

# from fastapi.responses import StreamingResponse
# def gen_frames():
#     while True:
#         success, frame = camera.read()
#         if not success:
#             print("fail")
#             break
#         else:
#             ret, buffer = cv2.imencode('.jpg', frame)
#             frame = buffer.tobytes()
#             yield (b'--frame\r\n'
#                    b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

# @app.get('/video_feed')
# def video_feed():
#     return StreamingResponse(gen_frames(), media_type='multipart/x-mixed-replace; boundary=frame')

# from fastapi.templating import Jinja2Templates
# templates = Jinja2Templates(directory="templates")

# @app.get('/v')
# def index(request: Request):
#     return templates.TemplateResponse("index.html", {"request": request})


# @app.post('/api/v1/add-student/')
# async def add_student(student: StudentOut_Pydantic):
#     stu_obj = Student(
#         name=student.name,
#         email=student.email,
#         address=student.address
#     )
#     await stu_obj.save()
#     student = await StudentIn_Pydantic.from_tortoise_orm(stu_obj)
#     json_data = jsonable_encoder(student)
#     return JSONResponse(
#         status_code=status.HTTP_201_CREATED,
#         content=json_data
#     )

# @app.get('/api/v1/student-list/')
# async def student_list():
#     students = await Student.all()
#     # return students
#     json_data = jsonable_encoder(students)
#     return JSONResponse(
#         status_code=status.HTTP_201_CREATED,
#         content=json_data
#     )

# @app.get('/api/v1/student-details/{id}')
# async def student_details(id: int):
#     student = await Student.get(id=id)
#     json_data = jsonable_encoder(student)
#     return JSONResponse(
#         status_code=status.HTTP_201_CREATED,
#         content=json_data
#     )

# @app.delete('/api/v1/delete-student/{id}')
# async def delete_student(id: int):
#     student = await Student.get(id=id)
#     await student.delete()
#     return {'details': "deleted"}

# @app.put('/api/v1/student-update/{id}')
# async def update_student(id: int, stu_info: StudentOut_Pydantic):
#     student = await Student.get(id=id)
#     student.name = stu_info.name
#     student.email = stu_info.email
#     student.address = stu_info.address
#     await student.save()
#     student = await StudentIn_Pydantic.from_tortoise_orm(student)
#     json_data = jsonable_encoder(student)
#     return JSONResponse(
#         status_code=status.HTTP_201_CREATED,
#         content=json_data
#     )

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))