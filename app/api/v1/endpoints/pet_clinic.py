# =============================
# 공공 API 연동 및 데이터 적재
# =============================
import httpx

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.dialects.postgresql import insert as pg_insert
from typing import List
from app.db.session import get_db
from app.models.pet_clinic import PetClinic
from app.schemas.pet_clinic import ClinicRow
from app.core.config import get_settings

router = APIRouter()
settings = get_settings()

@router.get("/load-pet-clinics", response_model=List[ClinicRow], responses={
    200: {"description": "INFO-000: 정상 처리되었습니다."},
    400: {"description": "ERROR-300~336: 요청 인자 오류 또는 샘플 범위 초과"},
    401: {"description": "INFO-100: 인증키가 유효하지 않습니다."},
    404: {"description": "INFO-200: 해당하는 데이터가 없습니다."},
    500: {"description": "ERROR-500~601: 서버 또는 SQL 오류"}
})
async def load_pet_clinics(start: int = 1, end: int = 5, db: AsyncSession = Depends(get_db)):
    API_KEY = settings.SEOUL_OPEN_API_KEY
    url = f"http://openapi.seoul.go.kr:8088/{API_KEY}/json/LOCALDATA_020301/{start}/{end}/"

    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        data = response.json()

    rows = data.get("LOCALDATA_020301", {}).get("row", [])
    if not rows:
        raise HTTPException(status_code=404, detail="No data returned from API")

    clinics = [PetClinic(
        opnsfteamcode=r.get("OPNSFTEAMCODE"),
        mgt_no=r.get("MGTNO"),
        apv_perm_ymd=r.get("APVPERMYMD"),
        apv_cancel_ymd=r.get("APVCANCELYMD"),
        trd_state_gbn=r.get("TRDSTATEGBN"),
        trd_state_nm=r.get("TRDSTATENM"),
        dtl_state_gbn=r.get("DTLSTATEGBN"),
        dtl_state_nm=r.get("DTLSTATENM"),
        dcby_md=r.get("DCBYMD"),
        clg_st_dt=r.get("CLGSTDT"),
        clg_end_dt=r.get("CLGENDDT"),
        ropn_ymd=r.get("ROPNYMD"),
        site_tel=r.get("SITETEL"),
        site_area=r.get("SITEAREA"),
        site_post_no=r.get("SITEPOSTNO"),
        site_whl_addr=r.get("SITEWHLADDR"),
        rdn_whl_addr=r.get("RDNWHLADDR"),
        rdn_post_no=r.get("RDNPOSTNO"),
        bplc_nm=r.get("BPLCNM"),
        last_mod_ts=r.get("LASTMODTS"),
        update_gbn=r.get("UPDATEGBN"),
        update_dt=r.get("UPDATEDT"),
        uptae_nm=r.get("UPTAENM"),
        x=float(r["X"]) if r.get("X") else None,
        y=float(r["Y"]) if r.get("Y") else None,
        lind_job_gbn_nm=r.get("LINDJOBGBNNM"),
        lind_prcb_gbn_nm=r.get("LINDPRCBGBNNM"),
        lind_seq_no=r.get("LINDSEQNO"),
        rgtmbds_no=r.get("RGTMBDSNO"),
        totep_num=r.get("TOTEPNUM")
    ) for r in rows]

    for clinic in clinics:
        clinic_data = ClinicRow.from_orm(clinic).dict(exclude_unset=True)

        stmt = pg_insert(PetClinic).values(**clinic_data)
        stmt = stmt.on_conflict_do_update(
            index_elements=['mgt_no'],
            set_=clinic_data
        )
        await db.execute(stmt)
    await db.commit()

    return [ClinicRow.from_orm(clinic) for clinic in clinics]
