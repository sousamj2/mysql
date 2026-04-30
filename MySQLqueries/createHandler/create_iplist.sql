CREATE TABLE IF NOT EXISTS iplist (
  ip_id       CHAR(36) PRIMARY KEY,
  user_id     CHAR(36),
  ip_address  VARCHAR(45),
  first_seen  DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  last_seen   DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  login_count INT NOT NULL DEFAULT 1,
  CONSTRAINT fk_iplist_user
    FOREIGN KEY (user_id) REFERENCES users(user_id)
) ENGINE=InnoDB;
