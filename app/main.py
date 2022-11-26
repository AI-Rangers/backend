from typing import Union
from fastapi import FastAPI, status
import sys
# Python version
version = f"{sys.version_info.major}.{sys.version_info.minor}"

import os
if os.getenv('API_ENV') != 'production':
    from dotenv import load_dotenv
    load_dotenv()

LINE_CHANNEL_ACCESS_TOKEN = os.getenv('LINE_CHANNEL_ACCESS_TOKEN')
LINE_CHANNEL_SECRET = os.getenv('LINE_CHANNEL_SECRET')
AAA = os.getenv('AAA')
LO = os.getenv('location')


print("ACCESS_TOKEN : ",LINE_CHANNEL_ACCESS_TOKEN)
print("CHANNEL_SECRET : ",LINE_CHANNEL_SECRET)

# from tortoise.contrib.fastapi import register_tortoise
# from fastapi.middleware.cors import CORSMiddleware
# from fastapi.encoders import jsonable_encoder
# from fastapi.responses import JSONResponse

# from .models import Student
# from .serializers import StudentIn_Pydantic, StudentOut_Pydantic


app = FastAPI()

# origins = ["*"]
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=origins,
#     allow_credentials=False,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )
# register_tortoise(
#     app,
#     db_url='sqlite://db.sqlite3',
#     modules={'models': ['app.main']},
#     generate_schemas=True,
#     add_exception_handlers=True
# )

@app.get("/env")
def read_env():
    return {"ACCESS_TOKEN": LINE_CHANNEL_ACCESS_TOKEN,
            "LINE_CHANNEL_SECRET": LINE_CHANNEL_SECRET,
            "AAA": AAA,
            "location": LO }

@app.get("/")
async def read_root():
    message = f"Hello world! From FastAPI running on Uvicorn with Gunicorn. Using Python {version}"
    return {"message": message}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}

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
