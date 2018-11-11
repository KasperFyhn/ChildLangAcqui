import os
from collections import Counter
from string import punctuation
import matplotlib.pyplot as plt
import glob

class Transcript:
    '''This class is a representation of a transcript following the norm from
    the CHILDES database. As long as the raw transcript file follows that norm,
    all kinds of informations and extractions from the transcript should be
    obtainable through the class methods and variables.'''  
    
    def __init__(self, filepath):        
        try:
            file = open(filepath, 'r', encoding='utf-8')
            self.name = os.path.basename(file.name)
            
            # store the raw transcript, but clean it a little bit
            self.raw_transcript = file.read()
            remove_list = ['\t', '\r']
            for item in remove_list:
                self.raw_transcript = self.raw_transcript.replace(item, '')
                
            # extract headerlines and transcriptlines
            text = self.raw_transcript.split('\n')
            self.headers = [line for line in text if line.startswith('@')]
            self.lines = [line for line in text
                          if line.startswith('*') or line.startswith('%')]
            self.fully_loaded = True # flag that transcript is fully loaded
            
        except IOError as e:
            self.fully_loaded = False # flag that transcript was not loaded
            print('An error occured when loading:', filepath)
            print('Error message:', e)
    
    def lines_as_tuples(self, speakers='all', morphosyntax=False,
                        grammar=False, actions=False):
        '''Return a list of tuples of all utterance lines, where tuple[0] is
        the three letter initials for the speaker and tuple[1] is the line. One
        or more speakers can be specified to retrieve just lines by these and 
        one or more flags can be marked to get annotations for the requested
        speaker(s).'''
        
        if speakers == 'all':
            speakers = self.speakers()
        if type(speakers) == str: # make sure that it is a list
            speakers = [speakers]
        
        # check if the requested speakers are present in the transcript
        # and report if they are not
        for speaker in speakers:
            if speaker not in self.speakers():
                print(f'WARNING: The speaker {speaker} is not present ' +
                      f'in the transcript {self.name}.')
              
        if morphosyntax == True:
            speakers.append('mor')
        if grammar == True:
            speakers.append('gra')
        if actions == True:
            speakers.append('act')
        
        # make list with lines as three part tuples
        tuples = [(line[0], line[1:4], line[5:]) for line in self.lines]
        
        # divide into blocks of turns with their annotations
        blocks = []
        for line in tuples:
            if line[0] == '*':
                blocks.append([])
                blocks[-1] = [(line[1], line[2])]
            elif line[0] == '%':
                blocks[-1].append((line[1], line[2]))
        
        # put together the blocks of the requested speakers along with the
        # requested annotations
        tuples = []
        for block in blocks:
            if block[0][0] in speakers:
                tuples += [line for line in block if line[0] in speakers]
        
        return tuples
    
    def tokens(self, speakers='all'):
        '''Return a list of tokens uttered by the specified speaker(s). If no
        speakers are specified, return tokens for all speakers.'''
        
        if speakers == 'all':
            speakers = self.speakers()
        if type(speakers) == str:
            speakers = [speakers]

        # get tokens from the specified speakers
        tuples = self.lines_as_tuples(speakers)
        tokens = [word.lower() for tpl in tuples for word in tpl[1].split()]
        
        # clean for punctuation
        tokens = ' '.join(tokens)
        tokens = ''.join(c for c in tokens if c not in punctuation)
        tokens = tokens.split()
        
        return tokens
    
    def types(self, speakers='all'):
        '''Return a list of types uttered by the specified speaker(s). If no
        speakers are specified, return types for all speakers.'''
        
        return set(self.tokens(speakers=speakers))
    
    def ttr(self, speakers='all', disregard=[]):
        '''Return the type-to-token-ratio of the transcript in whole. Pass
        specific speaker(s) to get it for only that/these speaker(s). A list of
        words to be disregarded in the calculation, e.g. function words, can be
        passed if needed.'''
        
        tokens = [word for word in self.tokens(speakers=speakers)
                  if word not in disregard]
        types = set(tokens)
        
        return len(types) / len(tokens)
    
    def word_freqs(self, speakers='all'):
        '''Return a Counter object of tokens uttered by the specified
        speaker(s). If no speakers are specified, return a Counter object for
        all speakers.'''
        
        return Counter(self.tokens(speakers=speakers))
    
    def prop_word_freqs(self, speakers='all'):
        '''Return a dict of words and their proportional frequencies.'''
        
        # get number of tokens and a list of tuples with words and frequencies
        freqs = self.word_freqs(speakers=speakers)
        tokens = sum(freqs.values()) 
        freqs = freqs.most_common()
        
        # make a dict with the word as key and prop freq as value
        prop_freqs = {word[0]:word[1]/tokens for word in freqs}
    
        return prop_freqs
    
    def speakers(self):
        '''Return a list of all speakers that appear in the transcript'''

        return list({line[1:4] for line in self.lines if line.startswith('*')})
    
    def speaker_details(self):
        '''Return a dictionary of dictionaries containing details about the
        given speaker(s). If no info is given in the original transcript file
        on some details, e.g. age or sex, those entries will simply be empty.
        The entries are: lang, corp, name, age, sex, role. As an example, the
        child's age is called by transcript.speaker_details()['CHI']['age']'''
        
        # find the ID lines from the header lines and split these
        ids = [id_str for id_str in self.headers if id_str.startswith('@ID')]
        ids = [entry[4:].split(sep='|') for entry in ids]
        
        # assign the values to their respective dict entries
        ids = [{'lang':entry[0], 'corp':entry[1], 'name':entry[2],
                'age':entry[3], 'sex':entry[4], 'role':entry[7]}
                for entry in ids]
        
        # create a dict with names as keys and the dicts as values
        ids = {entry['name']:entry
               for entry in ids if entry['name'] in self.speakers()}
                
        return ids
    
    def children(self):
        '''Return a list of the target child(ren) in the transcript.'''
        
        children = [entry['name'] for entry in self.speaker_details().values()
                    if entry['role'] == 'Target_Child']
        
        return children
    
