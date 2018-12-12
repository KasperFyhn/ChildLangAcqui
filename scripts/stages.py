import childes_transcripts as ts
import re
import pandas as pd

def main():
    #data = input('Please, input the data folder')
    transcripts = ts.load_all_from_dir(
        r'C:\Users\Kasper Fyhn Jacobsen\Dropbox\Child Language Acquisition\Data\Brown\Sarah'
    )

    ages = [ts.age_in_months(tran.speaker_details()['CHI']['age'])
            for tran in transcripts]
    mlus = [tran.mlu() for tran in transcripts]
    df = pd.DataFrame({'ages': ages, 'MLU': mlus})

    for t in transcripts:
        print(in_second_stage(t))



def zero_stage(transcript, threshold=0.95):
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

    if (holophrases / len(utterances)) > threshold:
        return holophrases / len(utterances), True
    else:
        return holophrases / len(utterances), False


def in_first_stage(transcript):
    """Determine if the child is in/has passed the first stage of acquisition
    by checking for clues for knowledge of semantic relations in the given
    transcript. Clues include sentences with subject and verb, ..."""

    lines = get_morphosyntax_lines(transcript)

    agent_patient_sentence = 0
    for line in lines:
        line = line.split(' ')
        #for tag in line:



def in_second_stage(transcript, threshold = 0.05):
    """Determine if the child is in/has passed the second stage of acquisition
    by checking for inflections in the child's utterances.
    """
#TODO: Check for productivity in some way!

    inflected_words = 0
    words_total = 0

    lines = get_morphosyntax_lines(transcript)

    for line in lines:
        line = line.split()
        words_total += len(line)
        for word in line:
            if len(word.split('-')) > 1:
                inflected_words += 1

    if inflected_words / words_total > threshold:
        return inflected_words / words_total, True
    else:
        return inflected_words / words_total, False


def in_third_stage(transcript):
    #TODO: based on different sentence types
    """"""
    pass

def in_fourth_stage(transcript):
    # TODO: based on embedded sentences

    pass

def in_fifth_stage(transcript):
    # TODO: based on coordinated sentences

    pass


def get_morphosyntax_lines(transcript, speaker='CHI'):
    """Return a list of only morphosyntactic tagging for stated speaker in the
    transcript."""

    lines = transcript.lines_as_tuples(speakers=speaker, morphosyntax=True)
    lines = [clean_line(line[1]) for line in lines if line[0] == 'mor']

    return lines


def get_grammar_lines(transcript, speaker='CHI'):
    """Return a list of only grammar tagging for stated speaker in the
    transcript."""

    lines = transcript.lines_as_tuples(speakers=speaker, grammar=True)
    lines = [clean_line(line[1]) for line in lines if line[0] == 'gra']

    return lines

def is_nominal(wordtag):
    """Return true if the word tag is noun, proper noun or pronoun."""


def is_verb(wordtag):
    """Return true if the word tag is a verb."""


def clean_line(line):
    """Clean a string for ' .', ' ?', ' !'"""

    remove_list = [' .', ' ?', ' !']
    for item in remove_list:
        line = line.replace(item, '')

    return line


main()