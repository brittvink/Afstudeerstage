#!/usr/bin/env python
# import pandas for data wrangling
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from gensim.models import KeyedVectors

import gensim.downloader
# Show all available models in gensim-data

wv = KeyedVectors.load("word2vec.wordvectors2", mmap='r')
sims = wv.most_similar('sustainability', topn=10)  # get other similar words

df = pd.DataFrame(sims, columns =['Name', 'Value'])

# Reorder the dataframe
df = df.sort_values(by=['Value'])

print(df)

# initialize the figure
plt.figure(figsize=(20,10))
ax = plt.subplot(111, polar=True)
plt.axis('off')

# Constants = parameters controling the plot layout:
upperLimit = 100
lowerLimit = 30
labelPadding = 4

# Compute max and min in the dataset
max = df['Value'].max()

# Let's compute heights: they are a conversion of each item value in those new coordinates
# In our example, 0 in the dataset will be converted to the lowerLimit (10)
# The maximum will be converted to the upperLimit (100)
slope = (max - lowerLimit) / max
heights = slope * df.Value + lowerLimit

# Compute the width of each bar. In total we have 2*Pi = 360°
width = 2*np.pi / len(df.index)

# Compute the angle each bar is centered on:
indexes = list(range(1, len(df.index)+1))
angles = [element * width for element in indexes]

# Draw bars
bars = ax.bar(
    x=angles,
    height=heights,
    width=width,
    bottom=lowerLimit,
    linewidth=2,
    edgecolor="white",
    color="darkorange",
)

# Add labels
for bar, angle, height, label in zip(bars,angles, heights, df["Name"]):

    # Labels are rotated. Rotation must be specified in degrees :(
    rotation = np.rad2deg(angle)

    # Flip some labels upside down
    alignment = ""
    if angle >= np.pi/2 and angle < 3*np.pi/2:
        alignment = "right"
        rotation = rotation + 180
    else:
        alignment = "left"

    # Finally add the labels
    ax.text(
        x=angle,
        y=lowerLimit + bar.get_height() + labelPadding,
        s=label,
        ha=alignment,
        va='center',
        rotation=rotation,
        rotation_mode="anchor")

    ax.text(
        x=0.5, y=0.58, s="sustainability",
        color='darkorange', va="center", ha="center", ma="center",
        fontsize=18, fontweight="bold", linespacing=0.87, transform=ax.transAxes
    )
plt.savefig("similar_words.png")