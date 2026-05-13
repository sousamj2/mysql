CREATE TABLE IF NOT EXISTS qresults (
  result_id    INT PRIMARY KEY AUTO_INCREMENT,
  q_uuid       VARCHAR(36) NOT NULL,
  user_id      CHAR(36),
  q_score      INT NOT NULL,
  n_correct    INT NOT NULL,
  n_wrong      INT NOT NULL,
  n_skipped    INT NOT NULL,
  duration     INT NOT NULL,
  createdatts  DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  quiz_config  JSON,
  question_ids JSON,
  user_answers JSON,
  CONSTRAINT fk_qresults_user
    FOREIGN KEY (user_id) REFERENCES users(user_id)
) ENGINE=InnoDB;
