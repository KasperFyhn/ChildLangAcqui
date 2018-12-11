import childes_transcripts as ts
import re
import pandas as pd


def zero_stage(transcript, holophrase_proportion=0.95):
    """Return true if the proportion of holophrases uttered by the child exceeds
    the given holophrase proportion threshold."""

    lines = get_morphosyntax_lines(transcript)

    utterances = []
    for line in lines:
        line = line.split('.')
        utterances += line
    utterances = [u.strip() for u in utterances if u != '']

    holophrases = 0
    non_holos = 0
    for utter in utterances:
        words = utter.split(' ')
        if len(words) > 1:
            non_holos += 1
        elif len(words) == 1:
            holophrases += 1

    if (holophrases / len(utterances)) > holophrase_proportion:
        return holophrases / len(utterances), True
    else:
        return holophrases / len(utterances), False


def first_stage(transcript):


    lines = get_morphosyntax_lines(transcripts)

    agent_patient_sentence = 0
    for line in lines:
        line = line.split(' ')
        for tag in line:


def second_stage(transcript):
    pass

def third_stage(transcript):
    pass

def fourth_stage(transcript):
    pass

def fifth_stage(transcript):
    pass


def get_morphosyntax_lines(transcript, speaker='CHI'):
    """Return a list of only morphosyntactic tagging for stated speaker in the
    transcript."""

    lines = transcript.lines_as_tuples(speakers=speaker, morphosyntax=True)
    lines = [line[1] for line in lines if line[0] == 'mor']

    return lines


def is_nominal(wordtag):
    """Return true if the word tag is noun, proper noun or pronoun."""




# data = input('Please, input the data folder')
transcripts = ts.load_all_from_dir(
        r'C:\Users\Kasper Fyhn Jacobsen\Dropbox\Child Language Acquisition\Data\Brown\Eve'
        )

ages = [ts.age_in_months(tran.speaker_details()['CHI']['age'])
        for tran in transcripts]
mlus = [tran.mlu() for tran in transcripts]
df = pd.DataFrame({'ages': ages, 'MLU': mlus})

for t in transcripts:
    print(zero_stage(t))