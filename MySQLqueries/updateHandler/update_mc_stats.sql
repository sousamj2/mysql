UPDATE users 
SET 
    mc_uuid = %s,
    mc_rank = %s,
    mc_bank = %s,
    mc_claims = %s,
    mc_last_online = %s
WHERE email = %s;
