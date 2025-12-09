import sqlite3

def init_db():
    aConn = sqlite3.connect("taxi.db")
    aCur = aConn.cursor()

    aCur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE,
            password TEXT,
            role TEXT,
            name TEXT,
            address TEXT,
            phone TEXT
        )
    """)

    aCur.execute("""
        CREATE TABLE IF NOT EXISTS bookings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            driver_id INTEGER,
            pickup_location TEXT NOT NULL,
            dropoff_location TEXT NOT NULL,
            booking_date TEXT NOT NULL,
            booking_time TEXT NOT NULL,
            status TEXT DEFAULT 'pending',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id),
            FOREIGN KEY (driver_id) REFERENCES users(id)
        )
    """)

    try:
        aCur.execute("SELECT driver_id FROM bookings LIMIT 1")
    except sqlite3.OperationalError:
        print("Migrating database: Adding driver_id column to bookings table...")
        aCur.execute("ALTER TABLE bookings ADD COLUMN driver_id INTEGER")
        print("Migration completed successfully!")

    aConn.commit()
    aConn.close()
