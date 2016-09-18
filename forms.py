from django import forms

from .models import Word
from .widgets import RadioCustomRenderer, IntegerRangeWidget

SEGMENT = (
    (1,'Monophoneme'),
    (2,'Biphoneme'),
    (3,'Triphoneme'),
)

PROPORTION = (
    (1,'Regular'),
    (2,'Inverted'),
    (3,'Combined'),
)

SUM_OR_AV = (
    (1,'Summed'),
    (2,'Averaged'),
)

class MainForm(forms.Form):
    segment_size = forms.ChoiceField(
        choices=SEGMENT, 
        initial=SEGMENT[0][0],
        widget=forms.RadioSelect(renderer=RadioCustomRenderer)
    )
    probability_type = forms.ChoiceField(
        choices=PROPORTION, 
        initial=PROPORTION[0][0],
        widget=forms.RadioSelect(renderer=RadioCustomRenderer)
    )
    summed_or_averaged = forms.ChoiceField(
        choices=SUM_OR_AV, 
        initial=SUM_OR_AV[1][0],
        widget=forms.RadioSelect(renderer=RadioCustomRenderer)
    )
    number_of_words_in_corpus = forms.CharField(
        widget=IntegerRangeWidget(attrs={
            'min_value':10,
            'max_value':Word.objects.count(),
            'default':Word.objects.count(),
        }))


class TextForm(forms.Form):
    text = forms.CharField(label='',widget=forms.Textarea(attrs={
            'placeholder':"Enter text here. Any character that doesn't belong to the Serbian alphabet (including white space) will be interpreted as a separator.",
            'spellcheck':'false'
        }))

    def __init__(self, *args, **kwargs):
        super(TextForm, self).__init__(*args, **kwargs)
        self.fields['text'].widget.attrs['class'] = 'col-xs-12 text-area'