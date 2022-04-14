import argparse
import itertools
import os
from collections import Counter, OrderedDict
import trstop.trstop
from tqdm import tqdm
import pandas as pd
import nltk
import re

nltk.download('punkt')
from nltk.tokenize import word_tokenize, sent_tokenize


def step_step_process(fname, out):
    # step1 tokenize text
    print("step1: Tokenizing text...")

    num_lines = sum(1 for line in open(fname, 'r'))
    article = []
    with open(fname, 'r') as f:
        for line in tqdm(f, total=num_lines):
            s = line.strip()
            count = word_tokenize(s)
            article.append(count)

    # step2 clean numbers and punc
    print("step2: Cleaning numbers and punctitons...")

    article2 = []
    for i in tqdm(range(len(article))):
        for y in range(0, len(article[i])):
            # print(reports[i][y])
            word = article[i][y]
            word = re.sub(r'[^\w\s]', '', word)
            word = re.sub(r'[0-9]+', '', word)
            word = word.lower()
            article2.append(word)

    # step3 clean empty words
    print("step3: Removing empty words...")

    article3 = [x for x in article2 if x]

    # step4 remove stop words
    print("step4: Removing stop words...")

    article4 = []

    for i in tqdm(range(len(article3))):
        for y in range(0, len(article3[i])):
            if (trstop.trstop.is_stop_word(article3[i][y]) == False):
                # print(word)
                article4.append(word)

    # step5 remove again empty words

    print("step5: Removing empty words again...")

    article5 = [x for x in article4 if x]

    # step6 find co-occurrence
    print("step6: Finding co-occurrence...")

    article6 = list(itertools.chain.from_iterable(article5))
    count = Counter(article6)
    ordered_count = OrderedDict(count.most_common())

    # step7 print to xlsx file
    print("step7: Printing to xlsx file...")

    df_clean_article = pd.DataFrame.from_dict(ordered_count, orient='index').reset_index()
    df_clean_article.to_excel(out)


parser = argparse.ArgumentParser()
parser.add_argument(
    "--txtfile",
    default=None,
    metavar="path",
    type=str,
    required=True,
    help="txt file path",
)
parser.add_argument(
    "--out",
    default=None,
    metavar="path",
    type=str,
    required=True,
    help="out xlsx path",
)

args = parser.parse_args()

fname = args.txtfile
out = args.out
step_step_process(fname, out)
