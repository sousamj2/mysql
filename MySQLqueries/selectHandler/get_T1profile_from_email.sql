SELECT 
u.first_name, u.last_name, u.email, u.tier, u.ign,
u.mc_uuid, u.mc_rank, u.mc_bank, u.mc_claims, u.mc_last_online,
co.lastloginip, co.lastlogints
FROM users u
JOIN connection co ON u.user_id = co.user_id
WHERE u.email = %s
