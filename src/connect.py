import sys

import obd 
import time
from datetime import datetime
import sqlite3

db_conn = sqlite3.connect("data/trips.db")
cursor = db_conn.cursor()

portstr = "/dev/ttys001"  # replace with your OBD-II adapter's port
baudrate = 38400  # replace with your OBD-II adapter's baud rate
connection = obd.OBD(portstr=portstr, baudrate=baudrate)  # auto-connects to emulator

commands = [
            ("RPM", obd.commands.RPM),
            ("Speed", obd.commands.SPEED),
            ("Coolant Temperature", obd.commands.COOLANT_TEMP)
        ]

if not connection.is_connected():
    print("Failed to connect to OBD-II adapter")
    connection.close()
    db_conn.close()
    sys.exit(1)


try:
    cursor.execute("INSERT INTO trips (start_time) VALUES (?)", (datetime.now().strftime('%Y-%m-%d %H:%M:%S'),))
    trip_id = cursor.lastrowid
    db_conn.commit()
    print(f"Started new trip with ID: {trip_id}")
    while True: 
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print(f"Timestamp: {current_time}")
        for name, cmd in commands:
            response = connection.query(cmd)
            if response.is_null():
                print(f"{name}: No data")
            else:
                print(f"{name}: {response.value}")
                cursor.execute("INSERT INTO readings (trip_id, timestamp, pid_name, value) VALUES (?, ?, ?, ?)",
                               (trip_id, current_time, name, response.value.magnitude))
        db_conn.commit()
        time.sleep(1)  # wait for 1 second before the next query
except KeyboardInterrupt:
    print("Exiting...")
    connection.close()
    db_conn.close()
