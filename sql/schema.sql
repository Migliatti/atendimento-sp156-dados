-- One row per request. Dates are ISO text (YYYY-MM-DD), which sorts correctly
-- and works with SQLite's date functions.
CREATE TABLE requests (
    id             INTEGER PRIMARY KEY,
    opened_date    TEXT NOT NULL,
    closed_date    TEXT,           -- empty while the request is not closed
    channel        TEXT,           -- PORTAL, CRM, MOBILE, CHATBOT, INTEGRACAO, ...
    theme          TEXT,
    subject        TEXT,
    service        TEXT,
    status         TEXT,           -- closed, open, in_progress, cancelled, other
    organ          TEXT,
    subprefecture  TEXT,
    district       TEXT,
    days_to_close  INTEGER         -- only for closed requests with a closing date
);
CREATE INDEX idx_requests_opened ON requests (opened_date);
CREATE INDEX idx_requests_theme  ON requests (theme);
