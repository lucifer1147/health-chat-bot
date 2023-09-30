import sys
import time
start = time.time()
if '--no-time' not in sys.argv:
    print("Loading getAsked.py...", end="\t")

import spacy

nlp = spacy.load('en_core_web_sm')

no_append_words = ['precaution', 'prevention', 'preventative', 'sign', 'symptom', 'treatment', 'vaccine', 'management']
catLi_li = [('precaution', ['precaution', 'prevention', 'preventative']), ('symptoms', ['sign', 'symptom']), ('treatment', ['treatment', 'vaccine', 'management'])]

def get_asked(sent: str):
    doc=nlp(sent)

    disease_asked = []
    disease_criterion = None

    toks = [tok.dep_ for tok in doc]

    if 'poss' in toks:
        disease_criterion = ['poss']
    elif 'nsubj' in toks:
        disease_criterion = ['pobj'] if 'pobj' in toks else ['nsubj']
    elif 'its' in sent or 'them' in sent or 'their' in sent:
        disease_asked = ['last one(s)']
    elif 'dobj' in toks and 'prep' in toks:
        disease_criterion = ['pobj']

    if disease_criterion is not None:
        for idx, tok in enumerate(doc):
            tok_str = str(tok)
            in_no_append = False

            for word in no_append_words:
                if word in tok_str.lower() or tok_str.lower() in word:
                    in_no_append = True
                    break

            if tok.dep_ in disease_criterion and not in_no_append:
                if doc[idx-1].dep_ in ['amod', 'nmod']:
                    disease_asked.append(str(doc[idx-1])+' '+tok_str)
                else:
                    disease_asked.append(tok_str)
            elif tok.dep_ in ['conj']:
                for word in disease_asked:
                    if str(doc[idx-2]) in word and not in_no_append:
                        disease_asked.append(tok_str)

    cat_asked = []

    for cat, words in catLi_li:
        for word in words:
            if word in sent.lower():
                cat_asked.append(cat)

    if cat_asked == []:
        cat_asked = ['about']

    return disease_asked, cat_asked

end = time.time()
if '--no-time' not in sys.argv:
    print(f"Loaded getAsked.py in {round(end-start)/10}s")
