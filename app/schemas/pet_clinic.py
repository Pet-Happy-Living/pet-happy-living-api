# =============================
# Pydantic 모델 정의 (API 응답 구조)
# =============================
from __future__ import annotations
from pydantic import BaseModel
from typing import Optional


class ClinicRow(BaseModel):
    mgt_no: str
    opnsfteamcode: str
    apv_perm_ymd: Optional[str]
    apv_cancel_ymd: Optional[str]
    trd_state_gbn: Optional[str]
    trd_state_nm: Optional[str]
    dtl_state_gbn: Optional[str]
    dtl_state_nm: Optional[str]
    dcby_md: Optional[str]
    clg_st_dt: Optional[str]
    clg_end_dt: Optional[str]
    ropn_ymd: Optional[str]
    site_tel: Optional[str]
    site_area: Optional[str]
    site_post_no: Optional[str]
    site_whl_addr: Optional[str]
    rdn_whl_addr: Optional[str]
    rdn_post_no: Optional[str]
    bplc_nm: Optional[str]
    last_mod_ts: Optional[str]
    update_gbn: Optional[str]
    update_dt: Optional[str]
    uptae_nm: Optional[str]
    x: Optional[float]
    y: Optional[float]
    lind_job_gbn_nm: Optional[str]
    lind_prcb_gbn_nm: Optional[str]
    lind_seq_no: Optional[str]
    rgtmbds_no: Optional[str]
    totep_num: Optional[str]

    class Config:
        orm_mode = True
        from_attributes = True
