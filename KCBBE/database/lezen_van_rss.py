import pandas as pd
import argparse
import feedparser

"""
WIE WEET SINGLE QUOTE, EVEN OPZOEKEN. Sphinx
In this function an RSS link is read. The RSS link is parsed into the function.
Then a connection is made to get all data from the RSS link. 
The data is safed in a dataframe that is later written to a txt file.
"""

def main(rss):
    # Parse data from urls in list
    posts = []
    NewsFeed = feedparser.parse(rss)

    # Get information from all posts in url
    for i in range(len(NewsFeed.entries)):
        entry = NewsFeed.entries[i]
        id = create_id(entry)

        # Add post to list "posts"
        posts.append((entry.title, entry.link, entry.summary, entry.published, id))

    if len(posts) == 0:
        return ("Er is geen data opgehaald van de link")

    else:
        # NADENKEN misschien niet in df
        # Add posts to dataframe
        df = pd.DataFrame(posts, columns=['title', 'link', 'summary', 'published', 'id'])

        # Write dataframe to outputfile
        df.to_csv("out.txt", index=False)
        return ("Er is data opgehaald van de link")


def create_id(entry):
    """
    This function creates a unique id.
    The id consists of the link to the article + the first 30 characters of the title
    """
    # Get ID
    id = entry.id + entry.title[:30]
    id = id.split("www.")[1]

    # Remove spaces, points and slaches
    remove_characters = [".", " ", "/"]
    for character in remove_characters:
        id = id.replace(character, "_")

    # Make sure all ID's have the same length
    if (len(id)) < 80:
        difference = 80 - len(id)
        string_to_add = ""
        for x in range(difference):
            string_to_add += "_"
        id += string_to_add

    # Return ID
    return id