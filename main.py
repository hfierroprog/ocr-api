from fastapi import FastAPI, File
from pydantic import BaseModel
from PIL import Image
from io import BytesIO
import numpy as np
import cv2
import string
import random
import pytesseract


class ImageRQ(BaseModel):
    name: str
    base64: str


app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}


@app.post("/ocr")
async def ocr_image(file: bytes = File()):
    image = Image.open(BytesIO(file))
    # Converting image to array
    image_arr = np.array(image.convert('RGB'))
    # Converting image to grayscale
    gray_img_arr = cv2.cvtColor(image_arr, cv2.COLOR_BGR2GRAY)
    # Converting image back to rbg
    image = Image.fromarray(gray_img_arr)

    # Printing lowercase
    letters = string.ascii_lowercase
    # Generating unique image name for dynamic image display
    #name = ''.join(random.choice(letters) for i in range(10)) + '.png'
    #full_filename = 'uploads/' + name

    # Extracting text from image
    custom_config = r'-l eng --oem 3 --psm 6'
    text = pytesseract.image_to_string(image, config=custom_config)

    # Remove symbol if any
    characters_to_remove = "!()@*“>+-/,'|£#%$&^_~"
    new_string = text
    for character in characters_to_remove:
        new_string = new_string.replace(character, "")

    # Converting string into list to dislay extracted text in seperate line
    new_string = new_string.split("\n")

    return {'status': 'OK', 'result_string': new_string}
