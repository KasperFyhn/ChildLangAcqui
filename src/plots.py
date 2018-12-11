def plot_word_freqs(words, transcripts, speaker='CHI'):
    """Show a plot of proportional frequencies for each given word with the age
    of the child in months on the x-axis."""

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
    """Show a plot of the summed proportional frequencies of a given wordgroup
    with the age of the child in months on the x-axis."""

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


def plot_ttr_over_time(transcripts, child='CHI', speakers=('CHI', 'MOT'),
                       disregard=()):
    """Show a plot of the type-to-token-ratio over time with the age of the
    child in months on the x-axis. As a default, the comparison is made with
    the target child and the mother. In case the child has another name code
    than 'CHI', this should be corrected in order to retrieve the age in each
    transcript."""

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