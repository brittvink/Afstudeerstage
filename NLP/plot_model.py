#!/usr/bin/env python

import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

import numpy as np
import argparse
import pandas as pd
import pickle
import matplotlib.pyplot as plt
from collections import Counter
from matplotlib.ticker import FuncFormatter
from sklearn.manifold import TSNE
from bokeh.plotting import figure, output_file, show, save
from bokeh.io import output_notebook
import matplotlib.colors as mcolors
import pyLDAvis
import pyLDAvis.gensim_models as gensimvis
import os


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
        self.model = getattr(arguments, 'model')
        self.corpus = getattr(arguments, 'corpus')
        self.data = getattr(arguments, 'data_file')
        self.prefix = getattr(arguments, 'prefix')
        self.passes = getattr(arguments, 'passes')
        self.topic = getattr(arguments, 'topic')
        self.modelName = "lda_model_{}_topics_{}_passes".format(self.topic, self.passes)

        # Set variables.
        self.outdir = os.path.join(str(os.path.dirname(os.path.abspath(__file__))), 'model_plots')
        if not os.path.exists(self.outdir):
            os.makedirs(self.outdir)


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
        parser.add_argument("-d",
                            "--data_file",
                            type=str,
                            required=True,
                            help="How many topics")
        parser.add_argument("-c",
                            "--corpus",
                            type=str,
                            required=True,
                            help="How many passes")
        parser.add_argument("-m",
                            "--model",
                            type=str,
                            required=True,
                            help="How many topics")

        parser.add_argument("-p",
                            "--prefix",
                            type=str,
                            required=True,
                            help="Prefix for the output file.")

        parser.add_argument("-passes",
                            "--passes",
                            type=int,
                            required=True,
                            help="Prefix for the output file.")

        parser.add_argument("-topic",
                            "--topic",
                            type=int,
                            required=True,
                            help="Prefix for the output file.")

        return parser.parse_args()


    def start(self):
        self.print_arguments()

        data_ready = pd.read_pickle(self.data)

        file = open(self.corpus, 'rb')
        corpus = pickle.load(file)
        file.close()

        file = open(self.model, 'rb')
        lda_model = pickle.load(file)
        file.close()

        df_topic_sents_keywords = self.format_topics_sentences(ldamodel=lda_model, corpus=corpus, texts=data_ready)

        # Format
        df_dominant_topic = df_topic_sents_keywords.reset_index()
        df_dominant_topic.columns = ['Document_No', 'Dominant_Topic', 'Topic_Perc_Contrib', 'Keywords', 'Text']
        print(df_dominant_topic.head(10))


        # Display setting to show more characters in column
        pd.options.display.max_colwidth = 100

        sent_topics_sorteddf_mallet = pd.DataFrame()
        sent_topics_outdf_grpd = df_topic_sents_keywords.groupby('Dominant_Topic')

        for i, grp in sent_topics_outdf_grpd:
            sent_topics_sorteddf_mallet = pd.concat([sent_topics_sorteddf_mallet,
                                                     grp.sort_values(['Perc_Contribution'], ascending=False).head(1)],
                                                    axis=0)

        # Reset Index
        sent_topics_sorteddf_mallet.reset_index(drop=True, inplace=True)

        # Format
        sent_topics_sorteddf_mallet.columns = ['Topic_Num', "Topic_Perc_Contrib", "Keywords", "Representative Text"]
        # Show
        sent_topics_sorteddf_mallet.head(10)

        doc_lens = [len(d) for d in df_dominant_topic.Text]

        self.plot_1(doc_lens)

        topics = lda_model.show_topics(formatted=False)
        data_flat = [w for w_list in data_ready for w in w_list]
        counter = Counter(data_flat)

        out = []
        for i, topic in topics:
            for word, weight in topic:
                out.append([word, i , weight, counter[word]])

        df = pd.DataFrame(out, columns=['word', 'topic_id', 'importance', 'word_count'])

        self.plot_2(df)

        dominant_topics, topic_percentages = self.topics_per_document(model=lda_model, corpus=corpus, end=-1)

        # Distribution of Dominant Topics in Each Document
        df = pd.DataFrame(dominant_topics, columns=['Document_Id', 'Dominant_Topic'])
        dominant_topic_in_each_doc = df.groupby('Dominant_Topic').size()
        df_dominant_topic_in_each_doc = dominant_topic_in_each_doc.to_frame(name='count').reset_index()


        # Total Topic Distribution by actual weight
        topic_weightage_by_doc = pd.DataFrame([dict(t) for t in topic_percentages])
        df_topic_weightage_by_doc = topic_weightage_by_doc.sum().to_frame(name='count').reset_index()

        # Top 3 Keywords for each Topic
        topic_top3words = [(i, topic) for i, topics in lda_model.show_topics(formatted=False)
                                         for j, (topic, wt) in enumerate(topics) if j < 3]

        df_top3words_stacked = pd.DataFrame(topic_top3words, columns=['topic_id', 'words'])
        df_top3words = df_top3words_stacked.groupby('topic_id').agg(', \n'.join)
        df_top3words.reset_index(level=0,inplace=True)

        # Plot
        self.plot_3(df_dominant_topic_in_each_doc, df_top3words, df_topic_weightage_by_doc)


        # Get topic weights and dominant topics ------------

        # Get topic weights
        topic_weights = []
        for i, row_list in enumerate(lda_model[corpus]):
            topic_weights.append([w for i, w in row_list[0]])

        # Array of topic weights
        arr = pd.DataFrame(topic_weights).fillna(0).values

        # Keep the well separated points (optional)
        arr = arr[np.amax(arr, axis=1) > 0.35]

        # Dominant topic number in each doc
        topic_num = np.argmax(arr, axis=1)

        # tSNE Dimension Reduction
        tsne_model = TSNE(n_components=2, verbose=1, random_state=0, angle=.99, init='pca')
        tsne_lda = tsne_model.fit_transform(arr)

        # Plot the Topic Clusters using Bokeh
        self.plot_4(tsne_lda, topic_num)
        self.plot_5(lda_model, corpus)


    def plot_1(self, doc_lens):
        # Plot
        plt.figure(figsize=(16, 7), dpi=160)
        plt.hist(doc_lens, bins=1000, color='navy')
        plt.text(750, 100, "Mean   : " + str(round(np.mean(doc_lens))))
        plt.text(750, 90, "Median : " + str(round(np.median(doc_lens))))
        plt.text(750, 80, "Stdev   : " + str(round(np.std(doc_lens))))
        plt.text(750, 70, "1%ile    : " + str(round(np.quantile(doc_lens, q=0.01))))
        plt.text(750, 60, "99%ile  : " + str(round(np.quantile(doc_lens, q=0.99))))

        plt.gca().set(xlim=(0, 1000), ylabel='Number of Documents', xlabel='Document Word Count')
        plt.tick_params(size=16)
        plt.xticks(np.linspace(0, 1000, 11))
        plt.title('Distribution of Document Word Counts', fontdict=dict(size=22))

        outpath = os.path.join(self.outdir,
                               "{}_distribution_document_word_counts{}.png".format(self.prefix, self.modelName))

        plt.savefig(outpath)
        plt.close()


    def plot_2(self, df):
        for i in range(0,self.topic):
            fig = plt.figure()
            ax = fig.add_subplot(111)

            cols = [color for name, color in mcolors.TABLEAU_COLORS.items()]
            ax.bar(x='word', height="word_count", data=df.loc[df.topic_id==i, :], color=cols[i], width=0.5, alpha=0.3, label='Word Count')
            ax_twin = ax.twinx()
            ax_twin.bar(x='word', height="importance", data=df.loc[df.topic_id==i, :], color=cols[i], width=0.2, label='Weights')
            ax.set_ylabel('Word Count', color=cols[i])

            # ax_twin.set_ylim(0, 0.030); ax.set_ylim(0, 3500)
            ax.set_title('Topic: ' + str(i), color=cols[i], fontsize=16)
            ax.tick_params(axis='y', left=False)
            ax.set_xticklabels(df.loc[df.topic_id==i, 'word'], rotation=30, horizontalalignment= 'right')
            ax.legend(loc='upper left'); ax_twin.legend(loc='upper right')
            fig.suptitle('Word Count and Importance of Topic Keywords', fontsize=22, y=1.05)
            outpath = os.path.join(self.outdir,
                                   "{}_topicnumber{}_common_words_{}.png".format(self.prefix, str(i), self.modelName))

            plt.savefig(outpath)
            plt.close()


    def plot_3(self, df_dominant_topic_in_each_doc, df_top3words, df_topic_weightage_by_doc):
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4), dpi=120, sharey=True)

        # Topic Distribution by Dominant Topics
        ax1.bar(x='Dominant_Topic', height='count', data=df_dominant_topic_in_each_doc, width=.5, color='firebrick')

        ax1.set_xticks(range(df_dominant_topic_in_each_doc.Dominant_Topic.unique().__len__()))
        tick_formatter = FuncFormatter(
            lambda x, pos: 'Topic ' + str(x) + '\n' + df_top3words.loc[df_top3words.topic_id == x, 'words'].values[0])
        ax1.xaxis.set_major_formatter(tick_formatter)
        ax1.tick_params(axis="x", labelsize=5)

        ax1.set_title('Number of Documents by Dominant Topic', fontdict=dict(size=10))
        ax1.set_ylabel('Number of Documents')
        ax1.set_ylim(0, 4000)

        # Topic Distribution by Topic Weights
        ax2.bar(x='index', height='count', data=df_topic_weightage_by_doc, width=.5, color='steelblue')
        ax2.set_xticks(range(df_topic_weightage_by_doc.index.unique().__len__()))
        ax2.xaxis.set_major_formatter(tick_formatter)
        ax2.tick_params(axis="x", labelsize=5)
        ax2.set_title('Number of Documents by Topic Weightage', fontdict=dict(size=10))

        outpath = os.path.join(self.outdir,
                               "{}_Number_of_docs_per_topic_{}.png".format(self.prefix, self.modelName))

        plt.savefig(outpath)


    def plot_4(self, tsne_lda, topic_num):
        output_notebook()
        n_topics = 4
        mycolors = np.array([color for name, color in mcolors.CSS4_COLORS.items()])
        print(mycolors)
        plot = figure(title="t-SNE Clustering of {} LDA Topics".format(n_topics),
                      plot_width=900, plot_height=700)
        print(tsne_lda[:, 0])
        print("_____")
        print(tsne_lda[:, 1])
        plot.scatter(x=tsne_lda[:, 0], y=tsne_lda[:, 1], color=mycolors[topic_num])

        outpath = os.path.join(self.outdir,
                               "{}_t-SNE_Clustering_of_LDA_topics_{}.html".format(self.prefix, self.modelName))

        output_file(outpath)
        save(plot)


    def plot_5(self, lda_model, corpus):
        pyLDAvis.enable_notebook()
        vis = gensimvis.prepare(lda_model, corpus, dictionary=lda_model.id2word)
        outpath = os.path.join(self.outdir,
                               "{}_gensimvis_{}.html".format(self.prefix, self.modelName))

        pyLDAvis.save_html(vis, outpath)


    def format_topics_sentences(self, ldamodel, corpus, texts):
        # Init output
        sent_topics_df = pd.DataFrame()

        # Get main topic in each document
        for i, row_list in enumerate(ldamodel[corpus]):
            row = row_list[0] if ldamodel.per_word_topics else row_list
            row = sorted(row, key=lambda x: (x[1]), reverse=True)
            # Get the Dominant topic, Perc Contribution and Keywords for each document
            for j, (topic_num, prop_topic) in enumerate(row):
                if j == 0:  # => dominant topic
                    wp = ldamodel.show_topic(topic_num)
                    topic_keywords = ", ".join([word for word, prop in wp])
                    sent_topics_df = sent_topics_df.append(
                        pd.Series([int(topic_num), round(prop_topic, 4), topic_keywords]), ignore_index=True)
                else:
                    break
        sent_topics_df.columns = ['Dominant_Topic', 'Perc_Contribution', 'Topic_Keywords']

        # Add original text to the end of the output
        contents = pd.Series(texts)
        sent_topics_df = pd.concat([sent_topics_df, contents], axis=1)

        return (sent_topics_df)


    def topics_per_document(self, model, corpus, start=0, end=1):
        corpus_sel = corpus[start:end]
        dominant_topics = []
        topic_percentages = []
        for i, corp in enumerate(corpus_sel):
            topic_percs, wordid_topics, wordid_phivalues = model[corp]
            dominant_topic = sorted(topic_percs, key=lambda x: x[1], reverse=True)[0][0]
            dominant_topics.append((i, dominant_topic))
            topic_percentages.append(topic_percs)
        return (dominant_topics, topic_percentages)


    def print_arguments(self):
        print("Arguments:")
        print("  > Model : {}".format(self.model))
        print("  > Corpus : {}".format(self.corpus))
        print("  > Data : {}".format(self.data))
        print("  > Prefix : {}".format(self.prefix))
        print("  > Passes : {}".format(self.passes))
        print("  > Topic : {}".format(self.topic))
        print("  > ModelName : {}".format(self.modelName))


if __name__ == '__main__':
    m = main()
    m.start()