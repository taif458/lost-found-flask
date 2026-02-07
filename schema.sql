CREATE TABLE IF NOT EXISTS lost_items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    report_id INTEGER NOT NULL,
    name TEXT NOT NULL,
    item_name TEXT NOT NULL,
    description TEXT,
    date TEXT,
    status TEXT,
    claim_status TEXT
);