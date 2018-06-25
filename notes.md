# data
each listing has:
+ listing_id
+ listing_url
+ kiez
+ start_date
+ end_date (can be null)
+ scrape_time
+ stay_length_days (can be null)
+ size
+ price


each time you scrape a page (every five-ten minutes) there may only be a few new listings
we want to only send the new ones
so a lookup on listing_id is required

for now will ignore any changes that might occur to a listing

# previous solution

+ archive a json for each new scrape
+ have a deduplicated json to look up new listings
+ read this file, filter newly scraped listings by listing_id (only new listing_ids)
+ write new listings_ids and records to deduplicated json
+ send the new listings to email server (filter based on user preferences)


# new concept

+ set variable scrape time
+ insert to main table, on primary key conflict ignore
+ select out values where scrape_time == scrape time
+ send to user - filter based on preferences

# scale test
+ 40 listings per five minutes between hours of 8am to 12am
+ should be able to run for a year
+ stress test will simulate this by making the intervals smaller (within limits)
+ 480 listings per hour, 
+ 

(60 / 5) = 12 scraping per hour
12 * 40 = 480 raw records per hour
hours to test for 17
17 * 365 = 6205
total listings in stress test: 2978400 ( 3million) every 5 minutes

//((60 / 10) * 40) * (16 * 365) = 1489200.0 (1.4 million) every 10 minutes

only 5% new listings though

40 * 0.05 = 2 new listings per scrape

if there are 1.5 million scraped then that's 75,000 new listings ( if 5% of listings are new)
somehow want to move over the 75,000 ids in blocks and select random numbers from there

need to write a program to confirm this random number generation works
+ total number of scrapes is: 1.5m / 40 = 37,500
+ 37,500 iterations with only around 2 new listings per scrape (not including first scrape)




# common requirements
+ random data generator (only want between 0 and 5 new listings per scrape)
+ 