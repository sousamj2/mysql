SELECT 
u.first_name, u.last_name, u.email, u.tier, u.ign,
co.lastloginip, co.lastlogints
FROM users u
JOIN connection co ON u.user_id = co.user_id
WHERE u.email = %s
