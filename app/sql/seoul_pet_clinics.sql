CREATE TABLE IF NOT EXISTS seoul_pet_clinics (
    mgt_no VARCHAR PRIMARY KEY,               -- 관리번호
    opnsfteamcode VARCHAR,                    -- 개방자치단체코드
    apv_perm_ymd VARCHAR,
    apv_cancel_ymd VARCHAR,
    trd_state_gbn VARCHAR,
    trd_state_nm VARCHAR,
    dtl_state_gbn VARCHAR,
    dtl_state_nm VARCHAR,
    dcby_md VARCHAR,
    clg_st_dt VARCHAR,
    clg_end_dt VARCHAR,
    ropn_ymd VARCHAR,
    site_tel VARCHAR,
    site_area VARCHAR,
    site_post_no VARCHAR,
    site_whl_addr TEXT,
    rdn_whl_addr TEXT,
    rdn_post_no VARCHAR,
    bplc_nm VARCHAR,
    last_mod_ts VARCHAR,
    update_gbn VARCHAR,
    update_dt VARCHAR,
    uptae_nm VARCHAR,
    x FLOAT,
    y FLOAT,
    lind_job_gbn_nm VARCHAR,
    lind_prcb_gbn_nm VARCHAR,
    lind_seq_no VARCHAR,
    rgtmbds_no VARCHAR,
    totep_num VARCHAR,
    created_at TIMESTAMPTZ DEFAULT NOW(),     -- 생성일자
    updated_at TIMESTAMPTZ                    -- 수정일자
);
