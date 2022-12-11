f = open("Obchak.txt").readline
n = int(f())
names = f().split()
d = {}
for i in names:
    d[i] = 0
for i in range(n):
    s = f().split()
    # if '\n' in s[-1]: s[-1] = s[-1][:-1]
    for i in range(len(s)):
        if i == 1: s[1] = int(s[1])
        else: s[i] = s[i].lower()
    summ = s[1] / (len(names) - (len(s) - 2))
    d[s[0]] -= s[1]
    if s[0] not in s[2:]: d[s[0]] += summ
    for j in names:
        if j not in s:
            d[j] += summ
pos_d = {}
neg_d = {}
for key, value in d.items():
    if value > 0: pos_d[key] = value
    else: neg_d[key] = value
pos_d = dict(sorted(pos_d.items(), key=lambda item: item[1], reverse=True))
neg_d = dict(sorted(neg_d.items(), key=lambda item: item[1]))
for key, value in pos_d.items():
    for k, v in neg_d.items():
        if v == 0: continue
        if pos_d[key] + neg_d[k] <= 0:
            print(f'{key} should pay to {k} ===>>> {pos_d[key]}')
            neg_d[k] += pos_d[key]
            pos_d[key] = 0
            break
        else:
            print(f'{key} should pay to {k} ===>>> {-neg_d[k]}')
            pos_d[key] += neg_d[k]
            neg_d[k] = 0
input()