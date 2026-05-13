CREATE TABLE IF NOT EXISTS users (
  user_id    CHAR(36) PRIMARY KEY,
  first_name VARCHAR(100) NOT NULL,
  last_name  VARCHAR(100) NOT NULL,
  email      VARCHAR(255) NOT NULL,
  username   VARCHAR(100) NOT NULL,
  h_password VARCHAR(255),
  ign        VARCHAR(100),
  mc_uuid    VARCHAR(100),
  mc_rank    VARCHAR(50) DEFAULT 'default',
  mc_bank    DECIMAL(15,2) DEFAULT 0.00,
  mc_claims  INT DEFAULT 0,
  mc_last_online DATETIME,
  g_token    BOOLEAN NOT NULL DEFAULT TRUE,
  tier       TINYINT DEFAULT 1
) ENGINE=InnoDB;
