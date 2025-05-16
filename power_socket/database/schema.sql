DROP TABLE IF EXISTS power_state;

CREATE TABLE power_state (
    id INTEGER PRIMARY KEY CHECK (id = 1),
    is_on BOOLEAN NOT NULL
);
INSERT OR IGNORE INTO power_state (id, is_on) VALUES (1,0)