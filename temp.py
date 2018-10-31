import childes_transcripts as ts

folder = r'C:\Users\Kasper Fyhn Jacobsen\Dropbox\Child Language Acquisition\Data\Evans'
transcripts = ts.load_all_from_dir(folder)

children = [trans.children() for trans in transcripts]

all_ttrs = []

for transcript in transcripts: 
    for child in transcript.children():
        name = child
        age = ts.age_in_months(transcript.speaker_details()[child]['age'])
        ttr = transcript.ttr(speakers=child)
        all_ttrs.append((name, age, ttr))
        
print(all_ttrs)