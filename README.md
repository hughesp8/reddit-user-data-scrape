# reddit-user-data-scrape
A multi-processed python script that scrapes a supplied Reddit username for their comments, posts and subreddits they have commented in. 
It then uses a python module called yake to extract keywords and finally pandas to output extracted data to a csv.

This script accesses the Reddit API so you will need a Reddit dev account which you can setup/learn more about [here](https://www.reddit.com/wiki/api)

You will need to supply six arguments to the script. 1. CSV input file containing names of reddit accounts 2. CSV output file 3-6 Parameters associated
with reddit authentication when using the praw module that you can read about further [here](https://praw.readthedocs.io/en/latest/code_overview/reddit_instance.html?highlight=praw.Reddit#the-reddit-instance).

```
python3 <input csv> <output csv> <CLIENT_ID> <CLIENT_SECRET> <USERAGENT> <USERNAME>
```

