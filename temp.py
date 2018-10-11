import childes_transcripts as ts
from collections import Counter
from nltk.corpus import stopwords
import os

master = r'C:\Users\Kasper Fyhn Jacobsen\Dropbox\Child Language Acquisition\Data\Brown'
en_stopwords = stopwords.words('english')
os.chdir(master)

for folder in os.listdir():

    if os.path.isdir(folder):

        transcripts = ts.load_all_from_dir(folder)
        print(folder)
        ts.plot_wordgroup_freq(en_stopwords, transcripts, label='stopwords')