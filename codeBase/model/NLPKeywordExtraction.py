from string import punctuation

import spacy


def keyword_extraction(text_to_analyse):
    # en_core_web_sm  is small https://betterprogramming.pub/extract-keywords-using-spacy-in-python-4a8415478fbf
    natural_language_processor = spacy.load("en_core_web_lg")
    doc = natural_language_processor(text_to_analyse)
    print(doc.ents)
    result = []
    pos_tag = ['nsubj', 'PROPN', 'ADJ', 'NOUN', 'NUM', 'VERB']
    doc = natural_language_processor(text_to_analyse.lower())
    sentence = next(doc.sents)
    for word in sentence:
        print("%s:%s" % (word, word.dep_))
    for token in doc:
        if token.text in natural_language_processor.Defaults.stop_words or token.text in punctuation:
            continue
        if token.pos_ in pos_tag:
            result.append(token.text)

    print(result)
    return result


def keyword_extraction2(text_to_analyse):
    natural_language_processor = spacy.load('en_core_web_lg')
    parsed_text = natural_language_processor(text_to_analyse)

    subject, indirect_object, direct_object, verb, prep, object_of_preposition = "", "", "", "", "", ""

    # get token dependencies
    for text in parsed_text:
        # nsubj for subject
        if text.dep_ == "nsubj":
            subject = text.orth_
        # iobj for indirect object
        if text.dep_ == "iobj":
            indirect_object = text.orth_
        # dobj for direct object
        if text.dep_ == "dobj":
            direct_object = text.orth_
        # ROOT for verb
        if text.dep_ == "ROOT":
            verb = text.orth_
        # preposition
        if text.dep_ == "prep":
            prep = text.orth_
        # object of preposition
        if text.dep_ == "pobj":
            object_of_preposition = text.orth_

    print(subject)
    print(direct_object)
    print(indirect_object)
    print(verb)
    print(prep)
    print(object_of_preposition)

    print(spacy.explain('npadvmod'))
    print(spacy.explain('advmod'))


def keyword_extraction_removed_from_sentence(text_to_analyse):
    natural_language_processor = spacy.load('en_core_web_lg')
    parsed_text = natural_language_processor(text_to_analyse)

    list_of_words_to_remove = []
    state_of_being_verbs = ['is', 'am', 'was', 'are', 'were', 'being', 'be', 'been']

    # get token dependencies
    for text in parsed_text:
        # det for article which unfortunately also includes numerals
        if text.dep_ == "det":
            list_of_words_to_remove.append(text.orth_.lower())
        # ROOT for verb
        if text.dep_ == "ROOT":
            if any(x == text.text for x in state_of_being_verbs):
                list_of_words_to_remove.append(text.orth_.lower())

    return remove_non_keywords_from_sentence(list_of_words_to_remove, text_to_analyse)


def remove_non_keywords_from_sentence(keywords_to_remove, text_to_analyse):
    words_in_sentence = text_to_analyse.split()

    resulting_words = [word for word in words_in_sentence if word.lower() not in keywords_to_remove]
    sentence_with_only_keywords = ' '.join(resulting_words)

    print(sentence_with_only_keywords)
    return sentence_with_only_keywords


if __name__ == "__main__":
    # keyword_extraction2('The quick brown fox jumps over the lazy dog.')
    # keyword_extraction2('I visited California one year ago')
    keyword_extraction_removed_from_sentence('A man visited California one year ago')
    keyword_extraction_removed_from_sentence('I am hungry')
