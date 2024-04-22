from fastapi import APIRouter, UploadFile
import os
from infra.file import save_file, send_file
import models.file as FileModel

router = APIRouter(
    prefix="/file",
)


@router.post("/upload")
async def upload_video(
    file: UploadFile,
    model_id: int,
):
    user_id = 1  # get user id from token
    model_path = "user-key/model"  # get model path by model
    raw_path = f"{model_path}/raw"
    path = os.path.join(raw_path, file.filename)

    await save_file(file, path)
    return await FileModel.create_file(path, user_id)


@router.get("/download")
async def download(file_id: int):
    user_id = 1  # get user id from token
    res = await FileModel.query_file(file_id)
    if not res:
        return {"message": "file not found"}

    if res.user_id != user_id:
        return {"message": "no permission"}

    return await send_file(res.path)
