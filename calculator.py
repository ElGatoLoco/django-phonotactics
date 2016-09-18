class Calculator(object):
    def __init__(self, corpus):
        self.corpus = corpus

    def get_relevant_words(self, all_words, position, segment_size, inverse=False):
        """ 
        Filter relevant words. I.e. checking if one letter word matches biphoneme
        segment doesn't make sense. 
        """
        if inverse:
            return [x[::-1] for x in all_words if len(x) >= position + segment_size]
        return [x for x in all_words if len(x) >= position + segment_size]

    def split_into_segments(self, word, segment_size):
        """
        If segment size is equal to one, return list of letters. Otherwise, return
        appropriate segments.
        """
        if segment_size == 1:
            return list(word)
        return (word[x:x+segment_size] for x in range(len(word)-segment_size+1))

    def get_number_of_matches(self, segment, position, segment_size, relevant_words):
        """
        Find out number of matching segments in the set of relevant words.
        """
        return len(filter(lambda x: x[position:position+segment_size] == segment, relevant_words))

    def calc_proportion(self, matches, total):
        """
        Simple float division placed into a function to prevent Zero division error.
        """
        if matches and total:
            return float(matches) / float(total)
        return 0.0

    def get_probability_by_segments(self, corpus, word, segment_size, inverse=False):
        """
        Calculate probabilities for each segment.
        """
        proportions = []
        for position, segment in enumerate(self.split_into_segments(word, segment_size)):
            relevant_words = self.get_relevant_words(corpus, position, segment_size, inverse=inverse)
            matches = self.get_number_of_matches(segment, position, segment_size, relevant_words)
            if inverse:
                segment = segment[::-1]
            proportions.append([segment,self.calc_proportion(matches,len(relevant_words))])
        if inverse:
            proportions.reverse()
        return proportions

    def get_word_probability(self, word, segment_size, prob_type):
        """
        Call the above method to calculate different probability types depending on
        parameters passed. If 'combined probability' is asked for, this method calls
        itself recursively to calculate 'regular probability' and 'inverse probability'
        for each segment, and then returns the average of the two results.
        """
        if prob_type == 1:
            return self.get_probability_by_segments(self.corpus, word, segment_size)
        if prob_type == 2:
            return self.get_probability_by_segments(
                self.corpus, word[::-1], segment_size, inverse=True)
        return [
            [i[0],(i[1]+j[1])/2] for i,j in zip(
                self.get_word_probability(word, segment_size, 1),
                self.get_word_probability(word, segment_size, 2)
            )
        ]
