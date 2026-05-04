UPDATE connection SET
lastlogints = thislogints,
lastloginip = thisloginip,
thislogints = %s,
thisloginip = %s
WHERE user_id = %s;