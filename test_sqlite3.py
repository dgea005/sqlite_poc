import sqlite3
from datetime import datetime
import numpy as np
from random_scrape_data_generator import give_random_data_chunks

sqlite3.register_adapter(np.int64, lambda val: int(val))

sqlite_file = "my_db.sqlite"
conn = sqlite3.connect(sqlite_file)
cur = conn.cursor()


#cur.execute('BEGIN TRANSACTION')
cur.execute("DROP TABLE IF EXISTS data_stg")

table_create_stmt = """CREATE TABLE data_stg (
    listing_id integer PRIMARY_KEY UNIQUE,
    listing_url text NOT NULL,
    kiez text NOT NULL,
    start_date text NOT NULL,
    end_date text NOT NULL,
    scrape_time timestamp NOT NULL,
    stay_length_days integer NOT NULL,
    size integer NOT NULL,
    price integer NOT NULL
);"""
cur.execute(table_create_stmt)


## try using the generator here

start_time = datetime.now()
iterations = 37230
#iterations = 100
print(f'starting at: {start_time}, running {iterations} iterations')

time_deltas = []
chunk_gen = give_random_data_chunks(iterations)
for i in range(iterations):
    chunk_start = datetime.now()
    data_chunk = next(chunk_gen)
    cur.execute('BEGIN TRANSACTION')
    cur.executemany("INSERT OR IGNORE INTO data_stg VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", data_chunk)

    cur.execute('COMMIT')
    time_deltas.append(datetime.now()-chunk_start)
conn.close()

end_time = datetime.now()

time_taken = end_time - start_time
print(f'time elapsed: {time_taken}')

print(f'time taken by last chunk: {time_deltas[-1]}')

## TODO:
# in reality the file will be downloaded and reopened frequently
# write the rest of the logic