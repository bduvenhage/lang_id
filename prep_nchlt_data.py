import time
from typing import List, Tuple, Optional, Dict  # noqa # pylint: disable=unused-import
import random
import json
import csv
import string


def cleanup_text(input_text: str) -> str:
    """
    Apply some basic cleanup to the input text. NOTE: Only used by the LID_ZA model.

    :param input_text: The input text.
    :return: The cleaned input text
    """

    text = input_text.lower()
    punc_to_remove = string.punctuation.replace('-', '') + '0123456789'
    text = text.translate(str.maketrans(punc_to_remove, ' ' * len(punc_to_remove)))

    text = text.replace('ã…â¡', 'š')
    text = text.replace('ï¿½', '')
    text = text.replace('ª', '')

    text = " ".join(text.split())
    text = text.strip()

    # All special characters are kept.
    return text


def shorten_sentences(sentences: List[Tuple[str, str]], min_length: int) -> List[Tuple[str, str]]:
    sentences_shortened = []  # List[Tuple[str, str]]

    for text, label in sentences:
        text_end_i = min_length

        if min_length <= len(text):
            while (text_end_i < len(text)) and (text[text_end_i] != ' '):
                text_end_i += 1

            sentences_shortened.append((text[:text_end_i], label))

    return sentences_shortened


def load_sentences_nchlt(filename: str, label: str) -> List[Tuple[str, str]]:
    sent_list = []  # type: List[Tuple[str, str]]

    # Iterate over the lines of the file
    with open(filename, 'rt') as f:
        print("Loading sentences from", filename)
        for line in f:
            if not line.startswith("<fn"):
                text = cleanup_text(line.strip())

                # if text != '':
                if 200 < len(text) < 300:
                    text_end_i = len(text)  # 30

                    while (text_end_i < len(text)) and (text[text_end_i] != ' '):
                        text_end_i += 1

                    sent_list.append((text[:text_end_i], label))
                    # sent_list.append((text, label))

    return sent_list


def save_sentences(filename: str, labelled_sentences: List[Tuple[str, str]]) -> None:
    with open(filename, 'wt') as f:
        print("Saving sentences to", filename)
        for sentence, label in labelled_sentences:
            f.write(f"{sentence}\t{label}\n")

sent_list_afr = load_sentences_nchlt("../feersum-lid-shared-task/data/afr/improved_afr.txt",
                               "afr")
sent_list_eng = load_sentences_nchlt("../feersum-lid-shared-task/data/eng/improved_eng.txt",
                               "eng")
sent_list_nbl = load_sentences_nchlt("../feersum-lid-shared-task/data/nbl/improved_nbl.txt",
                               "nbl")
sent_list_xho = load_sentences_nchlt("../feersum-lid-shared-task/data/xho/improved_xho.txt",
                               "xho")
sent_list_zul = load_sentences_nchlt("../feersum-lid-shared-task/data/zul/improved_zul.txt",
                               "zul")
sent_list_nso = load_sentences_nchlt("../feersum-lid-shared-task/data/nso/improved_nso.txt",
                               "nso")
sent_list_sot = load_sentences_nchlt("../feersum-lid-shared-task/data/sot/improved_sot.txt",
                               "sot")
sent_list_tsn = load_sentences_nchlt("../feersum-lid-shared-task/data/tsn/improved_tsn.txt",
                               "tsn")
sent_list_ssw = load_sentences_nchlt("../feersum-lid-shared-task/data/ssw/improved_ssw.txt",
                               "ssw")
sent_list_ven = load_sentences_nchlt("../feersum-lid-shared-task/data/ven/improved_ven.txt",
                               "ven")
sent_list_tso = load_sentences_nchlt("../feersum-lid-shared-task/data/tso/improved_tso.txt",
                               "tso")

random.shuffle(sent_list_afr)
random.shuffle(sent_list_eng)
random.shuffle(sent_list_nbl)
random.shuffle(sent_list_xho)
random.shuffle(sent_list_zul)
random.shuffle(sent_list_nso)
random.shuffle(sent_list_sot)
random.shuffle(sent_list_tsn)
random.shuffle(sent_list_ssw)
random.shuffle(sent_list_ven)
random.shuffle(sent_list_tso)

print("len(sent_list_afr) =", len(sent_list_afr))
print("len(sent_list_eng) =", len(sent_list_eng))
print("len(sent_list_nbl) =", len(sent_list_nbl))
print("len(sent_list_xho) =", len(sent_list_xho))
print("len(sent_list_zul) =", len(sent_list_zul))
print("len(sent_list_nso) =", len(sent_list_nso))
print("len(sent_list_sot) =", len(sent_list_sot))
print("len(sent_list_tsn) =", len(sent_list_tsn))
print("len(sent_list_ssw) =", len(sent_list_ssw))
print("len(sent_list_ven) =", len(sent_list_ven))
print("len(sent_list_tso) =", len(sent_list_tso))

training_samples = 3500  # samples per language!
testing_samples = 600  # samples per language!

sent_list_train = []
sent_list_train.extend(sent_list_afr[:training_samples])
sent_list_train.extend(sent_list_eng[:training_samples])
sent_list_train.extend(sent_list_nbl[:training_samples])
sent_list_train.extend(sent_list_nso[:training_samples])
sent_list_train.extend(sent_list_sot[:training_samples])
sent_list_train.extend(sent_list_ssw[:training_samples])
sent_list_train.extend(sent_list_tsn[:training_samples])
sent_list_train.extend(sent_list_tso[:training_samples])
sent_list_train.extend(sent_list_ven[:training_samples])
sent_list_train.extend(sent_list_xho[:training_samples])
sent_list_train.extend(sent_list_zul[:training_samples])

sent_list_test = []
sent_list_test.extend(sent_list_afr[training_samples:(training_samples + testing_samples)])
sent_list_test.extend(sent_list_eng[training_samples:(training_samples + testing_samples)])
sent_list_test.extend(sent_list_nbl[training_samples:(training_samples + testing_samples)])
sent_list_test.extend(sent_list_nso[training_samples:(training_samples + testing_samples)])
sent_list_test.extend(sent_list_sot[training_samples:(training_samples + testing_samples)])
sent_list_test.extend(sent_list_ssw[training_samples:(training_samples + testing_samples)])
sent_list_test.extend(sent_list_tsn[training_samples:(training_samples + testing_samples)])
sent_list_test.extend(sent_list_tso[training_samples:(training_samples + testing_samples)])
sent_list_test.extend(sent_list_ven[training_samples:(training_samples + testing_samples)])
sent_list_test.extend(sent_list_xho[training_samples:(training_samples + testing_samples)])
sent_list_test.extend(sent_list_zul[training_samples:(training_samples + testing_samples)])

print("training_samples:", len(sent_list_train))
print("testing_samples:", len(sent_list_test))

random.shuffle(sent_list_train)
random.shuffle(sent_list_test)

sent_list_test_shortened = shorten_sentences(sent_list_test, 15)

save_sentences("../nchlt_train.txt", sent_list_train)
save_sentences("../nchlt_test.txt", sent_list_test)

