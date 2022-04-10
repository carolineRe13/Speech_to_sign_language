
import spacy


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