def load_all_from_dir(dirname):
    '''Return a list of Transcript objects loaded from the given directory
    sorted after file names. The directory name should be stated either as
    relative path from the working directory or as an absolute path.'''
    
    prev_dir = os.getcwd()
    os.chdir(dirname)
    
    # load all transcripts from the folder and clean out non-loaded ones
    trans = [Transcript(file) for file in glob.glob('*.cha')]
    trans = [trn for trn in trans if trn.fully_loaded]
    
    # make sure the list is sorted
    trans.sort(key=lambda x: x.name)
    
    os.chdir(prev_dir)
    
    return trans

def age_in_months(age):
    '''Return an age passed in the format y;mm.dd as the number of months with
    two decimal numbers.'''
    
    # split the passed age string at the specified characters
    y_md = age.split(';')
    m_d = y_md[1].split('.')
    
    # convert each number to a float
    years = float(y_md[0])
    months = float(m_d[0])
    # in case days is not specified, assign 0
    try:
        days = float(m_d[1])
    except:
        days = 0
    
    # calculate number of months
    total = years * 12 + months + days / 30
    
    return float(f'{total:.2f}')

def word_freqs_all(transcripts, speakers='all'):
    '''Return one Counter object of all transcripts passed counting only
    utterances from the specified speaker(s).'''
    
    counters = [trn.word_freqs(speakers=speakers) for trn in transcripts]
    counter_all = Counter()
    for counter in counters:
        counter_all.update(counter)
        
    return counter_all

def basic_stats(transcript: Transcript, speakers='CHI'):
    '''Return a tuple containing age in months, number of tokens, number of
    types and TTR.'''
    
    age = age_in_months(transcript.speaker_details()['CHI']['age'])
    tokens = len(transcript.tokens(speakers='CHI'))
    types = len(transcript.types(speakers='CHI'))
    ttr = transcript.ttr(speakers=speakers)
    
    return(age, tokens, types, ttr)

def plot_word_freqs(words, transcripts, speaker='CHI'):
    '''Show a plot of proportional frequencies for each given word with the age
    of the child in months on the x-axis.'''
    
    if type(words) == str:
        words = [words]
    
    # get ages from all transcripts and convert these to months
    ages = [trn.speaker_details()['CHI']['age'] for trn in transcripts]
    ages = [age_in_months(age) for age in ages]
    
    # for each word, get and plot the prop freq with a color and a label
    for word in words:
        word_freqs = [trn.prop_word_freqs(speakers=speaker)[word]
                      if word in trn.tokens(speakers=speaker) else None
                      for trn in transcripts]        
        plt.plot(ages, word_freqs, '^', label=word)
    
    # make it pretty and show the plot
    plt.title('Word frequencies over time')
    plt.xlabel('Age in months')
    plt.ylabel('Proportional word frequency')
    plt.legend()
    plt.show()
    
    return

def plot_wordgroup_freq(wordgroup, transcripts, speaker='CHI', 
                        label='wordgroup'):
    '''Show a plot of the summed proportional frequencies of a given wordgroup
    with the age of the child in months on the x-axis.'''
    
    # get ages from all transcripts and convert these to months
    ages = [trn.speaker_details()['CHI']['age'] for trn in transcripts]
    ages = [age_in_months(age) for age in ages]
    
    # make a list of the sums of word frequencies of words in the group
    word_freqs = []
    for trn in transcripts:
        prop_freqs = trn.prop_word_freqs(speakers=speaker)
        tokens = trn.tokens(speakers=speaker)
        wordgroup_freqs = [prop_freqs[word] if word in tokens else 0
                           for word in wordgroup]
        sum_freqs = sum(wordgroup_freqs)
        if sum_freqs == 0:
            word_freqs.append(None)
        else:
            word_freqs.append(sum_freqs)
    
    # make and show the plot
    plt.plot(ages, word_freqs, '^')
    plt.title(f'Word frequencies over time for {label}')
    plt.xlabel('Age in months')
    plt.ylabel('Proportional word frequency')
    plt.show()
    
    return

def plot_ttr_over_time(transcripts, child='CHI', speakers=['CHI', 'MOT'],
                       disregard=[]):
    '''Show a plot of the type-to-token-ratio over time with the age of the
    child in months on the x-axis. As a default, the comparison is made with
    the target child and the mother. In case the child has another name code
    than 'CHI', this should be corrected in order to retrieve the age in each
    transcript.'''
    
    # get ages from all transcripts and convert these to months
    ages = [trn.speaker_details()[child]['age'] for trn in transcripts]
    ages = [age_in_months(age) for age in ages]
    
    # get type-to-token-ratios from all trancripts
    for speaker in speakers:
        ttr = [trn.ttr(speakers=speaker, disregard=disregard)
               if speaker in trn.speakers() else None
               for trn in transcripts]
        plt.plot(ages, ttr, '^', label=speaker)
    
    # make it pretty and show the plot
    plt.title('Type-to-token-ratio over time')
    plt.xlabel('Age in months')
    plt.ylabel('TTR')
    plt.legend()
    plt.show()
    
    return