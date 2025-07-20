from fastapi import APIRouter
from app.api.v1.endpoints import user, pet_clinic

router = APIRouter()

# 각 모듈의 라우터를 prefix와 함께 등록
router.include_router(user.router, prefix="/users", tags=["Users"])
router.include_router(pet_clinic.router, prefix="/pet-clinic", tags=["Pet-clinic"])


@router.get("/health", tags=["Health"])
def health_check():
    return {"status": "ok"}
