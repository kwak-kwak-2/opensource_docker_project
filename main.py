import os
import io
import random
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from PIL import Image

# 1. API 문서 최적화 (산업경영공학 품질 관리 관점 명시)
app = FastAPI(
    title="Smart Factory Quality Control API",
    description=("산업경영공학 관점의 생산 공정 품질 관리(Quality Control) 서비스입니다. "
                 "제조 공정 중 업로드된 부품 이미지를 바탕으로, AI 모델이 스크래치, 파손, 오염 등의 "
                 "불량 여부 및 결함 유형을 예측하는(Mock-up) API를 제공합니다.")
)

# 검사 완료된 이미지를 저장할 디렉토리 생성
OUTPUT_DIR = "output"
os.makedirs(OUTPUT_DIR, exist_ok=True)

@app.post("/analyze-defect/")
async def analyze_defect(file: UploadFile = File(...)):
    try:
        # 파일 내용을 바이트로 읽기
        contents = await file.read()
        file_size_bytes = len(contents)
        
        # 모델 추론 전처리 등 실제 AI 파이프라인처럼 작동하도록 Pillow로 이미지 검증
        img = Image.open(io.BytesIO(contents))
        orig_width, orig_height = img.size
        
        # 입력된 부품 이미지 로컬 저장 (분석 이력용)
        save_path = os.path.join(OUTPUT_DIR, f"inspected_{file.filename}")
        img.save(save_path)

        # ---------------------------------------------------------
        # 2. AI-driven Defect Detection Mock-up 로직 (실제 모델 대체)
        # ---------------------------------------------------------
        
        # 30% 확률로 불량(True), 70% 확률로 정상(False) 판정
        is_defective = random.random() < 0.30
        
        # 모델의 예측 신뢰도 (75% ~ 99% 사이 난수)
        confidence_score = round(random.uniform(0.75, 0.99), 4)

        if is_defective:
            # 불량일 경우 구체적 결함 유형을 판별
            defect_type = random.choice(["스크래치", "파손", "오염", "찍힘", "도장 불량"])
        else:
            # 정상일 경우 결함 없음
            defect_type = "정상"

        # 3. 깔끔한 JSON 형태의 분석 결과 반환
        return JSONResponse(content={
            "filename": file.filename,
            "resolution": f"{orig_width}x{orig_height}",
            "file_size_bytes": file_size_bytes,
            "analysis_result": {
                "is_defective": is_defective,
                "confidence_score": confidence_score,
                "defect_type": defect_type,
            },
            "saved_path": save_path,
            "message": "부품 품질 검사가 성공적으로 완료되었습니다."
        })
        
    except Exception as e:
        return JSONResponse(status_code=400, content={"error": f"Image processing failed: {str(e)}"})

@app.get("/")
def read_root():
    return {
        "message": "Smart Factory Quality Control API is running.",
        "endpoint": "Send a POST request with an image to /analyze-defect/"
    }
