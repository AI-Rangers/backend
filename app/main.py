from typing import Union
from fastapi import FastAPI, status, File, UploadFile, Request, WebSocket, WebSocketDisconnect
from fastapi.staticfiles import StaticFiles
from .line.urls import line_app
from .ai.classification import predict, read_imagefile
from .ai.styletransfer import styleTransfer
from .ai.circlegan import style_transfer

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

# if os.getenv('API_ENV') == 'production':
#     # from werkzeug.contrib.fixers import ProxyFix
#     from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware
#     app.add_middleware(HTTPSRedirectMiddleware)

app.mount("/static", StaticFiles(directory="static"), name="static")

origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
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

origin_img_folder = "static/origin/"
styled_img_folder = "static/styled/"

# circlegan api 本機可以跑，部署上去跑會出現錯誤
@app.get("/circlegan/{img_name}")
def get_circlegan_image(img_name: str):
    raw_image_path = f"{origin_img_folder}{img_name}"
    transfered_image_path = f"{styled_img_folder}transfered_{img_name}"

    style_image = style_transfer(raw_image_path)
    style_image_path = transfered_image_path
    style_image.save(style_image_path)

    return {
        "folder": styled_img_folder,
        "file": f"transfered_{img_name}",
        "path": style_image_path
    }
    # {
    # "folder": "static/styled/",
    # "file": "transfered_sample.jpg",
    # "path": "static/styled/transfered_sample.jpg"
    # }


@app.get("/img/{img_name}/style/{selected_style}")
def get_processed_image(img_name: str, selected_style: str):
    # if description:
    #     book_detail.update({"book_description": "This is the description"})
    # styleTransfer("/content/", "Cat03.jpg", "pink_style_1800.t7")
    processed_image = styleTransfer(origin_img_folder, styled_img_folder, img_name, selected_style)
    return {
        "folder": styled_img_folder,
        "file": processed_image,
        "path": f"{styled_img_folder}{processed_image}"
    }
    # {
    #   "folder": "static/styled/",
    #   "file": "processedImg_00b79136-cb64-4f7f-990e-addfbcc342f3.jpg",
    #   "path": "static/styled/processedImg_00b79136-cb64-4f7f-990e-addfbcc342f3.jpg"
    # }

@app.post("/uploadfile/")
async def create_upload_file(
    uploaded_file: UploadFile = File(description="A file read as UploadFile"),
):
    extension = uploaded_file.filename.split(".")[-1] in ("jpg", "jpeg", "png")
    if not extension:
        return "圖片請用 jpg、jpeg 或 png 格式!"
    try:
        contents = uploaded_file.file.read()
        file_location = f"{origin_img_folder}{uploaded_file.filename}"
        with open(file_location, "wb+") as file_object:
            file_object.write(contents)
    except Exception:
        return {"message": "There was an error uploading the file"}
    finally:
        uploaded_file.file.close()
    # return {"message": f"Successfully uploaded {file.filename}"}
    return {
        # "info": f"file '{uploaded_file.filename}' saved at '{file_location}'",
        "folder": origin_img_folder,
        "file": uploaded_file.filename,
        "path": file_location
    }
    # {
    #   "folder": "static/origin/",
    #   "file": "00b79136-cb64-4f7f-990e-addfbcc342f3.jpg",
    #   "path": "static/origin/00b79136-cb64-4f7f-990e-addfbcc342f3.jpg"
    # }







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

from fastapi.responses import StreamingResponse
def gen_frames():
    while True:
        success, frame = camera.read()
        if not success:
            print("fail")
            break
        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.get('/video_feed')
def video_feed():
    return StreamingResponse(gen_frames(), media_type='multipart/x-mixed-replace; boundary=frame')

from fastapi.templating import Jinja2Templates
templates = Jinja2Templates(directory="templates")

def https_url_for(request: Request, name: str, **path_params: any) -> str:
    http_url = request.url_for(name, **path_params)
    # Replace 'http' with 'https'
    return http_url.replace("http", "https", 1)
templates.env.globals["https_url_for"] = https_url_for

@app.get('/v')
def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


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