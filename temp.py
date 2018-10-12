import childes_transcripts as ts
from collections import Counter
from nltk.corpus import stopwords
import os



folder = '/Users/kasperfyhnjacobsen/Dropbox/Child Language Acquisition/Data/Kuczaj'
en_stopwords = stopwords.words('english')

transcripts = ts.load_all_from_dir(folder)
ts.plot_word_freqs(['i', 'you', 'doll'], transcripts)

'''
print(folder)
ts.plot_ttr(transcripts, speakers=['CHI', 'MOT', 'FAT'])
ts.plot_ttr(transcripts, speakers=['CHI', 'MOT', 'FAT'], disregard=en_stopwords)
ts.plot_wordgroup_freq(en_stopwords, transcripts, label='stopwords')
'''
