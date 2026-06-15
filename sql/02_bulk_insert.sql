IMPORT INTO transactions_v2 (
    call_id, call_time, client_id, region_code, campaign_type,
    call_status, client_response, duration_sec, follow_up_required
) FROM "file:///data/transactions.csv" WITH (
    format = "csv_with_names",
    delimiter = ",",
    header = "true"
);
