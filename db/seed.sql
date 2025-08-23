-- Seed data
INSERT INTO users (username, email)
VALUES ('admin', 'admin@example.com')
ON CONFLICT (username) DO NOTHING;
