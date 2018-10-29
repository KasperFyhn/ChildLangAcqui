import childes_transcripts as ts
from nltk.corpus import stopwords
import seaborn as sns
import pandas as pd



folder = '/Users/kasperfyhnjacobsen/Dropbox/Child Language Acquisition/Data/Kuczaj'
transcripts = ts.load_all_from_dir(folder)

data = [ts.basic_stats(transcript) for transcript in transcripts]


df = pd.DataFrame(data, columns=['age', 'tokens', 'types'])

sns.lmplot(x='age', y='types', data=df)