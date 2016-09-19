class Calculator(object):
    def __init__(self, corpus, segment_size):
        self.corpus = corpus
        self.segment_size = segment_size

    @staticmethod
    def calc_proportion(matches, total):
        """
        Simple float division placed into a static method to prevent Zero division error.
        """
        if matches and total:
            return float(matches) / float(total)
        return 0.0

    def get_relevant_words(self, position, inverse=False):
        """ 
        Filter relevant words. I.e. checking if one letter word matches biphoneme
        segment doesn't make sense nor does matching phoneme in the fifth position
        with the words shorter than five characters. 
        """
        if inverse:
            return [x[::-1] for x in self.corpus if len(x) >= position + self.segment_size]
        return [x for x in self.corpus if len(x) >= position + self.segment_size]

    def split_into_segments(self, word):
        """
        If segment size is equal to one, return list of characters. Otherwise, return
        appropriate segments.
        """
        if self.segment_size == 1:
            return list(word)
        return (word[x:x+self.segment_size] for x in range(len(word)-self.segment_size+1))

    def get_number_of_matches(self, segment, position, relevant_words):
        """
        Find out number of matching segments in the set of relevant words.
        """
        return len(filter(
            lambda x: x[position:position+self.segment_size] == segment, relevant_words)
        )

    def get_probability_for_segments(self, word, inverse=False):
        """
        Calculate probabilities for each segment.
        """
        proportions = []
        for position, segment in enumerate(self.split_into_segments(word)):
            relevant_words = self.get_relevant_words(position, inverse=inverse)
            matches = self.get_number_of_matches(segment, position, relevant_words)
            if inverse:
                segment = segment[::-1]
            proportions.append([segment,self.calc_proportion(matches,len(relevant_words))])
        if inverse:
            proportions.reverse()
        return proportions

    def get_word_probability_by_segments(self, word, prob_type):
        """
        Call the above method to calculate different probability types depending on
        parameters passed. If 'combined probability' is asked for, this method calls
        itself recursively to calculate 'regular probability' and 'inverse probability'
        for each segment, and then returns the average of the two results.
        """
        if prob_type == 1:
            return self.get_probability_for_segments(word)
        if prob_type == 2:
            return self.get_probability_for_segments(word[::-1], inverse=True)
        return [
            [i[0],(i[1]+j[1])/2] for i,j in zip(
                self.get_word_probability_by_segments(word, 1),
                self.get_word_probability_by_segments(word, 2)
            )
        ]

    def get_probs(self, word, prob_type, averaged=False):
        """
        Get probabilities for all segments of the word, sum them and average (if asked for).
        Return list of two elements, where the first one is summed/averaged probability and 
        the second one is a list of probabilities by segments.
        """
        by_segments = self.get_word_probability_by_segments(word, prob_type)
        summed = sum(x[1] for x in by_segments)
        if averaged and summed > 0:
            return [summed / (len(word)-self.segment_size+1), by_segments]
        return [summed, by_segments]
