import childes_transcripts as ts
import pandas as pd


def main():
    data = input('Please, input the data folder')
    transcripts = ts.load_all_from_dir(data)

    ages = [ts.age_in_months(tran.speaker_details()['CHI']['age'])
            for tran in transcripts]
    mlus = [tran.mlu() for tran in transcripts]
    df = pd.DataFrame({'ages': ages, 'MLU': mlus})

    for t in transcripts:
        print(in_fourth_stage(t))


def in_zeroth_stage(transcript, threshold=0.95):
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
    by checking if s/he has passed stage 0, yet not reached stage 2."""

    if not in_zeroth_stage(transcript) and not in_second_stage(transcript):
        return True
    else:
        return False


def in_second_stage(transcript, inflection_threshold=0.05,
                    function_words_threshold=0.2):
    """Determine if the child is in/has passed the second stage of acquisition
    by checking for inflections in the child's utterances."""

    #TODO: check for clitics?

    inflected_words = 0
    function_words = 0
    words_total = 0

    lines = get_morphosyntax_lines(transcript, imitations=False)

    for line in lines:
        line = line.split()
        words_total += len(line)
        for word in line:
            if len(word.split('-')) > 1:
                inflected_words += 1
            elif is_function_word(word):
                function_words += 1

    prop_function_words = function_words / words_total
    prop_inflected_words = inflected_words / (words_total - function_words)

    if (prop_function_words > function_words_threshold
            and prop_inflected_words > inflection_threshold):
        return len(lines), prop_function_words, prop_inflected_words, True
    else:
        return len(lines), prop_function_words, prop_inflected_words, False


def in_third_stage(transcript, threshold=0.2):
    #TODO: based on different sentence types and the appearance of mod's/aux's
    """"""

    lines = get_morphosyntax_lines(transcript, imitations=False, clean=False)
    questions = [clean_line(line) for line in lines if '?' in line]

    interrogative_with_verb = 0
    interrogative_with_aux = 0

    for question in questions:
        verb = False
        aux = False
        wordtags = question.split()
        for wordtag in wordtags:
            class_ = wordtag.split('|')[0]
            if 'v' in class_ or 'part' in class_:
                verb = True
            elif 'mod' in class_ or 'aux' in class_ or 'inf' in class_:
                aux = True
        if verb:
            interrogative_with_verb += 1
            if aux:
                interrogative_with_aux += 1

    if interrogative_with_aux / len(questions) > threshold:
        return interrogative_with_aux / len(questions), True
    else:
        return interrogative_with_aux / len(questions), False


def in_fourth_stage(transcript):
    # TODO: based on embedded sentences

    lines = get_grammar_lines(transcript, imitations=False)

    embedded_sentence = 0

    for line in lines:
        if 'XCOMP' in line:
            embedded_sentence += 1

    if embedded_sentence > 20:
        return True
    else:
        return False

def in_fifth_stage(transcript):
    # TODO: based on coordinated sentences

    pass


def get_morphosyntax_lines(transcript, speaker='CHI', clean=True,
                           imitations=True):
    """Return a list of only morphosyntactic tagging for stated speaker in the
    transcript."""

    blocks = transcript.lines_as_tuples(speakers=speaker, annotations=True,
                                        as_blocks=True)
    lines = []
    for block in blocks:
        if imitations or not ('spa', '$IMIT') in block:
            lines += block

    if clean:
        lines = [clean_line(line[1]) for line in lines if line[0] == 'mor']
    else:
        lines = [line[1] for line in lines if line[0] == 'mor']

    return lines


def get_grammar_lines(transcript, speaker='CHI', imitations=True):
    """Return a list of only grammar tagging for stated speaker in the
    transcript."""

    blocks = transcript.lines_as_tuples(speakers=speaker, annotations=True,
                                        as_blocks=True)
    lines = []
    for block in blocks:
        if imitations or not ('spa', '$IMIT') in block:
            lines += block
    lines = [clean_line(line[1]) for line in lines if line[0] == 'gra']

    return lines

def is_function_word(wordtag):
    """Return true if the word is a function word."""

    allowed_classes = {'aux',
                       'conj',
                       'coord',
                       'cop',
                       'det:art',
                       'det:dem',
                       'det:int',
                       'det:num',
                       'det:poss',
                       'inf',
                       'neg',
                       'post',
                       'prep',
                       'pro:dem',
                       'pro:exist',
                       'pro:indef',
                       'pro:int',
                       'pro:obj',
                       'pro:per',
                       'pro:poss',
                       'pro:refl',
                       'pro:rel',
                       'pro:sub', 'qn'
                       }

    if wordtag.split('|')[0] in allowed_classes:
        return True
    else:
        return False


def clean_line(line):
    """Clean a string for ' .', ' ?', ' !'"""

    remove_list = [' .', ' ?', ' !']
    for item in remove_list:
        line = line.replace(item, '')

    return line


main()
