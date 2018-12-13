import childes_transcripts as ts
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

def main():
    data = input('Please, input the data folder')
    transcripts = ts.load_all_from_dir(data)

    ages = [ts.age_in_months(tran.speaker_details()['CHI']['age'])
            for tran in transcripts]
    mlus = [tran.mlu() for tran in transcripts]
    #stages = [determine_stage(tran) for tran in transcripts]

    prev_stage = 1
    stages = []
    for tran in transcripts:
        stage = determine_stage(tran)
        if stage > prev_stage:
            prev_stage += 1
            stages.append(prev_stage)
        elif stage < prev_stage:
            prev_stage -= 1
            stages.append(prev_stage)
        else:
            stages.append(prev_stage)



    df = pd.DataFrame({'age': ages, 'MLU': mlus, 'stage': stages})

    print(df.head(len(df)))
    sns.lmplot('MLU', 'stage', df)
    plt.show()


class DependencyStructure:

    def __init__(self, line):

        words = line.split()
        self.words = [_Constituent(word) for word in words]
        for const in self.words:
            const.update_dependencies(self.words)

    def root(self):

        for word in self.words:
            if word.role == 'ROOT' or word.role == 'INCROOT':
                return word

        return None

    def roles(self):

        return {const.role: const for const in self.words}

    def get_item(self, index):

        return self.words[index -1]


class _Constituent:

    def __init__(self, word):

        parts = word.split('|')
        self.index = parts[0]
        self.head = parts[1]
        self.role = parts[2]
        self.dependencies = []

    def update_dependencies(self, constituents):

        for const in constituents:
            if const.head == self.index:
                self.dependencies.append(const)
                const.head = self

    def dependency_roles(self):

        return {const.role: const for const in self.dependencies}


def determine_stage(transcript):
    """Returns the number of the stage that the transcript is assessed to."""

    if in_fifth_stage(transcript) and in_fourth_stage(transcript):
        return 5
    elif in_fourth_stage(transcript) and in_third_stage(transcript):
        return 4
    elif in_third_stage(transcript) and in_second_stage(transcript):
        return 3
    elif in_second_stage(transcript):
        return 2
    elif in_first_stage(transcript):
        return 1
    elif in_zeroth_stage(transcript):
        return 0
    else:
        return -1

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
        return True
    else:
        return False


def in_first_stage(transcript):
    """Determine if the child is in/has passed the first stage of acquisition
    by checking if s/he has passed stage 0, yet not reached stage 2."""

    if not in_zeroth_stage(transcript):
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
        if len(line) < 2:
            continue
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
        return True
    else:
        return False


def in_third_stage(transcript, threshold=0.2):
    #TODO: based on different sentence types and the appearance of mod's/aux's
    """"""

    lines = get_morphosyntax_lines(transcript, imitations=False, clean=False)
    questions = [clean_line(line) for line in lines if '?' in line]
    if not questions:
        return False

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
        return True
    else:
        return False


def in_fourth_stage(transcript):
    """"""

    lines = get_grammar_lines(transcript, imitations=False)

    embedded_sentences = 0

    for line in lines:
        struct = DependencyStructure(line)
        root = struct.root()
        if root == None:
            continue
        elif 'COMP' in root.dependency_roles():
            comp = root.dependency_roles()['COMP']
            if ('SUBJ' in comp.dependency_roles() or
                'LINK' in comp.dependency_roles()):
                embedded_sentences += 1
        elif 'CMOD' in struct.roles():
            embedded_sentences += 1

    if embedded_sentences / len(lines) > 0.02:
        return True
    else:
        return False

def in_fifth_stage(transcript):
    # TODO: based on coordinated sentences

    lines = get_grammar_lines(transcript, imitations=False)

    coord_sentences = 0

    for line in lines:
        struct = DependencyStructure(line)
        root = struct.root()
        if root == None:
            continue
        elif (root.role == 'ROOT' and
              'CONJ' in root.dependency_roles()):
            conj = root.dependency_roles()['CONJ']
            if 'COORD' in conj.dependency_roles():
                coord_sentences += 1

    if coord_sentences / len(lines) > 0.005:
        return True
    else:
        return False




def get_morphosyntax_lines(transcript, speaker='CHI', clean=True,
                           imitations=True):
    """Return a list of only morphosyntactic tagging for stated speaker in the
    transcript."""

    blocks = transcript.lines_as_tuples(speakers=speaker, annotations=True,
                                        as_blocks=True)
    # filter out imitations
    lines = []
    for block in blocks:
        if imitations or not ('spa', '$IMIT') in block:
            lines += block

    if clean:
        lines = [clean_line(line[1]) for line in lines if line[0] == 'mor']
    else:
        lines = [line[1] for line in lines if line[0] == 'mor']

    return lines


def get_grammar_lines(transcript, speaker='CHI', clean=True, imitations=True):
    """Return a list of only grammar tagging for stated speaker in the
    transcript."""

    blocks = transcript.lines_as_tuples(speakers=speaker, annotations=True,
                                        as_blocks=True)
    lines = []
    for block in blocks:
        if imitations or not ('spa', '$IMIT') in block:
            lines += block

    if clean:
        lines = [clean_line(line[1]) for line in lines if line[0] == 'gra']
    else:
        lines = [line[1] for line in lines if line[0] == 'gra']

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