SELECT 
u.first_name, u.last_name, u.email, u.tier,
co.lastloginip, co.lastlogints, co.vpn_check
FROM users u
JOIN connection co ON u.user_id = co.user_id
WHERE u.email = %s;
