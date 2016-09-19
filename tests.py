from django.test import TestCase

from .calculator import Calculator

class TestCalculator(TestCase):
    def setUp(self):
        self.corpus = [
            'A','BE','DOG','HOG','HASH','BLACK','BEATLE','HATRED','MISSES','PANCAKE','RANDOMLY']

    def test_get_relevant_words_1(self):
        c = Calculator(self.corpus, 1)
        position = 0
        words = c.get_relevant_words(position)
        self.assertEqual(len(words), 11)
        self.assertEqual(words, self.corpus)

    def test_get_relevant_words_2(self):
        c = Calculator(self.corpus, 2)
        position = 3
        words = c.get_relevant_words(position)
        self.assertEqual(len(words), 6)
        self.assertEqual(words, self.corpus[5:])

    def test_get_relevant_words_3(self):
        c = Calculator(self.corpus, 3)
        position = 1
        words = c.get_relevant_words(position)
        self.assertEqual(len(words), 7)
        self.assertEqual(words, self.corpus[4:])

    def test_get_relevant_words_4(self):
        c = Calculator(self.corpus, 3)
        position = 1
        words = c.get_relevant_words(position, inverse=True)
        self.assertEqual(len(words), 7)
        self.assertEqual(words, [x[::-1] for x in self.corpus[4:]])

    def test_get_number_of_matches_1(self):
        segment_size = 1
        c = Calculator(self.corpus, segment_size)
        segment = 'O'
        position = 1
        relevant_words = c.get_relevant_words(position)
        matches = c.get_number_of_matches(segment, position, relevant_words)
        self.assertEqual(matches, 2)

    def test_get_number_of_matches_2(self):
        segment_size = 2
        c = Calculator(self.corpus, segment_size)
        segment = 'AN'
        position = 1
        relevant_words = c.get_relevant_words(position)
        matches = c.get_number_of_matches(segment, position, relevant_words)
        self.assertEqual(matches, 2)

    def test_split_into_segments_1(self):
        word = 'PASS'
        c = Calculator(self.corpus, 1)
        segments = c.split_into_segments(word)
        self.assertEqual([x for x in segments], ['P','A','S','S'])

    def test_split_into_segments_2(self):
        word = 'VICTORY'
        c = Calculator(self.corpus, 2)
        segments = c.split_into_segments(word)
        self.assertEqual([x for x in segments], ['VI','IC','CT','TO','OR','RY'])

    def test_split_into_segments_3(self):
        word = 'BLACK'
        c = Calculator(self.corpus, 3)
        segments = c.split_into_segments(word)
        self.assertEqual([x for x in segments], ['BLA','LAC','ACK'])

    def test_get_probability_for_segments(self):
        word = 'BANANA'
        segment_size = 2
        c = Calculator(self.corpus, segment_size)
        prob = c.get_probability_for_segments(word)
        self.assertEqual(prob, 
            [
                ['BA',0],
                ['AN',2.0/9.0],
                ['NA',0],
                ['AN',0],
                ['NA',0]
            ]
        )

    def test_get_word_probability_by_segments__regular_monophoneme(self):
        word = 'BANANA'
        segment_size = 1
        c = Calculator(self.corpus, segment_size)
        prob = c.get_word_probability_by_segments(word, 1)
        self.assertEqual([x[1] for x in prob], [3.0/11,4.0/10,2.0/9,0.0,0.0,0.0])

    def test_get_word_probability_by_segments__regular_biphoneme(self):
        word = 'BANANA'
        segment_size = 2
        c = Calculator(self.corpus, segment_size)
        prob = c.get_word_probability_by_segments(word, 1)
        self.assertEqual([x[1] for x in prob], [0.0,2.0/9,0.0,0.0,0.0])

    def test_get_word_probability_by_segments__regular_triphoneme(self):
        word = 'BEAGLE'
        segment_size = 3
        c = Calculator(self.corpus, segment_size)
        prob = c.get_word_probability_by_segments(word, 1)
        self.assertEqual([x[1] for x in prob], [1.0/9,0.0,0.0,0.0])

    def test_get_word_probability_by_segments__inverse_monophoneme(self):
        word = 'FROG'
        segment_size = 1
        c = Calculator(self.corpus, segment_size)
        prob = c.get_word_probability_by_segments(word, 2)
        self.assertEqual([x[1] for x in prob], [0.0,1.0/9,2.0/10,2.0/11])

    def test_get_word_probability_by_segments__inverse_biphoneme(self):
        word = 'BULLDOG'
        segment_size = 2
        c = Calculator(self.corpus, segment_size)
        prob = c.get_word_probability_by_segments(word, 2)
        self.assertEqual([x[1] for x in prob], [0.0,0.0,0.0,0.0,1.0/9,2.0/10])

    def test_get_word_probability_by_segments__inverse_triphoneme(self):
        word = 'BULLDOG'
        segment_size = 3
        c = Calculator(self.corpus, segment_size)
        prob = c.get_word_probability_by_segments(word, 2)
        self.assertEqual([x[1] for x in prob], [0.0,0.0,0.0,0.0,1.0/9])

    def test_get_word_probability_by_segments__combined_monophoneme(self):
        word = 'BANANANA'
        segment_size = 1
        c = Calculator(self.corpus, segment_size)
        prob = c.get_word_probability_by_segments(word, 3)
        self.assertEqual([x[1] for x in prob], [
            (3.0/11+0.0)/2,
            (4.0/10+1.0/2)/2,
            (2.0/9+1.0/5)/2,
            (0.0+1.0/6)/2,
            0.0,
            (0.0+3.0/9)/2,
            0.0,
            (0.0+1.0/11)/2
        ])

    def test_get_word_probability_by_segments__combined_biphoneme(self):
        word = 'BLOG'
        segment_size = 2
        c = Calculator(self.corpus, segment_size)
        prob = c.get_word_probability_by_segments(word, 3)
        self.assertEqual([x[1] for x in prob], [
            (1.0/10+0.0)/2,
            0.0,
            (0.0+2.0/10)/2
        ])

    def test_get_word_probability_by_segments__combined_triphoneme(self):
        word = 'HASHRED'
        segment_size = 3
        c = Calculator(self.corpus, segment_size)
        prob = c.get_word_probability_by_segments(word, 3)
        self.assertEqual([x[1] for x in prob], [
            (1.0/9+0.0)/2,
            (1.0/7+0.0)/2,
            0.0,
            0.0,
            (0.0+1.0/9)/2
        ])
