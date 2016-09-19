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
        # GET PARAMETERS FROM THE FIRST FORM
        probability_type = int(form_list[0].cleaned_data.get('probability_type'))
        segment_size = int(form_list[0].cleaned_data.get('segment_size'))
        sum_or_average = int(form_list[0].cleaned_data.get('summed_or_averaged'))
        num_of_words = int(form_list[0].cleaned_data.get('number_of_words_in_corpus'))

        # GET WORDS FROM THE SECOND FORM AND CONVERT THEM TO CYRILLIC UPPERCASE
        text = form_list[1].cleaned_data.get('text')
        if text:
            text = set(convert_all(text))

        # INSTANTIATE CALCULATOR AND PASS CORPUS (OR PART OF IT) AND SEGMENT SIZE
        c = Calculator(
            [x['word'] for x in Word.objects.values()][:num_of_words],
            segment_size
        )

        # DETERMINE WHETHER WORD PROBABILITIES SHOULD BE AVERAGED
        averaged = True if sum_or_average == 2 else False

        # CALCULATE PROBABILITIES FOR ALL OF THE WORDS ENTERED
        probs = {}
        for word in text:
            probs[word] = c.get_probs(word, probability_type, averaged)

        return render(self.request, 'done.html', {
            # PUT PROBABILITIES INTO AN ORDERED DICT AND ORDER THEM DESCENDING
            'probability': OrderedDict(sorted(probs.items(), key=lambda x: x[1])),
            # PASS INPUT PARAMETERS TO THE CONTEXT
            'info': [[  'Segment size', OrderedDict(SEGMENT)[segment_size]],
                     [  'Probability type', OrderedDict(PROPORTION)[probability_type]],
                     [  'Summed or averaged', OrderedDict(SUM_OR_AV)[sum_or_average]],
                     [  'Number of words in corpus', num_of_words]
                    ],
        })