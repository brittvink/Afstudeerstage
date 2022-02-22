def main(rss):
    import pandas as pd
    import argparse
    import feedparser

    # Parse data from urls in list
    posts = []
    NewsFeed = feedparser.parse(rss)

    # Get information from all posts in url
    for i in range(len(NewsFeed.entries)):
        entry = NewsFeed.entries[i]
        id = entry.id

        # Add post to list "posts"
        posts.append((entry.title, entry.link, entry.summary, entry.published, id))

    # Add posts to dataframe
    df = pd.DataFrame(posts, columns=['title', 'link', 'summary', 'published', 'id'])

    # Write dataframe to outputfile
    df.to_csv("out.txt", index=False)