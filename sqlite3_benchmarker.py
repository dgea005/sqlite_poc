import os
import sqlite3
from datetime import datetime
import numpy as np
from random_scrape_data_generator import give_random_data_chunks



class sqlite3Simulator:

    def __init__(self, iteration_count, sqlite_db="my_db.sqlite"):
        """
        iteration_count: number of scrapes of (40) records to run
        sqlite_db: sqlite db to run this on
        """
        self.sqlite_db = sqlite_db
        self.iteration_count = iteration_count
        self.time_taken = None
        self.chunk_changes = []
        self.time_deltas = []
        self.select_time_deltas = []

    def get_cursor(self):
        # doing each chunk in it's own connection is a bit closer to application realitys
        connection = sqlite3.connect(self.sqlite_db)
        cursor = connection.cursor()
        return connection, cursor

    def setup(self):
        """fresh setup of sqlite3 db
        modifies some files and doesn't return anything
        """
        sqlite3.register_adapter(np.int64, lambda val: int(val))
        try:
            print('setting up clean sqlite3 file')
            os.remove(self.sqlite_db)
            conn, cur = self.get_cursor()
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
                                    price integer NOT NULL,
                                   scrape_batch_id integer NOT NULL 
                                );"""
            cur.execute(table_create_stmt)
            conn.close()
        except OSError:
            pass

    def run_simulation(self):
        start_time = datetime.now()
        print(f'sqlite3 simulation starting at: {start_time}, running {self.iteration_count} iterations')

        
        chunk_gen = give_random_data_chunks(self.iteration_count)
        for i in range(self.iteration_count):
            chunk_start = datetime.now()
            data_chunk = next(chunk_gen)
            # doesn't return anthing...
            _ = [record.append(i) for record in data_chunk]
            conn, cur = self.get_cursor()

            cur.execute('BEGIN TRANSACTION')
            cur.executemany("INSERT OR IGNORE INTO data_stg VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", data_chunk)
            cur.execute('COMMIT')
            self.time_deltas.append((datetime.now()-chunk_start).total_seconds())
            self.chunk_changes.append(conn.total_changes)
            conn.close()

            ## run additional query here
            self.get_latest_items_written()
        
        end_time = datetime.now()
        self.time_taken = end_time - start_time
        print(f'time elapsed: {self.time_taken}')
        print(f'time taken by last chunk: {self.time_deltas[-1]}')


    def get_latest_items_written(self):
        query_start = datetime.now()
        conn, cur = self.get_cursor()
        sql = "select * from data_stg where scrape_batch_id = (select max(scrape_batch_id) from data_stg)"
        for row in cur.execute(sql):
            pass
        self.select_time_deltas.append((datetime.now()-query_start).total_seconds())


if __name__ == "__main__":
    benchmarker = sqlite3Simulator(iteration_count=10)
    benchmarker.setup()
    benchmarker.run_simulation()