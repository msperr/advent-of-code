import math

DAY = 15
PART = 2


def get_number(n, cf_, bd_):
    if len(n) == 2:
        return '1'
    elif len(n) == 3:
        return '7'
    elif len(n) == 4:
        return '4'
    elif len(n) == 5:
        return '3' if len(n.intersection(cf_)) == 2 else '5' if len(n.intersection(bd_)) == 2 else '2'
    elif len(n) == 6:
        return '6' if len(n.intersection(cf_)) == 1 else '0' if len(n.intersection(bd_)) == 1 else '9'
    elif len(n) == 7:
        return '8'


if __name__ == '__main__':
    with open(f'input_2021/day_{DAY}_input.txt') as file:
        lines = file.readlines()
    if DAY == 1:
        if PART == 1:
            print(sum(1 for i, j in zip(lines[:-1], lines[1:]) if int(i) < int(j)))
        elif PART == 2:
            print(sum(1 for i, j in zip(lines[:-3], lines[3:]) if int(i) < int(j)))
    elif DAY == 2:
        lines = [(s.split()[0], int(s.split()[1])) for s in lines]
        if PART == 1:
            print(sum((1 if s1 == 'forward' else 0) * s2 for s1, s2 in lines) * sum(
                (1 if s1 == 'down' else -1 if s1 == 'up' else 0) * s2 for s1, s2 in lines))
        elif PART == 2:
            horizontal, depth, aim = 0, 0, 0
            for s1, s2 in lines:
                if s1 == 'forward':
                    horizontal += s2
                    depth += aim * s2
                else:
                    aim += (1 if s1 == 'down' else -1) * s2
            print(horizontal * depth)
    elif DAY == 3:
        if PART == 1:
            gamma = ['1' if c > len(lines) / 2 else '0' for c in
                     [sum(int(s[i]) for s in lines) for i in range(len(lines[0]) - 1)]]
            epsilon = ['1' if c == '0' else '0' for c in gamma]
            print(math.prod(int(''.join(c), 2) for c in [gamma, epsilon]))
        elif PART == 2:
            result = 1
            for f in [lambda x, y: '1' if x >= y / 2 else '0',
                      lambda x, y: '0' if y > x >= y / 2 or x == 0 else '1']:
                tmp = list(lines)
                for i in range(len(lines[0]) - 1):
                    tmp = [s for s in tmp if s[i] == f(sum(int(c[i]) for c in tmp), len(tmp))]
                result *= int(''.join(tmp[0]), 2)
            print(result)
    elif DAY == 4:
        bingo_input = lines[0].split(',')
        bingo_tables = [s.strip().replace('  ', ' ').split() for s in lines[2:]]
        size = len(bingo_tables[0])
        bingo_tables = [bingo_tables[i:i + size] for i in range(0, len(bingo_tables), size + 1)]
        for i in range(len(bingo_input)):
            b = bingo_input[:i + 1]
            result = [t1 for t1 in bingo_tables if any(all(s in b for s in t2) for t2 in t1) or any(
                all(t2[j] in b for t2 in t1) for j in range(size))]
            if PART == 1 and len(result) >= 1:
                print(sum(int(s) for t in result[0] for s in t if s not in b) * int(b[-1]))
                break
            elif PART == 2:
                if len(result) < len(bingo_tables):
                    bingo_tables = [t for t in bingo_tables if t not in result]
                else:
                    print(sum(int(s) for t in result[0] for s in t if s not in b) * int(b[-1]))
                    break
    elif DAY == 5:
        vents = [[[int(s3) for s3 in s2.split(',')] for s2 in s.split(' -> ')] for s in lines]
        size = max(d for s in vents for s2 in s for d in s2) + 1
        diagram = [[0] * size for i in range(size)]
        for (x1, y1), (x2, y2) in vents:
            if x1 == x2 or y1 == y2:
                for x in range(min(x1, x2), max(x1, x2) + 1):
                    for y in range(min(y1, y2), max(y1, y2) + 1):
                        diagram[x][y] += 1
            elif PART == 2:
                for template in range(abs(x2 - x1) + 1):
                    diagram[x1 + (1 if x2 >= x1 else -1) * template][y1 + (1 if y2 >= y1 else -1) * template] += 1
        print(sum(1 for d1 in diagram for d2 in d1 if d2 >= 2))
    elif DAY == 6:
        fish = [int(f) for f in lines[0].split(',')]
        fish = {n: fish.count(n) for n in range(9)}
        for i in range(80 if PART == 1 else 256):
            fish = {8 if k == 0 else k - 1: v + (fish[0] if k == 7 else 0) for k, v in fish.items()}
        print(sum(fish.values()))
    elif DAY == 7:
        crabs = [int(c) for c in lines[0].split(',')]
        if PART == 1:
            print(min(sum(abs(c - p) for c in crabs) for p in range(min(crabs), max(crabs) + 1)))
        elif PART == 2:
            print(min(
                sum(int(abs(c - p) * (abs(c - p) + 1) / 2) for c in crabs) for p in range(min(crabs), max(crabs) + 1)))
    elif DAY == 8:
        numbers = [(s.split(' ')[:10], s.strip().split(' ')[11:]) for s in lines]
        result = 0
        for n1, n2 in numbers:
            cf = set([n for n in n1 if len(n) == 2][0])
            bd = set([n for n in n1 if len(n) == 4][0]).difference(cf)
            if PART == 1:
                result += sum(1 for n in n2 if get_number(set(n), cf, bd) in ['1', '4', '7', '8'])
            elif PART == 2:
                result += int(''.join(get_number(set(n), cf, bd) for n in n2))
        print(result)
    elif DAY == 9:
        h = [[int(s2) for s2 in list(s1.strip())] for s1 in lines]
        size = len(h[0])
        p = [(i, j) for i in range(len(h)) for j in range(len(h[i])) if all(
            i2 in [-1, len(h)] or j2 in [-1, size] or h[i2][j2] > h[i][j] for i2, j2 in
            [(i - 1, j), (i + 1, j), (i, j - 1), (i, j + 1)])]
        if PART == 1:
            print(sum(h[i][j] + 1 for i, j in p))
        elif PART == 2:
            result = list()
            for i, j in p:
                visited = set()


                def process(i2, j2):
                    visited.add((i2, j2))
                    r = 1
                    for i3, j3 in [(i2 - 1, j2), (i2 + 1, j2), (i2, j2 - 1), (i2, j2 + 1)]:
                        if (i3, j3) not in visited and 0 <= i3 < len(h) and 0 <= j3 < size and h[i3][j3] < 9:
                            r += process(i3, j3)
                    return r


                result.append(process(i, j))
            print(sorted(result, reverse=True))
            print(math.prod(sorted(result, reverse=True)[:3]))
    elif DAY == 10:
        result = 0 if PART == 1 else []
        chars = {')': '(', ']': '[', '}': '{', '>': '<'}
        for line in lines:
            chunks = ''
            corrupted = False
            for s in line.strip():
                if s in chars.values():
                    chunks += s
                else:
                    if len(chunks) > 0 and chunks[-1] == chars[s][0]:
                        chunks = chunks[:-1]
                    else:
                        if PART == 1:
                            result += 3 if s == ')' else 57 if s == ']' else 1197 if s == '}' else 25137
                        corrupted = True
                        break
            if PART == 2 and not corrupted and len(chunks) > 0:
                r = 0
                for s in reversed(chunks):
                    r = 5 * r + (1 if s == '(' else 2 if s == '[' else 3 if s == '{' else 4)
                result += [r]
        if PART == 2:
            result = sorted(result)[int((len(result) - 1) / 2)]
        print(result)
    elif DAY == 11:
        levels = [[int(j) for j in list(line.strip())] for line in lines]
        size = len(levels[0])
        result = 0
        i = 1
        while PART == 2 or i <= 100:
            levels = [[j + 1 for j in line] for line in levels]
            while any(j is not None and j > 9 for line in levels for j in line):
                x, y = [(x2, y2) for x2 in range(len(levels)) for y2 in range(size) if
                        levels[x2][y2] is not None and levels[x2][y2] > 9][0]
                levels[x][y] = None
                for x2 in range(x - 1, x + 2):
                    for y2 in range(y - 1, y + 2):
                        if 0 <= x2 < len(levels) and 0 <= y2 < size and levels[x2][y2] is not None:
                            levels[x2][y2] += 1
            if PART == 2 and all(j is None for line in levels for j in line):
                print(i)
                break
            flash = [(x, y) for x in range(len(levels)) for y in range(size) if levels[x][y] is None]
            result += len(flash)
            for x, y in flash:
                levels[x][y] = 0
            i += 1
        if PART == 1:
            print(result)
    elif DAY == 12:
        paths = [d.strip().split('-') for d in lines]


        def f(path, v, n):
            if n == 'end':
                return 1
            elif all(c.islower() for c in n) and (PART == 1 or v or n == 'start') and n in path:
                return 0
            else:
                return sum(
                    f(path + [n], v or (all(c.islower() for c in n) and n in path), t if s == n else s) for s, t in
                    paths if n in [s, t])


        print(f([], False, 'start'))
    elif DAY == 13:
        points = [(int(p2) for p2 in p.strip().split(',')) for p in lines if
                  len(p) > 1 and not p.startswith('fold along')]
        fold = [(p[11] == 'x', int(p[13:].strip())) for p in lines if p.startswith('fold along')]
        final = set(points)
        for i in range(1 if PART == 1 else len(fold)):
            final = set((2 * fold[i][1] - x if fold[i][0] and x > fold[i][1] else x,
                         2 * fold[i][1] - y if not fold[i][0] and y > fold[i][1] else y) for x, y in final)
        if PART == 1:
            print(len(final))
        else:
            for i in range(max(x for _, x in final) + 1):
                print(' '.join('#' if (j, i) in final else '.' for j in range(max(x for x, _ in final) + 1)))
    elif DAY == 14:
        # noinspection PyTypeChecker
        insertions = dict([d.strip().split(' -> ') for d in lines[2:]])
        template = {k: 0 for k in insertions.keys()}
        for i in range(len(lines[0].strip()) - 1):
            template[lines[0].strip()[i:i + 2]] += 1
        for k in range(10 if PART == 1 else 40):
            curr_template = {k: 0 for k in template.keys()}
            for t, c in template.items():
                curr_template[''.join([t[0], insertions[t]])] += c
                curr_template[''.join([insertions[t], t[1]])] += c
            template = curr_template
        curr_template = {k[0]: 0 for k in template.keys()}
        for t, c in template.items():
            curr_template[t[0]] += c
        curr_template[lines[0].strip()[-1]] += 1
        print(max(curr_template.values()) - min(curr_template.values()))
    elif DAY == 15:
        risk = [[int(x) for x in y.strip()] for y in lines]
        if PART == 2:
            risk = [[(x + i - 1) % 9 + 1 for x in y] for i in range(5) for y in risk]
            risk = [[(x + i - 1) % 9 + 1 for i in range(5) for x in y] for y in risk]
        current = [[(False, len(risk) * len(risk[0]) * 9) for x in y] for y in risk]
        current[0][0] = (False, 0)
        index = 0
        while True:
            index += 1
            (x, y), v = min([((x, y), v2[1]) for y, v1 in enumerate(current) for x, v2 in enumerate(v1) if not v2[0]],
                            key=lambda v: v[1])
            if x == len(risk[0]) - 1 and y == len(risk) - 1:
                print(v)
                break
            for x2, y2 in [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)]:
                if 0 <= x2 < len(risk[0]) and 0 <= y2 < len(risk) and not current[y2][x2][0]:
                    current[y2][x2] = (False, min(current[y2][x2][1], current[y][x][1] + risk[y2][x2]))
            current[y][x] = (True, current[y][x][1])
