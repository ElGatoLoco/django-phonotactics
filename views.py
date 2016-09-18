from django.shortcuts import render
from django.views.generic.edit import FormView
from formtools.wizard.views import SessionWizardView

from collections import OrderedDict

from .calculator import Calculator
from .forms import MainForm, TextForm, SEGMENT, PROPORTION, SUM_OR_AV
from .models import Word
from .utils import convert_all

class CalculatorWizard(SessionWizardView):
    form_list = [MainForm, TextForm]
    template_name = 'wizard_form.html'

    def done(self, form_list, **kwargs):
        # GET PARAMETERS FROM FORM
        probability_type = int(form_list[0].cleaned_data.get('probability_type'))
        segment_size = int(form_list[0].cleaned_data.get('segment_size'))
        sum_or_average = int(form_list[0].cleaned_data.get('summed_or_averaged'))
        num_of_words = int(form_list[0].cleaned_data.get('number_of_words_in_corpus'))

        # GET WORDS FROM FORM AND CONVERT THEM TO CYRILLIC UPPERCASE
        text = form_list[1].cleaned_data.get('text')
        if text:
            text = set(convert_all(text))

        # INSTANTIATE CALCULATOR AND PASS CORPUS (OR PART OF IT)
        c = Calculator([x['word'] for x in Word.objects.values()][:num_of_words])

        probs = {}
        for word in text:
            # FOR EVERY WORD GET SEGMENT AND SUMMED PROBABILITIES AND CALCULATE SUM
            by_segment = c.get_word_probability(word, segment_size, probability_type)
            summed_prob = float(sum(x[1] for x in by_segment))
            if sum_or_average == 1:
                # IF SUMMED PROBABILITY - PLACE SUMMED PROBABILITY INTO A DICT
                probs[word] = [summed_prob, by_segment]
            elif summed_prob > 0:
                # ELSE, CHECK IF SUM GREATER THAN ZERO AND AVERAGE IT, THEN PLACE INTO A DICT
                probs[word] = [summed_prob/(len(word)-segment_size+1), by_segment]
            else:
                # IF ZERO, PLACE ZERO INSTEAD
                probs[word] = [0.0, by_segment]

        return render(self.request, 'done.html', {
            # PUT PROBABILITIES INTO AN ORDERED DICT AND ORDER THEM DESCENDING
            'probability': OrderedDict(sorted(probs.items(), key=lambda x: x[1])),
            # PASS INPUT PARAMETERS TO CONTEXT
            'info': [[  'Segment size', OrderedDict(SEGMENT)[segment_size]],
                     [  'Probability type', OrderedDict(PROPORTION)[probability_type]],
                     [  'Summed or averaged', OrderedDict(SUM_OR_AV)[sum_or_average]],
                     [  'Number of words in corpus', num_of_words]
                    ],
        })