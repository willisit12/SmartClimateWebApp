-- users table
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username VARCHAR(150) NOT NULL UNIQUE,
    password_hash VARCHAR(128) NOT NULL
);

-- predictions table
CREATE TABLE predictions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    outside_temp FLOAT NOT NULL,
    room_temp FLOAT NOT NULL,
    occupancy INTEGER NOT NULL,
    hour_of_day INTEGER NOT NULL,
    weekday INTEGER NOT NULL,
    predicted_ac_temp FLOAT NOT NULL,
    predicted_light_status VARCHAR(10) NOT NULL,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    user_id INTEGER NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);
