CREATE TABLE IF NOT EXISTS leads (
 request_id TEXT PRIMARY KEY,
 code TEXT NOT NULL UNIQUE,
 name TEXT NOT NULL,
 email TEXT NOT NULL,
 phone TEXT NOT NULL,
 note TEXT NOT NULL DEFAULT '',
 reservation_requested INTEGER NOT NULL DEFAULT 0,
 configuration TEXT NOT NULL,
 total INTEGER NOT NULL,
 down_payment INTEGER NOT NULL,
 monthly REAL NOT NULL,
 created_at INTEGER NOT NULL
);
CREATE INDEX IF NOT EXISTS leads_created ON leads(created_at);
CREATE TABLE IF NOT EXISTS rate_limits (
 key TEXT NOT NULL,
 window INTEGER NOT NULL,
 count INTEGER NOT NULL DEFAULT 1,
 PRIMARY KEY (key, window)
);
