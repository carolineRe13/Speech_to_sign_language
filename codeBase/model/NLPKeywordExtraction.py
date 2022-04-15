import spacy
from flask import app

STATE_OF_BEING_VERBS = ['is', 'am', 'was', 'are', 'were', 'being', 'be', 'been']


def keyword_extraction_removed_from_sentence(text_to_analyse):
    """
        This method filters out words from a text which are not used in ASL
    """
    natural_language_processor = spacy.load('en_core_web_sm')
    parsed_text = natural_language_processor(text_to_analyse)

    list_of_words_to_remove = []

    for text in parsed_text:
        # det for article excluding numerals
        if text.dep_ == "det":
            list_of_words_to_remove.append(text.orth_.lower())
        # ROOT for verb
        if text.dep_ == "ROOT":
            if any(x == text.text for x in STATE_OF_BEING_VERBS):
                list_of_words_to_remove.append(text.orth_.lower())

    return remove_non_keywords_from_sentence(list_of_words_to_remove, text_to_analyse)


def remove_non_keywords_from_sentence(keywords_to_remove, text_to_analyse):
    """
        Words are removed from original text
    """
    words_in_sentence = text_to_analyse.split()

    resulting_words = [word for word in words_in_sentence if word.lower() not in keywords_to_remove]
    sentence_with_only_keywords = ' '.join(resulting_words)

    app.logger.info('Sentence with only keywords: ' + sentence_with_only_keywords)
    return sentence_with_only_keywords

