import sqlite3


# TODO implement some kind of a lock
database = sqlite3.connect("shortcuts.sqlite3", check_same_thread=False)


database.execute("CREATE TABLE IF NOT EXISTS shortcuts ("
                 "shortened VARCHAR(64) PRIMARY KEY,"
                 "expanded VARCHAR,"
                 "internal BOOLEAN DEFAULT FALSE"
                 ")")


database.commit()
