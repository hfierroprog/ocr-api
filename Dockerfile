FROM python:3.9 
EXPOSE 8000
# Or any preferred Python version.
ADD main.py requirements.txt ./
RUN apt-get update
RUN apt-get install ffmpeg libsm6 libxext6 tesseract-ocr -y
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
CMD ["uvicorn", "--host=0.0.0.0", "main:app"] 
# Or enter the name of your unique directory and parameter set.
