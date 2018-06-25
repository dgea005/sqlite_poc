import numpy as np
from random import randrange
from datetime import datetime

def give_random_data_chunks(scrape_iterations):
    first_scrape_number = 39
    for i in range(scrape_iterations):
        if np.random.binomial(1, 0.4):
            first_scrape_number += 1
        time_now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        # generate range of numbers
        listing_ids = np.arange(first_scrape_number-39, first_scrape_number)
        # would write here
        yield [generate_random_record(listing_id=l_id, scrape_time=time_now) for l_id in listing_ids]


def generate_random_record(listing_id, scrape_time):
    listing_url = f'http://my_fake_url.com/items/{listing_id}'
    random_text = f'{randrange(8**10)}'
    return [
                listing_id, 
                listing_url, 
                random_text, 
                random_text, 
                random_text, 
                scrape_time, 
                np.random.randint(30, 270), 
                np.random.randint(10, 100), 
                np.random.randint(400, 1000)
            ]
    
    # return {
    #          'listing_id': listing_id,
    #          'listing_url': listing_url,
    #          'kiez': random_text,
    #          'start_date': random_text,
    #          'end_date': random_text,
    #          'scrape_time': scrape_time,
    #          'stay_length_days': np.random.randint(30, 270),
    #          'size': np.random.randint(10, 100),
    #          'price': np.random.randint(400, 1000)
    #         }

if __name__ == "__main__":
    # how this can be used in the other processes
    iterations = 2
    chunk_gen = give_random_data_chunks(iterations)
    for i in range(iterations):
        dc = next(chunk_gen)
        for record in dc:
            for col in record:
                print(type(col))
        
    #print(len(data))
    #print(data[-1])
