CREATE TABLE users (
  id INTEGER PRIMARY KEY,
  username TEXT NOT NULL,
  email TEXT
);
INSERT INTO users (username, email) VALUES ('alice', 'alice@example.com');
