CREATE DATABASE IF NOT EXISTS `mc_mjcrafts`;
CREATE DATABASE IF NOT EXISTS `explicolivais`;

CREATE USER IF NOT EXISTS 'mc_user'@'%' IDENTIFIED BY 'mc_password';
GRANT ALL PRIVILEGES ON `mc_mjcrafts`.* TO 'mc_user'@'%';

CREATE USER IF NOT EXISTS 'expl_user'@'%' IDENTIFIED BY 'expl_password';
GRANT ALL PRIVILEGES ON `explicolivais`.* TO 'expl_user'@'%';

FLUSH PRIVILEGES;
