import os
import io
import random
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from PIL import Image

app = FastAPI(title="MLOps Image Analysis API", description="가벼운 이미지 분석, 리사이징 및 성별 식별(Mock-up) API")

# 리사이징된 이미지를 저장할 디렉토리 생성
OUTPUT_DIR = "output"
os.makedirs(OUTPUT_DIR, exist_ok=True)

@app.post("/analyze-image/")
async def analyze_and_resize_image(file: UploadFile = File(...)):
    try:
        # 파일 내용을 바이트로 읽기
        contents = await file.read()
        file_size_bytes = len(contents)
        
        # Pillow를 이용하여 이미지 열기
        img = Image.open(io.BytesIO(contents))
        orig_width, orig_height = img.size
        
        # 224x224 모델 학습용 크기로 리사이징
        resized_img = img.resize((224, 224))
        
        # 리사이징된 이미지 로컬 저장 (옵션)
        save_path = os.path.join(OUTPUT_DIR, f"resized_{file.filename}")
        resized_img.save(save_path)

        # 성별 식별 모델 Mock-up 로직 (실제 모델이 들어갈 자리)
        # 50% 확률로 Male 또는 Female 반환
        predicted_gender = random.choice(["Male", "Female"])
        
        return JSONResponse(content={
            "filename": file.filename,
            "file_size_bytes": file_size_bytes,
            "original_resolution": f"{orig_width}x{orig_height}",
            "resized_resolution": "224x224",
            "gender": predicted_gender,
            "saved_path": save_path,
            "message": "이미지가 성공적으로 분석되고 리사이징 되었습니다."
        })
        
    except Exception as e:
        return JSONResponse(status_code=400, content={"error": f"Image processing failed: {str(e)}"})

@app.get("/")
def read_root():
    return {"message": "MLOps Image API Server is running. Send a POST request with an image to /analyze-image/"}
