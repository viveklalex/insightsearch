import spacy
from aspect_analyze import *
nlp = spacy.load("en_core_web_lg")
import regex as re


class DataframeClean(Aspectanalyze):
    def __init__(self, file, column_name, date_column,bert):
        self.file = file
        self.column_name = column_name
        self.date_column = date_column
        self.bert=bert

        self.common_titles = [
            "mr",
            "mrs",
            "ms",
            "miss",
            "dr",
            "herr",
            "monsieur",
            "hr",
            "frau",
            "a v m",
            "admiraal",
            "admiral",
            "alderman",
            "alhaji",
            "ambassador",
            "baron",
            "barones",
            "brig",
            "brigadier",
            "brother",
            "canon",
            "capt",
            "captain",
            "cardinal",
            "cdr",
            "chief",
            "cik",
            "cmdr",
            "col",
            "colonel",
            "commandant",
            "commander",
            "commissioner",
            "commodore",
            "comte",
            "comtessa",
            "congressman",
            "conseiller",
            "consul",
            "conte",
            "contessa",
            "corporal",
            "councillor",
            "count",
            "countess",
            "air cdre",
            "air commodore",
            "air marshal",
            "air vice marshal",
            "brig gen",
            "brig general",
            "brigadier general",
            "crown prince",
            "crown princess",
            "dame",
            "datin",
            "dato",
            "datuk",
            "datuk seri",
            "deacon",
            "deaconess",
            "dean",
            "dhr",
            "dipl ing",
            "doctor",
            "dott",
            "dott sa",
            "dr",
            "dr ing",
            "dra",
            "drs",
            "embajador",
            "embajadora",
            "en",
            "encik",
            "eng",
            "eur ing",
            "exma sra",
            "exmo sr",
            "f o",
            "father",
            "first lieutient",
            "first officer",
            "flt lieut",
            "flying officer",
            "fr",
            "frau",
            "fraulein",
            "fru",
            "gen",
            "generaal",
            "general",
            "governor",
            "graaf",
            "gravin",
            "group captain",
            "grp capt",
            "h e dr",
            "h h",
            "h m",
            "h r h",
            "hajah",
            "haji",
            "hajim",
            "her highness",
            "her majesty",
            "herr",
            "high chief",
            "his highness",
            "his holiness",
            "his majesty",
            "hon",
            "hr",
            "hra",
            "ing",
            "ir",
            "jonkheer",
            "judge",
            "justice",
            "khun ying",
            "kolonel",
            "lady",
            "lcda",
            "lic",
            "lieut",
            "lieut cdr",
            "lieut col",
            "lieut gen",
            "lord",
            "madame",
            "mademoiselle",
            "maj gen",
            "major",
            "master",
            "mevrouw",
            "miss",
            "mlle",
            "mme",
            "monsieur",
            "monsignor",
            "mstr",
            "nti",
            "pastor",
            "president",
            "prince",
            "princess",
            "princesse",
            "prinses",
            "prof",
            "prof dr",
            "prof sir",
            "professor",
            "puan",
            "puan sri",
            "rabbi",
            "rear admiral",
            "rev",
            "rev canon",
            "rev dr",
            "rev mother",
            "reverend",
            "rva",
            "senator",
            "sergeant",
            "sheikh",
            "sheikha",
            "sig",
            "sig na",
            "sig ra",
            "sir",
            "sister",
            "sqn ldr",
            "sr",
            "sr d",
            "sra",
            "srta",
            "sultan",
            "tan sri",
            "tan sri dato",
            "tengku",
            "teuku",
            "than puying",
            "the hon dr",
            "the hon justice",
            "the hon miss",
            "the hon mr",
            "the hon mrs",
            "the hon ms",
            "the hon sir",
            "the very rev",
            "toh puan",
            "tun",
            "vice admiral",
            "viscount",
            "viscountess",
            "wg cdr",
        ]

    @staticmethod
    def stop_words_removal(x, common_titles):


        # listing person names
        people = [w.text for w in nlp(x).ents if w.label_ == "PERSON"]
        stopwords = common_titles + people  # +list(stop_words)
        text_wp = (" ").join([w for w in x.lower().split() if w not in stopwords])
        text_wp = re.sub(r"[^\w\s]", "", text_wp).lower()

        return text_wp

    def _clean(self):
        # removing empty rows directly from the dataframe
        clean_df = self.file.copy().dropna()

        clean_df["reviewText"] = (
            clean_df["reviewText"]
            .apply(lambda x: self.stop_words_removal(x, self.common_titles))
            .dropna()
        )
     
        if self.date_column is not None:

                clean_df[self.date_column] = pd.to_datetime(
                    clean_df[self.date_column], format="%m %d, %Y"
                )
                clean_df = clean_df.assign(
                    year=clean_df["reviewTime"].dt.year,
                    month=clean_df["reviewTime"].dt.month,
                    day=clean_df["reviewTime"].dt.day,
              )

        Aspectanalyze.__init__(self, clean_df, self.column_name)
        Sentimentanalyze.__init__(self, clean_df, self.column_name, self.date_column,self.bert)
        return clean_df
