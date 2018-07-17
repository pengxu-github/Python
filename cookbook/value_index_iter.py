from collections import defaultdict

word_summary = defaultdict(list)

with open('value_index_iter.py', 'r') as f:
    lines = f.readlines()

for idx, line in enumerate(lines, 1):
    # print(idx, line)
    # Create a list  of words in current line
    words = [w.strip().lower() for w in line.split()]
    for word in words:
        word_summary[word].append(idx)

print(word_summary.items())
for k in word_summary:
    print('{} : {}'.format(k, word_summary[k]))
