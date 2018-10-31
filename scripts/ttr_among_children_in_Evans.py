import childes_transcripts as ts
import pandas as pd
import seaborn as sns

folder = r'C:\Users\Kasper Fyhn Jacobsen\Dropbox\Child Language Acquisition\Data\Evans'
transcripts = ts.load_all_from_dir(folder)


all_ttrs = []

for transcript in transcripts: 
    for child in transcript.children():
        name = child
        age = ts.age_in_months(transcript.speaker_details()[child]['age'])
        ttr = transcript.ttr(speakers=child)
        all_ttrs.append((name, age, ttr))
        
data = pd.DataFrame(all_ttrs, columns=['name', 'age', 'ttr'])

print(data.head(len(data)))

sns.scatterplot(x='age', y='ttr', data=data)