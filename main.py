from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from PIL import ImageOps, Image
import pytesseract
import io
import re
from datetime import datetime

app = FastAPI()


@app.get("/")
def root():
    return {"message": "Driving License reader API is running"}


@app.post("/upload")
async def upload_image(file: UploadFile = File(...)):
    if file.content_type not in ("image/jpeg", "image/jpg", "image/png"):
        raise HTTPException(
            status_code=400, detail="Only image files are supported")

    contents = await file.read()
    image = Image.open(io.BytesIO(contents))

    image = image.resize((image.width * 2, image.height * 2))
    gray = ImageOps.grayscale(image)
    gray = ImageOps.autocontrast(gray)

    config = "--oem 3 --psm 6 -l eng"
    text = pytesseract.image_to_string(gray, config=config)
    clean_text = re.sub(r'[^A-Za-z0-9-\s]', '', text)

    name = get_name(clean_text)
    age = get_age(clean_text)
    return JSONResponse(content={
        "name": name,
        "age": age
    })


def get_name(text: str):
    match = re.search(r"Name\s+(.*)", text)
    return match.group(1)


def get_age(text: str):
    match = re.search(r"DOB\s+(\d{2}-\d{2}-\d{4})", text)
    dob = datetime.strptime(match.group(1), "%d-%m-%Y").date()
    today = datetime.today().date()
    return today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
