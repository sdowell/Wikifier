# Wikifier

## Getting Started

Import environment.yml [tutorial](http://conda.pydata.org/docs/using/envs.html#share-an-environment)

Note that the first runtime will be long if starting with an empty database, as the program populates the database in real time using the wikipedia api.

Entry point: app.py

Optional arguments:

-t twitterfile (located in twitter_data/Twitter_gold.txt)

-w wisefile (located in wise_data/standard_result.txt)

-d databasefile (name of database file)

-g weights (comma delimited list of weights)

-n (use neural network model)

-p printfile (print accuracy results to file)

-k ngrams (ngram size)

-r numtrials (number of data points to evaluate)
