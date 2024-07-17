import os
from fastapi import UploadFile
from backend.core.config import settings


def save_profile(user_id: int, file: UploadFile):
    """
    save image profile in file in project
    @param user_id: user id
    @param file: file to save
    @return: saved profile
    """
    _, ext = os.path.splitext(file.filename)  # result -> _:filename /ext:.formatfile
    save_name = f"{settings.STATIC_DIR}/images/users/{user_id}{ext}"  # result ->  static/images/users/<user_id>.formatfile
    with open(save_name, "wb") as image:  # result -> bufferdwriter(object) with save_name
        image.write(file.file.read())

    return save_name
