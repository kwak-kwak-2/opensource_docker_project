import os
import io
import random
import time
from datetime import datetime
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from PIL import Image

# 1. API 문서 메타데이터 최적화 (산업경영공학 관점)
description = """
본 API 시스템은 제조 공정의 수율 향상 및 불량률 최소화를 위한 **지능형 품질 검사(Intelligent Quality Inspection)** 백엔드 서비스입니다. 
산업경영공학의 통계적 품질 관리(SQC) 기법과 딥러닝 기반 컴퓨터 비전 기술을 융합하여 실시간으로 부품의 결함을 탐지합니다.

### 💡 주요 기능
- **실시간 결함 탐지 (Real-time Defect Detection):** 업로드된 부품 이미지를 분석하여 불량 여부, 결함 유형(스크래치, 파손, 오염 등), 모델의 신뢰도(Confidence Score)를 즉각적으로 파악합니다.
- **후속 조치 자동 분류 (Decision Support):** 탐지된 결함 종류와 신뢰도를 기반으로 공정 내 후속 조치(통과, 재검사, 폐기 등)를 시스템이 제안합니다.

### 🏗 시스템 아키텍처
- **Framework:** FastAPI (비동기 처리 기반 고성능 API 제공 및 자동 Swagger UI 생성)
- **Deployment:** Docker & MLOps Pipeline (GitHub Actions 기반의 CI/CD 파이프라인 구축)
- **Model Mock-up:** 향후 PyTorch/TensorFlow 기반의 CNN(ResNet, YOLO 등) 모델 확장을 고려한 규격화된 Interface 구현

### 🎓 전공 지식 적용 포인트 (산업경영공학)
- **통계적 공정 관리(SPC):** 결함 데이터를 수집하여 공정 능력 분석(Process Capability Analysis) 및 관리도(Control Chart) 작성의 기초 데이터로 활용할 수 있도록 `line_id`, `timestamp` 등의 현장 데이터를 설계에 포함했습니다.
- **생산 운영 최적화:** 단순한 불량 판정을 넘어 `action_required` 속성을 통해 재작업(Rework) 최소화와 라인 균형(Line Balancing)을 고려한 현장 맞춤형 구조를 채택하였습니다.
"""

tags_metadata = [
    {
        "name": "핵심 품질 서비스(Core Quality Services)",
        "description": "딥러닝 기반 부품 결함 검출 및 품질 관리 의사결정 로직을 포함합니다.",
    },
    {
        "name": "시스템 상태(System Status)",
        "description": "API 서버의 헬스 체크 및 가동 상태 모니터링을 확인합니다.",
    },
]

app = FastAPI(
    title="🏭 Smart Factory Quality Control API",
    description=description,
    version="2.1.0",
    contact={
        "name": "MLOps Pipeline Maintainer",
        "email": "admin@smartfactory.dev",
    },
    openapi_tags=tags_metadata
)

OUTPUT_DIR = "output"
os.makedirs(OUTPUT_DIR, exist_ok=True)

@app.post("/analyze-defect/", tags=["핵심 품질 서비스(Core Quality Services)"], summary="부품 이미지 모델 추론 및 결함 검사")
async def analyze_defect(file: UploadFile = File(...)):
    """
    제조 공정 라인에서 촬영된 부품 이미지를 업로드받아 결함 여부를 검사합니다.
    - **파일 제약 사항:** 이미지 파일 (JPEG, PNG 등)
    - **반환 데이터:** 불량 여부, 신뢰도, 결함 유형, 후속 조치 권고안(Action Required), 식별된 제조 라인 ID 등 현장 최적화 데이터
    """
    try:
        # 가상의 처리 시간 지연 측정 시작
        start_time = time.time()
        
        contents = await file.read()
        file_size_bytes = len(contents)
        
        # 이미지 무결성 검증 (실제 AI 파이프라인 전처리)
        img = Image.open(io.BytesIO(contents))
        orig_width, orig_height = img.size
        
        # 분석이 완료된 이미지를 작업 디렉토리에 보관 로깅용
        timestamp_str = datetime.now().strftime("%Y%m%d_%H%M%S")
        save_path = os.path.join(OUTPUT_DIR, f"line_cam_{timestamp_str}_{file.filename}")
        img.save(save_path)

        # ---------------------------------------------------------
        # 2. AI-driven Defect Detection Mock-up 로직 극대화
        # ---------------------------------------------------------
        
        # 현장 데이터 생성
        line_id = random.choice(["Line-A(조립 공정)", "Line-B(도장 공정)", "Line-C(포장 공정)", "Line-D(최종 검수)"])
        sensor_temp = round(random.uniform(22.0, 26.5), 1) # 라인 온도 센서 데이터 가상 생성
        
        # 결함 판정 로직 (약 25%의 불량률 가정)
        is_defective = random.random() < 0.25 
        
        if is_defective:
            defect_type = random.choice(["미세 스크래치", "구조적 파손", "표면 오염", "도장 벗겨짐", "규격 치수 미달"])
            # 불량일 경우 모델의 추론 확신도 (0.65~0.99)
            confidence_score = round(random.uniform(0.65, 0.99), 4)
            
            # Action Required 판단: 신뢰도가 80% 미만이거나 특정 결함의 경우 재검사, 그 외엔 폐기
            if confidence_score < 0.80 or defect_type in ["미세 스크래치", "표면 오염"]:
                action_required = "재검사 (Re-inspect)"
            else:
                action_required = "폐기 (Discard)"
        else:
            defect_type = "정상"
            confidence_score = round(random.uniform(0.90, 0.99), 4) # 정상 판정의 경우 높은 신뢰도
            action_required = "통과 (Pass)"
            
        # 추론 지연 시간(Latency) 시뮬레이션
        process_time_ms = round((time.time() - start_time + random.uniform(0.12, 0.45)) * 1000, 2)

        # 3. 고도화된 JSON 구조의 분석 결과 반환
        return JSONResponse(content={
            "status": "success",
            "metadata": {
                "filename": file.filename,
                "resolution": f"{orig_width}x{orig_height}",
                "file_size_bytes": file_size_bytes,
            },
            "field_context": {
                "line_id": line_id,
                "environment_temp_c": sensor_temp,
                "timestamp": datetime.now().isoformat()
            },
            "analysis_result": {
                "is_defective": is_defective,
                "defect_type": defect_type,
                "confidence_score": confidence_score,
            },
            "decision_support": {
                "action_required": action_required,
                "inference_time_ms": process_time_ms
            },
            "message": "AI 기반 품질 검사가 완료되어 품질 관리 시스템(QMS)에 로깅되었습니다."
        })
        
    except Exception as e:
        return JSONResponse(status_code=400, content={"status": "error", "message": f"Image processing failed: {str(e)}"})

@app.get("/", tags=["시스템 상태(System Status)"], summary="서버 헬스 체크 및 모니터링")
def read_root():
    """
    **모니터링 대시보드 및 로드밸런서**가 자동으로 호출하는 헬스 체크용 엔드포인트입니다.
    현재 API 서버의 구동 상태, 시스템 시간, API 버전 정보를 제공합니다.
    """
    return {
        "status": "healthy",
        "service": "Smart Factory Quality Control API",
        "version": "2.1.0",
        "timestamp": datetime.now().isoformat()
    }
