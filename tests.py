from django.test import TestCase

from .calculator import Calculator

class TestCalculator(TestCase):
    def setUp(self):
        self.words = [
            'A','BE','DOG','HOG','HASH','BLACK','BEATLE','HATRED','MISSES','PANCAKE','RANDOMLY']
        self.c = Calculator(self.words)

    def test_get_relevant_words_1(self):
        position = 0
        segment_size = 1
        words = self.c.get_relevant_words(self.words, position, segment_size)
        self.assertEqual(len(words), 11)
        self.assertEqual(words, self.words)

    def test_get_relevant_words_2(self):
        position = 3
        segment_size = 2
        words = self.c.get_relevant_words(self.words, position, segment_size)
        self.assertEqual(len(words), 6)
        self.assertEqual(words, self.words[5:])

    def test_get_relevant_words_3(self):
        position = 1
        segment_size = 3 
        words = self.c.get_relevant_words(self.words, position, segment_size)
        self.assertEqual(len(words), 7)
        self.assertEqual(words, self.words[4:])

    def test_get_relevant_words_4(self):
        position = 1
        segment_size = 3
        words = self.c.get_relevant_words(self.words, position, segment_size, inverse=True)
        self.assertEqual(len(words), 7)
        self.assertEqual(words, [x[::-1] for x in self.words[4:]])

    def test_get_number_of_matches_1(self):
        segment = 'O'
        position = 1
        segment_size = 1
        relevant_words = self.c.get_relevant_words(self.words, position, segment_size)
        matches = self.c.get_number_of_matches(segment, position, segment_size, relevant_words)
        self.assertEqual(matches, 2)

    def test_get_number_of_matches_2(self):
        segment = 'AN'
        position = 1
        segment_size = 2
        relevant_words = self.c.get_relevant_words(self.words, position, segment_size)
        matches = self.c.get_number_of_matches(segment, position, segment_size, relevant_words)
        self.assertEqual(matches, 2)

    def test_split_into_segments_1(self):
        word = 'PASS'
        segment_size = 1
        segments = self.c.split_into_segments(word, segment_size)
        self.assertEqual([x for x in segments], ['P','A','S','S'])

    def test_split_into_segments_2(self):
        word = 'VICTORY'
        segment_size = 2
        segments = self.c.split_into_segments(word, segment_size)
        self.assertEqual([x for x in segments], ['VI','IC','CT','TO','OR','RY'])

    def test_split_into_segments_3(self):
        word = 'BLACK'
        segment_size = 3
        segments = self.c.split_into_segments(word, segment_size)
        self.assertEqual([x for x in segments], ['BLA','LAC','ACK'])

    def test_get_probability_by_segments(self):
        word = 'BANANA'
        segment_size = 2
        prob = self.c.get_probability_by_segments(self.words, word, segment_size)
        self.assertEqual(prob, 
            [
                ['BA',0],
                ['AN',2.0/9.0],
                ['NA',0],
                ['AN',0],
                ['NA',0]
            ]
        )

    def test_get_word_probability__regular_monophoneme(self):
        word = 'BANANA'
        segment_size = 1
        prob = self.c.get_word_probability(word, segment_size, 1)
        self.assertEqual([x[1] for x in prob], [3.0/11,4.0/10,2.0/9,0.0,0.0,0.0])

    def test_get_word_probability__regular_biphoneme(self):
        word = 'BANANA'
        segment_size = 2
        prob = self.c.get_word_probability(word, segment_size, 1)
        self.assertEqual([x[1] for x in prob], [0.0,2.0/9,0.0,0.0,0.0])

    def test_get_word_probability__regular_triphoneme(self):
        word = 'BEAGLE'
        segment_size = 3
        prob = self.c.get_word_probability(word, segment_size, 1)
        self.assertEqual([x[1] for x in prob], [1.0/9,0.0,0.0,0.0])

    def test_get_word_probability__inverse_monophoneme(self):
        word = 'FROG'
        segment_size = 1
        prob = self.c.get_word_probability(word, segment_size, 2)
        self.assertEqual([x[1] for x in prob], [0.0,1.0/9,2.0/10,2.0/11])

    def test_get_word_probability__inverse_biphoneme(self):
        word = 'BULLDOG'
        segment_size = 2
        prob = self.c.get_word_probability(word, segment_size, 2)
        self.assertEqual([x[1] for x in prob], [0.0,0.0,0.0,0.0,1.0/9,2.0/10])

    def test_get_word_probability__inverse_triphoneme(self):
        word = 'BULLDOG'
        segment_size = 3
        prob = self.c.get_word_probability(word, segment_size, 2)
        self.assertEqual([x[1] for x in prob], [0.0,0.0,0.0,0.0,1.0/9])

    def test_get_word_probability__combined_monophoneme(self):
        word = 'BANANANA'
        segment_size = 1
        prob = self.c.get_word_probability(word, segment_size, 3)
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

    def test_get_word_probability__combined_biphoneme(self):
        word = 'BLOG'
        segment_size = 2
        prob = self.c.get_word_probability(word, segment_size, 3)
        self.assertEqual([x[1] for x in prob], [
            (1.0/10+0.0)/2,
            0.0,
            (0.0+2.0/10)/2
        ])

    def test_get_word_probability__combined_triphoneme(self):
        word = 'HASHRED'
        segment_size = 3
        prob = self.c.get_word_probability(word, segment_size, 3)
        self.assertEqual([x[1] for x in prob], [
            (1.0/9+0.0)/2,
            (1.0/7+0.0)/2,
            0.0,
            0.0,
            (0.0+1.0/9)/2
        ])
