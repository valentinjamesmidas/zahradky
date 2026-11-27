CREATE TABLE IF NOT EXISTS project_requests (
 request_id TEXT PRIMARY KEY,
 code TEXT NOT NULL UNIQUE,
 intent TEXT NOT NULL CHECK(intent IN ('quote','visit')),
 location TEXT NOT NULL,
 visit_email TEXT,
 assigned_to TEXT NOT NULL,
 created_at INTEGER NOT NULL,
 first_response_at INTEGER
);
CREATE INDEX IF NOT EXISTS requests_open ON project_requests(intent,location,first_response_at,created_at);
INSERT OR IGNORE INTO project_requests (request_id,code,intent,location,assigned_to,created_at)
 SELECT request_id,code,'quote',json_extract(configuration,'$.location'),'zahradky@albetservis.cz',created_at FROM leads;
CREATE VIEW IF NOT EXISTS sales_inbox AS
 SELECT r.code,r.intent,r.location,r.assigned_to,r.created_at,r.first_response_at,
 (r.first_response_at-r.created_at) AS response_seconds,
 COALESCE(r.visit_email,l.email) AS email,l.name,l.phone,l.note,l.configuration,l.reservation_requested
 FROM project_requests r LEFT JOIN leads l USING(request_id);
