import io
import re
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from PIL import ImageOps, Image
import pytesseract
from extract_details import get_age, get_license_number, get_name, get_validity

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

    return JSONResponse(content={
        "name": get_name(clean_text),
        "age": get_age(clean_text),
        "license_number": get_license_number(clean_text),
        "validity": get_validity(clean_text),
    })
