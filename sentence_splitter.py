from quntoken import tokenize

for tok in tokenize(open('pandas.txt')):
    print(tok, end='')
