import transcripts as ts

transcripts = ts.load_all_from_dir('/Users/kasperfyhnjacobsen/Desktop/Brown/Adam')

ts.plot_prop_word_freqs(['i', 'mom'], transcripts)