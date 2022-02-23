import pandas as pd
import argparse
import feedparser

def main_read_file(file):
        # Make a list with urls from inputfile
        list = []
        with open(file) as f:
            lines = f.readlines()
            for line in lines:
                list.append(line.strip())

        # Parse data from urls in list
        posts = []
        for url in list:
            NewsFeed = feedparser.parse(url)

            # Get information from all posts in url
            for i in range(len(NewsFeed.entries)):
                entry = NewsFeed.entries[i]
                id = entry.id

                # Add post to list "posts"
                posts.append((entry.title, entry.link, entry.summary, entry.published, id))

        # Add posts to dataframe
        df = pd.DataFrame(posts, columns=['title', 'link', 'summary', 'published', 'id'])

        # Write dataframe to outputfile
        df.to_csv("output.txt", index=False)