#!/usr/bin/env python
import pandas as pd
import argparse
from collections import Counter
from sklearn.feature_extraction import text
from sklearn.feature_extraction.text import CountVectorizer
import pickle
from wordcloud import WordCloud
import matplotlib.pyplot as plt


# Metadata
__program__ = "Pre-Process files to start PICALO"
__author__ = "Britt Vink"
__maintainer__ = "Britt Vink"
__email__ = "bvink@umcg.nl"
__license__ = "GPLv3"
__version__ = 1.0
__description__ = "{} is a program developed and maintained by {}. " \
                  "This program is licensed under the {} license and is " \
                  "provided 'as-is' without any warranty or indemnification " \
                  "of any kind.".format(__program__,
                                        __author__,
                                        __license__)

class main():
    def __init__(self):
        # Get the command line arguments.
        arguments = self.create_argument_parser()


    @staticmethod
    def create_argument_parser():
        parser = argparse.ArgumentParser(prog=__program__,
                                         description=__description__,
                                         )
        # Add optional arguments.
        parser.add_argument("-v",
                            "--version",
                            action="version",
                            version="{} {}".format(__program__,
                                                   __version__),
                            help="show program's version number and exit.")

        return parser.parse_args()

    def start(self):
        self.print_arguments()
        data = pd.read_pickle("data_dtm.pkl")
        data = data.transpose()
        data_clean = pd.read_pickle("data_clean.pkl")
        print("data is loaded")


        top_dict = self.top_words(data)
        words = self.top_words_each_article(data, top_dict)
        stopwords = self.identify_common_word(data, words)
        self.recreat_dtm(data_clean, stopwords)
        self.wordclouds(data, stopwords)

        article_name_list = self.idenify_non_zeros(data)

        self.common_words_plot(data, words, article_name_list)




    def top_words(self, data):
        # Find the top 30 words per article
        top_dict = {}
        for c in data.columns:
            top = data[c].sort_values(ascending=False).head(30)
            top_dict[c] = list(zip(top.index, top.values))

        # Print the top 15 words per article
        for article, top_words in top_dict.items():
            filename = "top_words_article/" + article
            f = open(filename, "w")
            f.write(', '.join([word for word, count in top_words[0:14]]))
            f.close()

            print(article)
            print(', '.join([word for word, count in top_words[0:14]]))
            print('---')

        print("most used words in articles are found")

        return top_dict


    def top_words_each_article(self, data, top_dict):
        # top 30 words for each article
        words = []
        for article in data.columns:
            top = [word for (word, count) in top_dict[article]]
            for t in top:
                words.append(t)

        return words


    def identify_common_word(self, data, words):
        # Let's aggregate this list and identify the most common words along with how many routines they occur in
        wordslist = Counter(words).most_common()

        # If more than half of the comedians have it as a top word, exclude it from the list
        print(round(len(data.index) / 2))
        add_stop_words = [word for word, count in Counter(words).most_common() if count > (round(len(data.index) / 2))]
        print(add_stop_words)

        print("words found that are in all in lot of articles are found")

        # Let's update our document-term matrix with the new list of stop words
        # Add new stop words
        stop_words = text.ENGLISH_STOP_WORDS.union(add_stop_words)

        return stop_words


    def recreat_dtm(self, data_clean, stop_words):
        # Recreate document-term matrix
        cv = CountVectorizer(stop_words=stop_words)
        data_cv = cv.fit_transform(data_clean.text)
        data_stop = pd.DataFrame(data_cv.toarray(), columns=cv.get_feature_names_out())
        data_stop.index = data_clean.index
        data_stop.to_pickle("data_stop.pkl")
        pickle.dump(cv, open("cv_stop.pkl", "wb"))


    def wordclouds(self, data, stop_words):
        # Let's make some word clouds!
        # Terminal / Anaconda Prompt: conda install -c conda-forge wordcloud

        wc = WordCloud(stopwords=stop_words, background_color="white", colormap="Dark2",
                       max_font_size=150, random_state=42)

        # Reset the output dimensions
        plt.rcParams['figure.figsize'] = [16, 6]

        # Create plots
        for index, article in enumerate(data.columns):
            words = data[article].sort_values(ascending=False)[:20]
            wc = wc.generate_from_frequencies(words)
            name = "wordclouds/" + article + ".png"
            wc.to_file(name)

        print("wordclouds are made")


    def idenify_non_zeros(self, data):
        # Find the number of unique words that each article uses

        # Identify the non-zero items in the document-term matrix, meaning that the word occurs at least once
        unique_list = []
        article_name_list = []
        for article in data.columns:
            uniques = data[article].to_numpy().nonzero()[0].size
            unique_list.append(uniques)
            article = article.split('htm')
            article_name_list.append(article[1])

        # Create a new dataframe that contains this unique word count
        data_words = pd.DataFrame(list(zip(article_name_list, unique_list)), columns=['article', 'unique_words'])
        data_unique_sort = data_words.sort_values(by='unique_words')
        print(data_unique_sort)
        data_unique_sort.to_csv('unique_words_sorted.csv', index=False)

        print("unique words sorted is saved")

        return article_name_list


    def common_words_plot(self, data, words, article_name_list):
        # Let's take a look at the most common words again.
        comomwordslist = Counter(words).most_common()
        print(comomwordslist)
        print(comomwordslist[:10])
        # Let's isolate just these common words
        data_common_words = data.transpose()[['study', 'said', ]]
        data_profanity = pd.concat([data_common_words.study, data_common_words.said], axis=1)
        data_profanity.columns = ['study', 'said']

        # Let's create a scatter plot of our findings
        plt.rcParams['figure.figsize'] = [10, 8]

        for i, article in enumerate(data_profanity.index):
            x = data_profanity.study.loc[article]
            y = data_profanity.said.loc[article]
            plt.scatter(x, y, color='blue')
            plt.text(x + 1.5, y + 0.5, article_name_list[i], fontsize=10)
            plt.xlim(-5, 155)

        plt.title('Number of Commom Words Used in Routine', fontsize=20)
        plt.xlabel('Number of Times Study Said', fontsize=15)
        plt.ylabel('Number of Times Said Said', fontsize=15)

        plt.savefig('words_said_plot.png')

        print('Plot of common words made')


    def print_arguments(self):
        print("Arguments:")
        print("")


if __name__ == '__main__':
    m = main()
    m.start()

