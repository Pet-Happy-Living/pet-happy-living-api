# =============================
# 테이블 정의 (서울시 동물병원 정보)
# =============================

from sqlalchemy import Column, String, Date, Float, Text, DateTime, func
from sqlalchemy.ext.declarative import declarative_base

# SQLAlchemy 기본 베이스 클래스 생성
Base = declarative_base()


class PetClinic(Base):
    __tablename__ = "seoul_pet_clinics"

    mgt_no = Column(String, primary_key=True, comment="관리번호")
    opnsfteamcode = Column(String, comment="개방자치단체코드")
    apv_perm_ymd = Column(String, comment="인허가일자")
    apv_cancel_ymd = Column(String, comment="인허가취소일자")
    trd_state_gbn = Column(String, comment="영업상태코드")
    trd_state_nm = Column(String, comment="영업상태명")
    dtl_state_gbn = Column(String, comment="상세영업상태코드")
    dtl_state_nm = Column(String, comment="상세영업상태명")
    dcby_md = Column(String, comment="폐업일자")
    clg_st_dt = Column(String, comment="휴업시작일자")
    clg_end_dt = Column(String, comment="휴업종료일자")
    ropn_ymd = Column(String, comment="재개업일자")
    site_tel = Column(String, comment="전화번호")
    site_area = Column(String, comment="소재지면적")
    site_post_no = Column(String, comment="소재지우편번호")
    site_whl_addr = Column(Text, comment="지번주소")
    rdn_whl_addr = Column(Text, comment="도로명주소")
    rdn_post_no = Column(String, comment="도로명우편번호")
    bplc_nm = Column(String, comment="사업장명")
    last_mod_ts = Column(String, comment="최종수정일자")
    update_gbn = Column(String, comment="데이터갱신구분")
    update_dt = Column(String, comment="데이터갱신일자")
    uptae_nm = Column(String, comment="업태구분명")
    x = Column(Float, comment="X좌표")
    y = Column(Float, comment="Y좌표")
    lind_job_gbn_nm = Column(String, comment="축산업무구분명")
    lind_prcb_gbn_nm = Column(String, comment="축산물가공업구분명")
    lind_seq_no = Column(String, comment="축산일련번호")
    rgtmbds_no = Column(String, comment="권리주체일련번호")
    totep_num = Column(String, comment="총인원")
    created_at = Column(DateTime(timezone=True), server_default=func.now(), comment="데이터 생성 시각")
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), comment="데이터 수정 시각")
