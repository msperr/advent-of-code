DAY = 6
PART = 2


def letter_index(s):
    return ord(s) - ord('A') + 27 if ord(s) < ord('a') else ord(s) - ord('a') + 1


if __name__ == '__main__':
    with open(f'input_2022/day_{DAY}_input.txt') as file:
        lines = file.readlines()
    if DAY == 1:
        idx = [-1] + [i for i, s in enumerate(lines) if s.strip() == ''] + [len(lines)]
        cals = sorted([sum(int(t.strip()) for t in lines[i1 + 1:i2]) for i1, i2 in zip(idx[:-1], idx[1:])])
        print(sum(c for c in cals[(-1 if PART == 1 else -3):]))
    if DAY == 2:
        lines = [s.strip().split(' ') for s in lines]
        d0, d1 = ({s: i for i, s in enumerate(c)} for c in [list('ABC'), list('XYZ')])
        if PART == 1:
            print(sum((d1[s[1]] - d0[s[0]] + 1) % 3 * 3 + d1[s[1]] + 1 for s in lines))
        else:
            print(sum(d1[s[1]] * 3 + (d0[s[0]] + d1[s[1]] - 1) % 3 + 1 for s in lines))
    if DAY == 3:
        if PART == 1:
            print(sum(letter_index([s for s in t[:int(len(t) / 2)] if s in t[int(len(t) / 2):]][0]) for t in lines))
        else:
            print(sum(letter_index([s for s in lines[i] if s in lines[i + 1] and s in lines[i + 2]][0]) for i in
                      range(0, len(lines), 3)))
    if DAY == 4:
        lines = [[[int(u) for u in t.split('-')] for t in s.strip().split(',')] for s in lines]
        print(sum(1 for s in lines if any(
            t1[0] <= t2[0 if PART == 1 else 1] and t2[1 if PART == 1 else 0] <= t1[1] for t1, t2 in zip(s, s[::-1]))))
    if DAY == 5:
        stacks = {i: [] for i in range(1, max(int((len(s) + 1) / 4) for s in lines if not s.startswith('move')) + 1)}
        actions = list()
        for s in lines:
            if '[' in s:
                for i, j in enumerate(range(1, len(s), 4), start=1):
                    if s[j] != ' ':
                        stacks[i] += s[j]
            elif s.startswith('move'):
                actions += [[int(t) for t in s.split(' ')[1:][::2]]]
        for a, b, c in actions:
            stacks[c] = stacks[b][:a][::(-1 if PART == 1 else 1)] + stacks[c]
            stacks[b] = stacks[b][a:]
        print(''.join(v[0] for v in stacks.values()))
    if DAY == 6:
        size = 4 if PART == 1 else 14
        print([i for i in range(size, len(lines[0]) + 1) if len(set(lines[0][i - size:i])) == size][0])
