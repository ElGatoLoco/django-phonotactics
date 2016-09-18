import re
from .mappings import lat2cir, bi2mono

def clean(text):
    """ Clean text and convert everything to uppercase. """
    text = text.upper()
    return re.sub(r'[~`!@#$%^&*()-=_+\{\}\[\]\\:\;\"\'\|\?\>\<\,\.\/QWXY]+', " ", text)

def convert2cir(text):
    """ Convert Latin script to Cyrilic."""
    for i, j in lat2cir.iteritems():
        text = text.replace(i, j)
    return text

def convert_to_monographeme(text):
    """ Convert bigraphemes to single Cyrilic."""
    for i, j in bi2mono.iteritems():
        text = text.replace(i, j)
    return text

def convert_all(text):
    """ Call all helper functions to convert Latin to Cyrilic uppercase and return list of strings. """
    return [x for x in convert_to_monographeme(convert2cir(clean(text))).split(' ') if x]
