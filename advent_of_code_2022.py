import functools
import math
import sys

import mip

DAY = 24
PART = 2


def letter_index(s):
    return ord(s) - ord('A') + 27 if ord(s) < ord('a') else ord(s) - ord('a') + 1


class Node:
    def __init__(self, predecessor):
        self.predecessor, self.subdirectories, self.size = predecessor, dict(), 0

    def recursive_size(self):
        return self.size + sum(n.recursive_size() for n in self.subdirectories.values())


class Monkey:
    def __init__(self):
        self.items, self.operation, self.test, self.true_monkey, self.false_monkey = [], None, None, None, None

    def operate(self, item):
        a, b = (item if self.operation[i] == 'old' else int(self.operation[i]) for i in [2, 4])
        return a * b if self.operation[3] == '*' else a + b

    def next_monkey(self, item):
        return self.true_monkey if item % self.test == 0 else self.false_monkey


def dist(trees):
    blockers = [i for i, t in enumerate(trees[1:], start=1) if t >= trees[0]]
    return len(trees) - 1 if len(blockers) == 0 else blockers[0]


def compare(a, b):
    if isinstance(a, int) and isinstance(b, int):
        return None if a == b else a < b
    elif isinstance(a, list) and isinstance(b, list):
        for x, y in zip(a, b):
            c = compare(x, y)
            if c is not None:
                return c
        if len(a) != len(b):
            return len(a) < len(b)
    else:
        return compare([a] if isinstance(a, int) else a, [b] if isinstance(b, int) else b)


