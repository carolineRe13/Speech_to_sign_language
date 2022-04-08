from string import punctuation

import spacy


def keyword_extraction(text_to_analyse):
    natural_language_processor = spacy.load("en_core_web_lg")
    doc = natural_language_processor(text_to_analyse)
    print(doc.ents)
    result = []
    pos_tag = ['PROPN', 'ADJ', 'NOUN', 'NUM', 'VERB']
    doc = natural_language_processor(text_to_analyse.lower())
    for token in doc:
        if token.text in natural_language_processor.Defaults.stop_words or token.text in punctuation:
            continue
        if token.pos_ in pos_tag:
            result.append(token.text)

    print(result)
    return result


if __name__ == "__main__":
    keyword_extraction('I would like to buy two apples')
