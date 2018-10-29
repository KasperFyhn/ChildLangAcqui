import childes_transcripts as ts
import seaborn as sns
import pandas as pd

def plot_word_freq(word: str, transcripts, speaker='CHI'):
    '''Show a plot of proportional frequencies for the given word with the age
    of the child in months on the x-axis.'''
    
    # get ages from all transcripts and convert these to months
    ages = [trn.speaker_details()['CHI']['age'] for trn in transcripts]
    ages = [ts.age_in_months(age) for age in ages]
    
    # get the proportinal
    freqs = [trn.prop_word_freqs(speakers=speaker)[word]
             if word in trn.tokens(speakers=speaker) else 0
             for trn in transcripts]
    
    data = pd.DataFrame({'age': ages, 'word frequency': freqs})

    sns.lmplot(x='age', y='word frequency', data=data)       
    
    return

def plot_wordgroup_freq(wordgroup, transcripts, speaker='CHI'):
    '''Show a plot of the summed proportional frequencies of a given wordgroup
    with the age of the child in months on the x-axis.'''
    
    # get ages from all transcripts and convert these to months
    ages = [trn.speaker_details()['CHI']['age'] for trn in transcripts]
    ages = [ts.age_in_months(age) for age in ages]
    
    # make a list of the sums of word frequencies of words in the group
    freqs = []
    for trn in transcripts:
        prop_freqs = trn.prop_word_freqs(speakers=speaker)
        tokens = trn.tokens(speakers=speaker)
        wordgroup_freqs = [prop_freqs[word] if word in tokens else 0
                           for word in wordgroup]
        freqs.append(sum(wordgroup_freqs))
    
    data = pd.DataFrame({'age': ages, 'Word group frequency': freqs})

    sns.lmplot(x='age', y='Word group frequency', data=data)  
    
    return