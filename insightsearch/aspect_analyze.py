from nltk.corpus import stopwords
from collections import Counter
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from textblob import TextBlob
from insightsearch.sentiment_analyze import *
from tqdm import tqdm
tqdm.pandas()



class Aspectanalyze(Sentimentanalyze):
    def __init__(self, df, column_name):
        self.stop_words = set(stopwords.words("english"))
        self.df = df

        self.column_name = column_name
        self.lines = [l for l in self.df["reviewText"]]

    def _aspect_list(self, line, candidate_aspects, aspect_opinion_dict):
        blob = TextBlob(line)

        if len(candidate_aspects) > 0:
            for a in candidate_aspects:
                first_w_index = blob.words.index(a.split()[0])

                last_w_index = blob.words.index(a.split()[-1])

                # chechking whether word_index-1 is adj if yes will add to list
                pref_words = []
                if self.index_valid(first_w_index - 1 , blob.tags):
                    if blob.tags[first_w_index - 1][1] in [
                       "RB",
                        "RBR",
                        "RBS",
                        "JJ",
                        "JJR",
                        "JJS",
                    ] and blob.tags[first_w_index - 1][0].lower().strip() not in [
                        "very",
                        "really","much"
                    ]:

                        if self.index_valid(first_w_index - 2, blob.tags) and blob.tags[first_w_index - 2][0].lower().strip() in [
                               "not"] :

                            pref_words.append(
                               "not" + str(blob.tags[first_w_index - 1][0].lower().strip())
                            )

                        else:
                            pref_words.append(
                               blob.tags[first_w_index - 1][0].lower().strip()
                            )





                if len(pref_words) > 0:
                    if self.index_valid(first_w_index - 2, blob.tags):
                        if blob.tags[first_w_index - 2][1] in [
                            "RB",
                            "RBR",
                            "RBS",
                            "JJ",
                            "JJR",
                            "JJS",
                        ] and blob.tags[first_w_index - 2][0].lower().strip() not in [
                            "very",
                            "really","much","and"
                        ]:
                            if self.index_valid(first_w_index - 3, blob.tags) and blob.tags[first_w_index - 3][0].lower().strip() in [
                               "not"] :

                                pref_words.append(
                               "not" + str(blob.tags[first_w_index - 2][0].lower().strip())
                            )

                            else:
                                pref_words.append(
                               blob.tags[first_w_index - 2][0].lower().strip()

                            )
                    if self.index_valid(first_w_index - 2, blob.tags):
                        if blob.tags[first_w_index - 2][1] in [
                            "RB",
                            "RBR",
                            "RBS",
                            "JJ",
                            "JJR",
                            "JJS",
                        ] and blob.tags[first_w_index - 2][0].lower().strip() in [
                            "and"
                        ]:
                            pref_words.append(
                                blob.tags[first_w_index - 3][0].lower().strip()

                            )

                    if self.index_valid(first_w_index - 3, blob.tags):
                        if blob.tags[first_w_index - 3][1] in [
                            "RB",
                            "RBR",
                            "RBS",
                            "JJ",
                            "JJR",
                            "JJS",
                        ] and blob.tags[first_w_index - 3][0].lower().strip() not in [
                            "very",
                            "really","much","and"
                        ]:
                            pref_words.append(
                                blob.tags[first_w_index - 3][0].lower().strip()
                            )

                attr = "".join(pref_words)
                if str(a.strip()) in list(aspect_opinion_dict.keys()):

                    aspect_opinion_dict[a] = " ".join(
                        [aspect_opinion_dict[a] + " " + attr]
                    ).strip()
                else:
                    aspect_opinion_dict[str(a.strip())] = attr

                after_words = []

                if self.index_valid(first_w_index + 1, blob.tags) and blob.words[first_w_index + 1].lower() in ["am", "is", "are", "was", "were"]:
                    if self.index_valid(first_w_index + 2, blob.tags):

                        if blob.tags[last_w_index + 2][1] in [
                            "RB",
                            "RBR",
                            "RBS",
                            "JJ",
                            "JJR",
                            "JJS",
                        ] and blob.tags[last_w_index + 2][0].lower().strip() not in [
                            "very",
                            "really","always"
                        ] :
                            after_words.append(
                                blob.tags[last_w_index + 2][0].lower().strip()
                            )

                    if self.index_valid(first_w_index + 3, blob.tags):

                        if blob.tags[last_w_index + 3][1] in [
                            "RB",
                            "RBR",
                            "RBS",
                            "JJ",
                            "JJR",
                            "JJS",
                        ] and blob.tags[last_w_index + 3][0].lower().strip() in [
                            "and"

                        ] :
                            if self.index_valid(first_w_index + 4, blob.tags):

                                after_words.append(
                                    blob.tags[last_w_index + 4][0].lower().strip()
                            )


                    if len(after_words) > 0:
                        if self.index_valid(first_w_index + 3, blob.tags):
                            if blob.tags[last_w_index + 3][1] in [
                                "RB",
                                "RBR",
                                "RBS",
                                "JJ",
                                "JJR",
                                "JJS",
                            ] and blob.tags[first_w_index + 3][0].lower().strip() not in [
                                "very",
                                "really","much","and"
                            ]:
                                after_words.append(
                                    blob.tags[last_w_index + 3][0].lower().strip()
                                )
                    if self.index_valid(first_w_index + 4, blob.tags):
                        if blob.tags[last_w_index + 4][1] in [
                            "RB",
                            "RBR",
                            "RBS",
                            "JJ",
                            "JJR",
                            "JJS",
                        ] and blob.tags[first_w_index + 3][0].lower().strip() in [
                            "and"
                        ]:
                            if self.index_valid(first_w_index + 4, blob.tags):

                                after_words.append(
                                        blob.tags[last_w_index + 4][0].lower().strip()
                            )



                    if self.index_valid(first_w_index + 2, blob.tags):
                        if blob.tags[last_w_index + 2][0].lower() in ["very", "really"]:

                            if self.index_valid(first_w_index + 3, blob.tags):
                                after_words.append(
                                    blob.tags[last_w_index + 3][0].lower().strip()
                                )
                    attr = " ".join(after_words)

                    if str(a.strip()) in list(aspect_opinion_dict.keys()):

                        aspect_opinion_dict[a] = " ".join(
                            [aspect_opinion_dict[a] + " " + attr]
                        ).strip()
                    else:
                        aspect_opinion_dict[str(a).strip()] = attr
            else:
                pass

    def aspect_generator(self):

        self.candidate_aspects_dict = {}
        self.aspect_opinion_dict = {}
        aspects = []
        no_reviews=len(self.lines)
        for line in tqdm(self.lines,desc="Collecting Aspects And Opinions From {} Reviews".format(no_reviews)):

            blob = TextBlob(line)

            nouns_1 = [aspects.append(n) for n, t in blob.tags if t in ["NN", "NNS", "NNP", "NNPS"] ]
            candidate_aspects = [n for n, t in blob.tags if t in ["NN", "NNS", "NNP", "NNPS"] ]

            self._aspect_list(line, candidate_aspects, self.aspect_opinion_dict)
        keys = list(self.aspect_opinion_dict.keys())
        for a in keys:

            if a in self.stop_words:
                self.aspect_opinion_dict.pop(a)

        final_df = pd.DataFrame(
            self.aspect_opinion_dict.items(), columns=["aspects", "opinions"]
        )
        final_df["opinions"] = final_df["opinions"].apply(lambda x: str(x).strip())
        final_df["opinion_len"] = final_df["opinions"].apply(
            lambda x: len(str(x).split())
        )
        final_df["opinion_list"] = final_df["opinions"].apply(
            lambda x: Counter(str(x).split()).most_common()
        )
        self.rslt_df = final_df.sort_values(by="opinion_len", ascending=False)
        return self.aspect_opinion_dict, self.rslt_df

    @staticmethod
    def index_valid(index_last_word, blob_tags):

        return True if (0 <= (index_last_word) < len(blob_tags)) else False

    def showing_aspect(self):
        try:
            aspect_opinion_dict = self.aspect_opinion_dict

        except AttributeError:
            self.aspect_generator()
        aspect_name = list(self.rslt_df["aspects"][:9])
        aspect_opinion = list(self.rslt_df["opinion_list"][:9])
        fig = make_subplots(
            rows=3,
            cols=3,
            start_cell="top-left",

            subplot_titles=aspect_name,
        )
        cols = [1, 2, 3, 1, 2, 3, 1, 2, 3]
        rows = [1, 1, 1, 2, 2, 2, 3, 3, 3]

        for s in range(9):
            try:
                op = [w[0] for w in aspect_opinion[s][:5]][::-1]
            except:
                if len(aspect_opinion[s]) > 0:

                        op=[w[0] for w in aspect_opinion[s][:len(aspect_opinion[s])]][::-1]
            try:

                num = [w[1] for w in aspect_opinion[s][:5]][::-1]
            except:

               if len(aspect_opinion[s]) > 0:
                  num=[w[1] for w in aspect_opinion[s][:len(aspect_opinion[s])]][::-1]

            fig = fig.add_trace(
                go.Bar(
                    x=num,
                    showlegend=False,
                    marker=dict(color="rgb(140, 3, 252)", colorscale="Edge"),
                    y=op,
                    orientation="h",

                ),
                row=int(rows[s]),
                col=int(cols[s]),
            )
            fig.update_layout(
                title="People are talking about.",
                height=1200,
                showlegend=False)
        self.fig_aspect = fig
