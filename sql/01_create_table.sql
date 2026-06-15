CREATE TABLE transactions_v2 (
    call_id String,
    call_time Datetime,
    client_id String,
    region_code String,
    campaign_type String,
    call_status String,
    client_response String,
    duration_sec Uint32,
    follow_up_required Bool,
    PRIMARY KEY (call_id)
);
