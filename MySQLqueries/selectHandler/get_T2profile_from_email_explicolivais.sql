SELECT 
u.first_name, u.last_name, u.email, u.tier,
p.address, p.number, p.floor, p.door, p.zip_code1, p.zip_code2, p.cell_phone, p.nfiscal, p.notes,
co.lastloginip, co.lastlogints, co.vpn_check
FROM users u
JOIN personal p ON u.user_id = p.user_id
JOIN connection co ON u.user_id = co.user_id
WHERE u.email = %s;