def move(i, j, grid, directions):
    if not any(grid[i - 1][j - 1:j + 2] + [grid[i][j - 1], grid[i][j + 1]] + grid[i + 1][j - 1:j + 2]):
        return i, j
    for d in directions:
        if not any(grid[i + x][j + y] for x, y in d):
            return i + d[1][0], j + d[1][1]
    return i, j


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
    if DAY == 7:
        node = Node(None)
        directories = [node]
        for line in lines[1:]:
            s = line.strip().split(' ')
            if s[0] == '$':
                if s[1] == 'cd':
                    if s[2] == '..':
                        node = node.predecessor
                    else:
                        node = node.subdirectories[s[2]]
                        directories += [node]
            elif s[0] == 'dir':
                node.subdirectories[s[1]] = Node(node)
            else:
                node.size += int(s[0])
        sizes = [n.recursive_size() for n in directories]
        if PART == 1:
            print(sum(s for s in sizes if s <= 100000))
        else:
            print(sorted(s for s in sizes if s >= 30000000 - 70000000 + sizes[0])[0])
    if DAY == 8:
        lines = [[int(t) for t in s.strip()] for s in lines]
        if PART == 1:
            print(4 * (len(lines) - 1) + sum(
                1 for i, s in enumerate(lines[1:-1], start=1) for j, t in enumerate(s[1:-1], start=1) if
                t > max(lines[i][:j]) or t > max(lines[i][j + 1:]) or t > max(s2[j] for s2 in lines[:i]) or t > max(
                    s2[j] for s2 in lines[i + 1:])))
        else:
            print(max(dist(s[:j + 1][::-1]) * dist(s[j:]) * dist([s2[j] for s2 in lines[:i + 1][::-1]]) * dist(
                [s2[j] for s2 in lines[i:]]) for i, s in enumerate(lines) for j, t in enumerate(s)))
    if DAY == 9:
        knots = [(0, 0) for i in range(2 if PART == 1 else 10)]
        positions = {tuple(knots[-1])}
        for s in lines:
            d, w = s.strip().split(' ')
            d = (1, 0) if d == 'R' else (0, 1) if d == 'U' else (-1, 0) if d == 'L' else (0, -1)
            for a in range(int(w)):
                knots[0] = tuple(knots[0][i] + d[i] for i in range(len(knots[0])))
                for j in range(1, len(knots)):
                    if any(abs(knots[j - 1][i] - knots[j][i]) > 1 for i in range(len(knots[0]))):
                        knots[j] = tuple(knots[j][i] + (
                            0 if knots[j - 1][i] == knots[j][i] else (knots[j - 1][i] - knots[j][i]) / abs(
                                knots[j - 1][i] - knots[j][i])) for i in range(len(knots[0])))
                positions.add(tuple(knots[-1]))
        print(len(positions))
    if DAY == 10:
        lines = [t for s in [[0] if s.strip() == 'noop' else [0, int(s.strip().split(' ')[1])] for s in lines] for t in
                 s]
        if PART == 1:
            print(sum(i * (1 + sum(lines[:i - 1])) for i in range(20, 221, 40)))
        else:
            register = 1
            screen = ''
            for i, s in enumerate(lines[:240]):
                screen += '#' if register - 1 <= i % 40 <= register + 1 else '.'
                register += s
            for i, j in zip(range(0, 201, 40), range(40, 241, 40)):
                print(screen[i:j])
    if DAY == 11:
        monkeys = []
        monkey = None
        for s in lines:
            t = s.strip().split(' ')
            if t[0] == 'Monkey':
                monkey = Monkey()
                monkeys += [monkey]
            elif t[0] == 'Starting':
                monkey.items = [int(x) for x in s.strip()[16:].split(', ')]
            elif t[0] == 'Operation:':
                monkey.operation = t[1:]
            elif t[0] == 'Test:':
                monkey.test = int(t[3])
            elif t[0] == 'If':
                if t[1] == 'true:':
                    monkey.true_monkey = int(t[5])
                else:
                    monkey.false_monkey = int(t[5])
        inspections = [0] * len(monkeys)
        for _ in range(20 if PART == 1 else 10000):
            for i, monkey in enumerate(monkeys):
                for item in monkey.items:
                    new_item = monkey.operate(item)
                    new_item = new_item // 3 if PART == 1 else new_item % (math.prod(m.test for m in monkeys))
                    monkeys[monkey.next_monkey(new_item)].items += [new_item]
                    inspections[i] += 1
                monkey.items = []
        inspections = sorted(inspections, reverse=True)
        print(inspections[0] * inspections[1])
    if DAY == 12:
        lines = [[t for t in s.strip()] for s in lines]
        height = [['a' if t == 'S' else 'z' if t == 'E' else t for t in s] for s in lines]
        distances = [[0 if t == ('S' if PART == 1 else 'E') else len(lines) * len(lines[0]) for t in s] for s in lines]
        visited = set()
        while True:
            i, j = sorted([(i, j, distances[i][j]) for i, s in enumerate(lines) for j, t in enumerate(s) if
                           (i, j) not in visited], key=lambda x: x[2])[0][:2]
            if lines[i][j] == 'E' if PART == 1 else height[i][j] == 'a':
                print(distances[i][j])
                break
            x = lines[i][j]
            visited.add((i, j))
            for i2, j2 in [(i2, j2) for i2, j2 in [(i - 1, j), (i + 1, j), (i, j - 1), (i, j + 1)] if
                           0 <= i2 < len(lines) and 0 <= j2 < len(lines[0]) and (i2, j2) not in visited and (
                           ord(height[i2][j2]) <= ord(height[i][j]) + 1 if PART == 1 else ord(height[i][j]) <= ord(
                                   height[i2][j2]) + 1)]:
                distances[i2][j2] = min(distances[i2][j2], distances[i][j] + 1)
    if DAY == 13:
        pairs = [(eval(lines[i].strip()), eval(lines[i + 1].strip())) for i in range(0, len(lines), 3)]
        if PART == 1:
            print(sum(i for i, p in enumerate(pairs, start=1) if compare(*p)))
        else:
            dividers = [[[2]], [[6]]]
            pairs = sorted([x for p in pairs for x in p] + dividers,
                           key=functools.cmp_to_key(lambda x, y: -1 if compare(x, y) else 1))
            print(math.prod(i for i, s in enumerate(pairs, start=1) if s in dividers))
    if DAY == 14:
        lines = [[[int(a) for a in t.split(',')] for t in s.strip().split(' -> ')] for s in lines]
        rock, sand = set(), set()
        for s in lines:
            for t1, t2 in zip(s[:-1], s[1:]):
                rock.update([(i, t1[1]) for i in range(min(t1[0], t2[0]), max(t1[0], t2[0]) + 1)])
                rock.update([(t1[0], i) for i in range(min(t1[1], t2[1]), max(t1[1], t2[1]) + 1)])
        finished = False
        while True:
            s = (500, 0)
            while True:
                if PART == 1 and s[1] >= max(t[1] for t in rock):
                    finished = True
                    break
                new_position = False
                for p in [(s[0], s[1] + 1), (s[0] - 1, s[1] + 1), (s[0] + 1, s[1] + 1)]:
                    if p not in rock.union(sand) and p[1] <= max(t[1] for t in rock) + 1:
                        s = p
                        new_position = True
                        break
                if not new_position:
                    sand.add(s)
                    if PART == 2 and s == (500, 0):
                        finished = True
                    break
            if finished:
                break
        print(len(sand))
    if DAY == 16:
        lines = {s.split(' ')[1]: (int(s.split(' ')[4][5:-1]), [t[:-1] for t in s.split(' ')[9:]]) for s in lines}
        steps = 30 if PART == 1 else 26
        model = mip.Model()
        x = {(n, t, d): model.add_var(f'x({n},{t},{d})', var_type=mip.BINARY) for n, v in lines.items() for t in
             [n] + v[1] for d in range(steps)}
        for node in lines.keys():
            for time in range(steps - 1):
                model += mip.xsum(v for (_, t, d), v in x.items() if t == node and d == time) == mip.xsum(
                    v for (s, _, d), v in x.items() if s == node and d == time + 1)
            model += mip.xsum(v for (s, _, d), v in x.items() if s == node and d == 0) == (
                0 if node != 'AA' else 1 if PART == 1 else 2)
            model += mip.xsum(v for (s, t, _), v in x.items() if s == node and t == node) <= 1
        model.objective = mip.xsum(v * (steps - 1 - d) * lines[s][0] for (s, t, d), v in x.items() if s == t)
        model.sense = mip.MAXIMIZE
        model.verbose = 0
        model.optimize()
        print(int(model.objective_value))
    if DAY == 17:
        types = [[(i, 0) for i in range(4)], [(1, 0), (0, 1), (1, 1), (2, 1), (1, 2)],
                 [(0, 0), (1, 0), (2, 0), (2, 1), (2, 2)], [(0, i) for i in range(4)], [(0, 0), (1, 0), (0, 1), (1, 1)]]
        rock = dict()
        i, p = 0, 0
        item = [(x + 2, y + (-1 if len(rock) == 0 else max(k for k, v in rock.items() if len(v) > 0)) + 4) for x, y
                in types[i % len(types)]]
        rock.update({k: set() for k in range(len(rock), max(j[1] for j in item) + 1)})
        while True:
            push = 1 if lines[0].strip()[p] == '>' else -1
            if p == len(lines[0].strip()) - 1:
                print(i, max(k for k, v in rock.items() if len(v) > 0),
                      rock[max(k for k, v in rock.items() if len(v) > 0)])
            p = (p + 1) % len(lines[0].strip())
            if not any(x + push < 0 or 6 < x + push or x + push in rock[y] for x, y in item):
                item = [(x + push, y) for x, y in item]
            if any(y == 0 or x in rock[y - 1] for x, y in item):
                for x, y in item:
                    rock[y].add(x)
                i += 1
                if i == 100:
                    break
                item = [(x + 2, y + (-1 if len(rock) == 0 else max(k for k, v in rock.items() if len(v) > 0)) + 4) for
                        x, y in types[i % 5]]
                rock.update({k: set() for k in range(len(rock), max(j[1] for j in item) + 1)})
            else:
                item = [(x, y - 1) for x, y in item]
        print(rock)
        print(max(k for k, v in rock.items() if len(v) > 0) + 1)
    if DAY == 18:
        lines = [[int(t) for t in s.strip().split(',')] for s in lines]
        size = [max(s[i] for s in lines) + 3 for i in range(3)]
        grid = [[[False for _ in range(size[2])] for _ in range(size[1])] for _ in range(size[0])]
        for s in lines:
            grid[s[0]+1][s[1]+1][s[2]+1] = True
        if PART == 1:
            print(sum(
                1 for x in range(size[0]) for y in range(size[1]) for a, b in zip(range(size[2] - 1), range(1, size[2]))
                if grid[x][y][a] != grid[x][y][b]) + sum(
                1 for x in range(size[0]) for z in range(size[2]) for a, b in zip(range(size[1] - 1), range(1, size[1]))
                if grid[x][a][z] != grid[x][b][z]) + sum(
                1 for y in range(size[1]) for z in range(size[2]) for a, b in zip(range(size[0] - 1), range(1, size[0]))
                if grid[a][y][z] != grid[b][y][z]))
        else:
            visited = [[[not any(grid[x2][y2][z2] for x2, y2, z2 in
                                 [(x2, y2, z2) for x2 in range(x - 1, x + 2) for y2 in range(y - 1, y + 2) for z2 in
                                  range(z - 1, z + 2)] if 0 <= x2 < size[0] and 0 <= y2 < size[1] and 0 <= z2 < size[2])
                         for z in range(size[2])] for y in range(size[1])] for x in range(size[0])]
            start = [(x, y, z) for x in range(size[0]) for y in range(size[1]) for z in range(size[2]) if
                     not grid[x][y][z] and not visited[x][y][z]][0]

            def f(x, y, z):
                visited[x][y][z] = True
                result = sum(1 if grid[x2][y2][z2] else f(x2, y2, z2) for x2, y2, z2 in
                                                   [(x - 1, y, z), (x + 1, y, z), (x, y - 1, z), (x, y + 1, z),
                                                    (x, y, z - 1), (x, y, z + 1)] if
                                                   0 <= x2 < size[0] and 0 <= y2 < size[1] and 0 <= z2 < size[2] and
                                                   not visited[x2][y2][z2])
                return result

            sys.setrecursionlimit(sum(1 for x in range(size[0]) for y in range(size[1]) for z in range(size[2]) if
                                      not grid[x][y][z] and not visited[x][y][z]))
            print(f(*start))
    if DAY == 19:
        lines = [s.strip().split(' ') for s in (lines if PART == 1 else lines[:3])]
        lines = {int(s[1][:-1]): [int(s[i]) for i in [6, 12, 18, 21, 27, 30]] for s in lines}
        goods = ['ore', 'clay', 'obsidian', 'geode']
        steps = 24 if PART == 1 else 32
        result = dict()
        for i, s in lines.items():
            model = mip.Model()
            x = {j: {r: model.add_var(f'x({j},{r})', var_type=mip.BINARY) for r in goods} for j in range(steps)}
            for j in range(steps):
                model += j + mip.xsum((j - k - 1) * x[k]['ore'] for k in range(j)) >= mip.xsum(
                    s[0] * x[k][goods[0]] + s[1] * x[k][goods[1]] + s[2] * x[k][goods[2]] + s[4] * x[k][goods[3]] for k
                    in range(j + 1)), f'ore({j})'
                model += mip.xsum((j - k - 1) * x[k]['clay'] for k in range(j)) >= mip.xsum(
                    s[3] * x[k][goods[2]] for k in range(1 + j)), f'clay({j})'
                model += mip.xsum((j - k - 1) * x[k]['obsidian'] for k in range(j)) >= mip.xsum(
                    s[5] * x[k][goods[3]] for k in range(1 + j)), f'obsidian({j})'
                model += mip.xsum(x[j][g] for g in goods) <= 1
            model.objective = mip.xsum((steps - j - 1) * x[j][goods[3]] for j in range(steps))
            model.sense = mip.MAXIMIZE
            model.verbose = 0
            model.optimize()
            result[i] = int(model.objective_value)
        if PART == 1:
            print(sum(i * r for i, r in result.items()))
        else:
            print(math.prod(result.values()))
    if DAY == 23:
        grid = [[t == '#' for t in s.strip()] for s in lines]
        directions = [[(-1, a) for a in range(-1, 2)], [(1, a) for a in range(-1, 2)], [(a, -1) for a in range(-1, 2)],
                      [(a, 1) for a in range(-1, 2)]]
        index = 1
        while index <= 10 or PART == 2:
            if any(grid[0]):
                grid = [[False for _ in grid[0]]] + grid
            if any(grid[-1]):
                grid = grid + [[False for _ in grid[0]]]
            if any(s[0] for s in grid):
                grid = [[False] + s for s in grid]
            if any(s[-1] for s in grid):
                grid = [s + [False] for s in grid]
            moves = dict()
            suppose = [[0 for _ in s] for s in grid]
            for i, j in [(i, j) for i, s in enumerate(grid) for j, t in enumerate(s) if t]:
                x, y = move(i, j, grid, directions)
                moves[(i, j)] = (x, y)
                suppose[x][y] += 1
            grid = [[False for _ in s] for s in grid]
            for (i, j), (x, y) in moves.items():
                if suppose[x][y] <= 1:
                    grid[x][y] = True
                else:
                    grid[i][j] = True
            if PART == 2 and all((i, j) == (x, y) or suppose[x][y] >= 2 for (i, j), (x, y) in moves.items()):
                break
            directions = directions[1:] + [directions[0]]
            index += 1
        if PART == 1:
            north = min(i for i, s in enumerate(grid) if any(s))
            south = max(i for i, s in enumerate(grid) if any(s))
            west = min(j for j in range(len(grid[0])) if any(s[j] for s in grid))
            east = max(j for j in range(len(grid[0])) if any(s[j] for s in grid))
            print(sum(1 for s in grid[north:south + 1] for t in s[west:east + 1] if not t))
        else:
            print(index)
    if DAY == 24:
        grid = [[([] if t == '.' else [t]) for t in s.strip()[1:-1]] for s in lines[1:-1]]
        moves = {'^': (-1, 0), 'v': (1, 0), '<': (0, -1), '>': (0, 1)}
        index = 0
        for source, target in [(0, -1)] if PART == 1 else [(0, -1), (-1, 0), (0, -1)]:
            position = [[False for _ in s] for s in grid]
            while True:
                index += 1
                grid = [[[k for k, v in moves.items() if k in grid[(i - v[0]) % len(grid)][(j - v[1]) % (len(
                    grid[0]))]] for j, t in enumerate(s)] for i, s in enumerate(grid)]
                if position[target][target]:
                    break
                position = [[len(t) == 0 and ((i, j) == (source % len(grid), source % len(grid[0])) or any(
                    position[x][y] for x, y in [(i - 1, j), (i, j), (i + 1, j), (i, j - 1), (i, j + 1)] if
                    0 <= x < len(grid) and 0 <= y < len(grid[0]))) for j, t in enumerate(s)] for i, s in
                            enumerate(grid)]
        print(index)
