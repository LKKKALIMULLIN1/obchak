import json

def solve(d):
    ans = "```\n"
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
                ans += f"{key} should pay to {k} ===>>> {pos_d[key]}\n"
                neg_d[k] += pos_d[key]
                pos_d[key] = 0
                break
            else:
                ans += f'{key} should pay to {k} ===>>> {-neg_d[k]}\n'
                pos_d[key] += neg_d[k]
                neg_d[k] = 0
    ans += '```'
    return ans


def count(names, cnt):
    f = open('data.txt').readline
    arr = []
    for i in range(cnt):
        arr.append(json.loads(f()[:-1]))
    d = {}
    for i in names:
        d[i] = 0
    for mas in arr:
        mas = mas[2:]
        summ = mas[1] / (len(names) - (len(mas[2])))
        d[mas[0]] -= mas[1]
        for j in names:
            if j not in mas[2]:
                d[j] += summ
    return(solve(d))