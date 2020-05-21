## uber_drivers_reddit
Part of the project involving using the content and social network data of Uber drivers from Reddit to analyze their organizing behavior

- This uses PRAW, the Python wrapper of the Reddit API, for fetching the data.
- This script collects some important properties of posts/submissions (threads), their comments (messages), and authors (users) of those submissions and comments. 
- Sadly, the API only allows retrieving the top 1000 posts in the subreddit (as far as I know currently).
  - Here, top means the one with the highest difference of upvotes to downvotes.
  - I'm looking at alternatives that circumvent this issue. One of them is [this auto-archival tool](https://github.com/peoplma/subredditarchive). 
- I'm looking at ways to improve this process. For the top 1000, it took around 5 3/4 hours to even get the raw data.
