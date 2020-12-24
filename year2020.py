import itertools
import collections
import copy
import math
import functools


def day1p1(raw_data):
    data = [int(n) for n in raw_data.split()]
    for n, m in itertools.combinations(data, 2):
        if m + n == 2020:
            return m * n


def day1p2(raw_data):
    data = [int(n) for n in raw_data.split()]
    for n, m, p in itertools.combinations(data, 3):
        if m + n + p == 2020:
            return m * n * p


def day2p1(raw_data):
    lines = raw_data.replace("-", " ").replace(": ", " ").split("\n")
    counter = 0
    for line in lines:
        n1, n2, c, p = line.split()
        if int(n1) <= p.count(c) <= int(n2):
            counter += 1
    return counter


def day2p2(raw_data):
    lines = raw_data.replace("-", " ").replace(": ", " ").split("\n")
    counter = 0
    for line in lines:
        n1, n2, c, p = line.split()
        if p[int(n1) - 1] == c and p[int(n2) - 1] != c:
            counter += 1
        elif p[int(n1) - 1] != c and p[int(n2) - 1] == c:
            counter += 1
    return counter


def day3p1(raw_data):
    lines = raw_data.split("\n")
    l = len(lines[0])
    counter = 0
    for i, line in enumerate(lines):
        if line[(3 * i) % l] == "#":
            counter += 1
    return counter


def day3p2(raw_data):
    lines = raw_data.split("\n")
    l = len(lines[0])
    c1 = c2 = c3 = c4 = c5 = 0
    for i, line in enumerate(lines):
        if line[(3 * i) % l] == "#":
            c1 += 1
        if line[i % l] == "#":
            c2 += 1
        if line[(5 * i) % l] == "#":
            c3 += 1
        if line[(7 * i) % l] == "#":
            c4 += 1
        if line[(i // 2) % l] == "#" and (i % 2) == 0:
            c5 += 1
    print(c1, c2, c3, c4, c5)
    return c1 * c2 * c3 * c4 * c5


def day4p1(raw_data):
    counter = 0
    for p in raw_data.split("\n\n"):
        password_data = p.replace(" ", ",").replace("\n", ",").rstrip(",")
        passport = {k: v for k, v in (d.split(":") for d in password_data.split(","))}
        if all(k in passport for k in "ecl pid eyr hcl byr iyr hgt".split()):
            counter += 1
    return counter


def day4p2(raw_data):
    counter = 0
    for p in raw_data.split("\n\n"):
        password_data = p.replace(" ", ",").replace("\n", ",").rstrip(",")
        passport = {k: v for k, v in (d.split(":") for d in password_data.split(","))}
        if (
            all(k in passport for k in "ecl pid eyr hcl byr iyr hgt".split())
            and 1920 <= int(passport["byr"]) <= 2002
            and 2010 <= int(passport["iyr"]) <= 2020
            and 2020 <= int(passport["eyr"]) <= 2030
            and passport["ecl"] in "amb blu brn gry grn hzl oth".split()
            and len(passport["pid"]) == 9
            and passport["pid"].isdigit()
            and len(passport["hcl"]) == 7
            and passport["hcl"][0] == "#"
            and all(c in "0123456789abcdef" for c in passport["hcl"][1:])
            and (
                passport["hgt"][-2:] == "cm"
                and 150 <= int(passport["hgt"][:-2]) <= 193
                or passport["hgt"][-2:] == "in"
                and 59 <= int(passport["hgt"][:-2]) <= 76
            )
        ):
            counter += 1
    return counter


def day5p1(raw_data):
    numbers = []
    for place in raw_data.split("\n"):
        row = place[:7].replace("B", "1").replace("F", "0")
        column = place[7:].replace("R", "1").replace("L", "0")
        number = int(row + column, 2)
        numbers.append(number)
    return max(numbers)


def day5p2(raw_data):
    numbers = []
    for place in raw_data.split("\n"):
        row = place[:7].replace("B", "1").replace("F", "0")
        column = place[7:].replace("R", "1").replace("L", "0")
        number = int(row + column, 2)
        numbers.append(number)
    numbers.sort()
    for i, n in enumerate(numbers[:-1]):
        if numbers[i + 1] == n + 2:
            return n + 1


def day6p1(raw_data):
    groups = raw_data.split("\n\n")
    count = 0
    for group in groups:
        count += len(set(group.replace("\n", "")))
    return count


def day6p2(raw_data):
    groups = raw_data.split("\n\n")
    count = 0
    for group in groups:
        answers = group.split("\n")
        common_answers = set(answers[0])
        for a in answers:
            common_answers &= set(a)
        count += len(common_answers)
    return count


def parse7(raw_data):
    raw_data = raw_data.replace(" bags", " bag").replace(".", "").replace(" bag", "")
    raw_data = raw_data.replace(" contain ", ",").replace(", ", ",")
    contain = collections.defaultdict(list)
    is_contained = collections.defaultdict(list)
    for rule in raw_data.split("\n"):
        bags = rule.split(",")
        base = bags.pop(0)
        for bag in bags[:]:
            if bag != "no other":
                quantity = int(bag.split(" ")[0])
                bag = " ".join(bag.split(" ")[1:])
                contain[base].append((quantity, bag))
                is_contained[bag].append(base)
    return contain, is_contained


def day7p1(raw_data):
    _, is_contained = parse7(raw_data)
    available_colors = set(["shiny gold"])
    stack = ["shiny gold"]
    while stack:
        for bag in is_contained[stack.pop(0)]:
            if bag not in available_colors:
                stack.append(bag)
                available_colors.add(bag)
    return len(available_colors) - 1


def day7p2(raw_data):
    contain, _ = parse7(raw_data)
    counter = 0
    stack = [(1, "shiny gold")]
    while stack:
        quantity_base, base = stack.pop(0)
        for quantity_bag, bag in contain[base]:
            quantity = quantity_base * quantity_bag
            counter += quantity
            stack.append((quantity, bag))
    return counter


def day8p1(raw_data):
    lines = raw_data.split("\n")
    acc = 0
    index = 0
    indexs = [0]
    while True:
        if "nop" in lines[index]:
            index += 1
        elif "acc" in lines[index]:
            acc += int(lines[index].split(" ")[-1])
            index += 1
        elif "jmp" in lines[index]:
            index += int(lines[index].split(" ")[-1])
        if index in indexs:
            break
        indexs.append(index)
    return acc


def day8p2(raw_data):
    raw_lines = raw_data.split("\n")
    l = len(raw_lines)
    positions = [
        i for i, line in enumerate(raw_lines) if "jmp" in line or "nop" in line
    ]
    for position in positions:
        lines = copy.copy(raw_lines)
        if "jmp" in lines[position]:
            lines[position] = lines[position].replace("jmp", "nop")
        elif "nop" in lines[position]:
            lines[position] = lines[position].replace("nop", "jmp")
        acc = 0
        index = 0
        indexs = [0]
        while True:
            if "nop" in lines[index]:
                index += 1
            elif "acc" in lines[index]:
                acc += int(lines[index].split(" ")[-1])
                index += 1
            elif "jmp" in lines[index]:
                index += int(lines[index].split(" ")[-1])
            if index in indexs or index >= l or index < 0:
                break
            indexs.append(index)
        if index == l:
            return acc


def day9p1(raw_data):
    numbers = [int(n) for n in raw_data.split()]
    for i, number in enumerate(numbers[25:]):
        if number not in (
            a + b for a, b in itertools.combinations(numbers[i : i + 25], 2)
        ):
            return number


def day9p2(raw_data):
    numbers = [int(n) for n in raw_data.split()]
    key = day9p1(raw_data)
    l = len(numbers)
    sum_before = [0]
    for i, v in enumerate(numbers):
        sum_before.append(sum_before[-1] + v)
    for i in range(2, l):
        for j in range(l - i):
            r = numbers[j : j + i]
            s = sum_before[j + i] - sum_before[j]
            if s == key:
                return min(r) + max(r)


def day10p1(raw_data):
    adapters = [int(i) for i in raw_data.split("\n")]
    adapters.sort()
    joltages = [0] + adapters + [adapters[-1] + 3]
    diff = [l - f for l, f in zip(joltages[1:], joltages[:-1])]
    return diff.count(1) * diff.count(3)


def day10p2(raw_data):
    adapters = [int(i) for i in raw_data.split("\n")]
    adapters.sort()
    joltages = collections.defaultdict(int)
    joltages[0] = 1
    for adapter in adapters:
        for i in range(1, 4):
            joltages[adapter] += joltages[adapter - i]
    return joltages[adapters[-1]]


class Seats:
    def __init__(self, raw_data):
        self.seats = [list(r) for r in raw_data.split("\n")]
        self.size = (len(self.seats), len(self.seats[0]))
        self.directions = [
            d for d in itertools.product(range(-1, 2), repeat=2) if d != (0, 0)
        ]
        self.positions_seats = []
        for i, j in itertools.product(*(range(s) for s in self.size)):
            if self.seats[i][j] != ".":
                self.positions_seats.append((i, j))
        self.close_seats = collections.defaultdict(list)
        for i, j in self.positions_seats:
            self.add_close(i, j)
        self.visible_seats = collections.defaultdict(list)
        for i, j in self.positions_seats:
            self.add_visible(i, j)

    def add_close(self, i, j):
        si, sj = self.size
        for di, dj in self.directions:
            if (
                0 <= i + di < si
                and 0 <= j + dj < sj
                and self.seats[i + di][j + dj] != "."
            ):
                self.close_seats[(i, j)].append((i + di, j + dj))

    def add_visible(self, i, j):
        si, sj = self.size
        for di, dj in self.directions:
            ii, jj = i, j
            while 0 <= ii + di < si and 0 <= jj + dj < sj:
                ii += di
                jj += dj
                if self.seats[ii][jj] != ".":
                    if (ii, jj) != (i, j):
                        self.visible_seats[(i, j)].append((ii, jj))
                    break

    def close_seats_count(self, i, j):
        count = 0
        for ii, jj in self.close_seats[(i, j)]:
            if self.seats[ii][jj] == "#":
                count += 1
        return count

    def changes_close(self):
        changes = []
        for i, j in self.positions_seats:
            count = self.close_seats_count(i, j)
            if self.seats[i][j] == "#" and count >= 4:
                changes.append((i, j, "L"))
            elif self.seats[i][j] == "L" and count == 0:
                changes.append((i, j, "#"))
        return changes

    def visible_seats_count(self, i, j):
        count = 0
        si, sj = self.size
        for ii, jj in self.visible_seats[(i, j)]:
            if self.seats[ii][jj] == "#":
                count += 1
        return count

    def changes_visible(self):
        changes = []
        for i, j in self.positions_seats:
            count = self.visible_seats_count(i, j)
            if self.seats[i][j] == "#" and count >= 5:
                changes.append((i, j, "L"))
            elif self.seats[i][j] == "L" and count == 0:
                changes.append((i, j, "#"))
        return changes

    def count(self):
        return sum(r.count("#") for r in self.seats)


def day11p1(raw_data):
    seats = Seats(raw_data)
    for _ in range(1000):
        changes = seats.changes_close()
        if not changes:
            return seats.count()
        for (i, j, v) in changes:
            seats.seats[i][j] = v


def day11p2(raw_data):
    seats = Seats(raw_data)
    for _ in range(100):
        changes = seats.changes_visible()
        if not changes:
            return seats.count()
        for (i, j, v) in changes:
            seats.seats[i][j] = v


def day12p1(raw_data):
    x, y = 0, 0
    orientation = 0
    moves = raw_data.split("\n")
    for move in moves:
        o, d = move[0], int(move[1:])
        if o == "N":
            y += d
        elif o == "S":
            y -= d
        elif o == "E":
            x += d
        elif o == "W":
            x -= d
        elif o == "F":
            if orientation == 0:
                x += d
            if orientation == 180:
                x -= d
            if orientation == 90:
                y -= d
            if orientation == 270:
                y += d
        elif "R" == o:
            orientation += d
            orientation += 360
            orientation %= 360
        elif "L" == o:
            orientation -= d
            orientation += 3600
            orientation %= 360
        else:
            print(move)
    return abs(x) + abs(y)


def day12p2(raw_data):
    wx, wy = 10, 1
    x, y = 0, 0
    moves = raw_data.split("\n")
    for move in moves:
        o, d = move[0], int(move[1:])
        if o == "N":
            wy += d
        elif o == "S":
            wy -= d
        elif o == "E":
            wx += d
        elif o == "W":
            wx -= d
        elif o == "F":
            x += wx * d
            y += wy * d
        elif "R" == o:
            wx, wy = (
                wx * (d == 0) - wx * (d == 180) - wy * (d == 270) + wy * (d == 90),
                wy * (d == 0) - wy * (d == 180) + wx * (d == 270) - wx * (d == 90),
            )
        elif "L" == o:
            wx, wy = (
                wx * (d == 0) - wx * (d == 180) + wy * (d == 270) - wy * (d == 90),
                wy * (d == 0) - wy * (d == 180) - wx * (d == 270) + wx * (d == 90),
            )
        else:
            print(move)
    return abs(x) + abs(y)


def day13p1(raw_data):
    time, buses = raw_data.split("\n")
    time = int(time)
    buses = [int(b) for b in buses.split(",") if b not in "x"]
    depart_time = math.inf
    bus_id = 0
    for b in buses:
        t = math.ceil(time / b) * b
        if depart_time > t:
            depart_time = t
            bus_id = b
    return (depart_time - time) * bus_id


def day13p2(raw_data):
    _, buses = raw_data.split("\n")
    buses = [(int(b), i) for i, b in enumerate(buses.split(",")) if b not in "x"]
    timestamp = 0
    step = 1
    for b, i in buses:
        while (timestamp + i) % b != 0:
            timestamp += step
        step = (step * b) // math.gcd(step, b)
    return timestamp


def day14p1(raw_data):
    lines = raw_data.split("\n")
    mem = {}
    for line in lines:
        if "mask" in line:
            mask = line.split(" = ")[-1]
        if "mem" in line:
            value = bin(int(line.split(" = ")[-1]))[2:].rjust(36, "0")
            addr = int(line.split("]")[0][4:])
            result = "".join([m if m != "X" else v for v, m in zip(value, mask)])
            mem[addr] = int(result, 2)
    return sum([m for m in mem.values()])


def day14p2(raw_data):
    lines = raw_data.split("\n")
    mem = {}
    for line in lines:
        if "mask" in line:
            mask = line.split(" = ")[-1]
        if "mem" in line:
            value = int(line.split(" = ")[-1])
            addr = bin(int(line.split("]")[0][4:]))[2:].rjust(36, "0")
            result = [m if m != "0" else v for v, m in zip(addr, mask)]
            positions = [i for i, v in enumerate(result) if v == "X"]
            count = result.count("X")
            for bits in itertools.product(["0", "1"], repeat=count):
                for p, b in zip(positions, bits):
                    result[p] = b
                mem[int("".join(result), 2)] = value
    return sum([m for m in mem.values()])


def day15p1(raw_data):
    numbers = [int(i) for i in raw_data.split(",")]
    while len(numbers) < 2020:
        if numbers[-1] not in numbers[:-1]:
            numbers.append(0)
        else:
            numbers.append(1 + numbers[-2::-1].index(numbers[-1]))
    return numbers[2019]


def day15p2(raw_data):
    numbers = [int(i) for i in raw_data.split(",")]
    positions = [-1] * 30_000_000
    for i, n in enumerate(numbers[:-1]):
        positions[n] = i + 1
    number = numbers[-1]
    for index in range(len(numbers), 30_000_000):
        p = positions[number]
        if p == -1:
            new_number = 0
        else:
            new_number = index - p
        positions[number] = index
        number = new_number
    return number


def day16p1(raw_data):
    rules, my_ticket, tickets = raw_data.split("\n\n")
    rules = [
        [[int(v) for v in r.split("-")] for r in rule.split(": ")[-1].split("or")]
        for rule in rules.split("\n")
    ]
    tickets = [
        [int(v) for v in ticket.split(",")] for ticket in tickets.split("\n")[1:]
    ]
    count = 0
    for ticket in tickets:
        for value in ticket:
            if all(
                not ((r1[0] <= value <= r1[1]) or (r2[0] <= value <= r2[1]))
                for r1, r2 in rules
            ):
                count += value
    return count


def day16p2(raw_data):
    rules_raw, my_ticket, tickets = raw_data.split("\n\n")
    rules = [
        [[int(v) for v in r.split("-")] for r in rule.split(": ")[-1].split("or")]
        for rule in rules_raw.split("\n")
    ]
    tickets = [
        [int(v) for v in ticket.split(",")] for ticket in tickets.split("\n")[1:]
    ]
    my_ticket = [int(v) for v in my_ticket.split("\n")[1].split(",")]
    rules_number = len(rules)

    # combinations is a list of list of rule index that are valid for all valid tickets
    combinations = [[*range(rules_number)] for _ in range(rules_number)]
    for ticket in tickets:
        if all(
            any(
                [
                    (r1[0] <= value <= r1[1]) or (r2[0] <= value <= r2[1])
                    for r1, r2 in rules
                ]
            )
            for value in ticket
        ):
            combinations = [
                [
                    c
                    for c in comb
                    if (rules[c][0][0] <= v <= rules[c][0][1])
                    or (rules[c][1][0] <= v <= rules[c][1][1])
                ]
                for v, comb in zip(ticket, combinations)
            ]

    comb = [None for c in combinations]
    while any(len(c) > 0 for c in combinations):
        for i in range(rules_number):
            if len(combinations[i]) == 1:
                comb[i] = combinations[i][0]
                for c in combinations:
                    if comb[i] in c:
                        c.remove(comb[i])

    count = 1
    list_rules = rules_raw.split("\n")
    for i, c in enumerate(comb):
        if "departure" in list_rules[c]:
            count *= my_ticket[i]
    return count


class ConwayND:
    def __init__(self, raw_data, dim):
        cube = [r for r in raw_data.split("\n")]
        self.dir = [
            d for d in itertools.product(range(-1, 2), repeat=dim) if d != (0,) * dim
        ]
        self.active = set()
        for i, j in itertools.product(range(len(cube)), range(len(cube[0]))):
            if cube[i][j] == "#":
                self.active.add(tuple([i, j] + [0] * (dim - 2)))

    def iteration(self):
        counter = collections.defaultdict(int)
        for position, di in itertools.product(self.active, self.dir):
            neighbor = tuple(p + d for p, d in zip(position, di))
            counter[neighbor] += 1

        self.active = {
            position
            for position, count in counter.items()
            if (count == 3 or (count == 2 and position in self.active))
        }


def day17p1(raw_data):
    cube = ConwayND(raw_data, 3)
    for _ in range(6):
        cube.iteration()
    return len(cube.active)


def day17p2(raw_data):
    cube = ConwayND(raw_data, 4)
    for _ in range(6):
        cube.iteration()
    return len(cube.active)


def add(a, b):
    return a + b


def mul(a, b):
    return a * b


def evaluate(items):
    operators = {"+": add, "*": mul}
    value = 0
    operator = None
    while items:
        item = items.pop(0)
        if item == "(":
            count = 1
            inside = []
            while count > 0:
                item = items.pop(0)
                if item == "(":
                    count += 1
                elif item == ")":
                    count -= 1
                if count > 0:
                    inside.append(item)
            item = evaluate(inside)
        if item not in ("+", "*"):
            if operator is not None:
                value = operator(value, int(item))
            else:
                value = int(item)
        elif item in ("+", "*"):
            operator = operators[item]

    return value


def evaluate2(items):
    left = []
    if "*" not in items:
        return evaluate(items)
    value = None
    while items:
        item = items.pop(0)
        if item == "(":
            count = 1
            inside = []
            while count > 0:
                item = items.pop(0)
                if item == "(":
                    count += 1
                elif item == ")":
                    count -= 1
                if count > 0:
                    inside.append(item)
            item = evaluate2(inside)
        if item == "*":
            value = (evaluate2(left or [1]) or 1) * (evaluate2(items or [1]) or 1)
            left = [value]
        else:
            left.append(item)
    return evaluate2(left + items)


def day18p1(raw_data):
    lines = raw_data.split("\n")
    count = 0
    for line in lines:
        items = line.replace("(", " ( ").replace(")", " ) ").split()
        count += evaluate(items)
    return count


def day18p2(raw_data):
    lines = raw_data.split("\n")
    count = 0
    for line in lines:
        items = line.replace("(", " ( ").replace(")", " ) ").split()
        count += evaluate2(items)
    return count







def expand(l):
    return [v for ll in l for v in ll]



class Rule:
    def __init__(self, rules_str: str, max_size = math.inf):
        self.max_size = max_size
        self.rules = [
            [int(v) for v in s.split(" ") if v.isdigit()]
            for s in rules_str.split(" | ")
        ]
        self.rules = [r for r in self.rules if len(r)]
        self.valids = [
            "".join(v.replace('"', "") for v in s.split(" ") if not v.isdigit())
            for s in rules_str.split(" | ")
        ]
        self.valids = [v for v in self.valids if len(v)]


    def eval(self, rules):
        for rule in self.rules:
            for combinations in itertools.product(
                    *(rules[rule_id].valids for rule_id in rule)
                    ):
                valid_message = ''.join(combinations)
                self.valids.append(''.join(combinations))




def day19p1(raw_data):
    rules_data, messages = raw_data.split("\n\n")
    max_size = max(len(m) for m in messages.split('\n'))
    rules ={
        int(i): Rule(s, max_size) for i, s in (r.split(": ") for r in rules_data.split("\n"))
        }
    stack = [0] # node list to visit
    backtrack = []
    while stack:
        i = stack.pop(0)
        next_rules = {j for j in set(expand(rules[i].rules)) if isinstance(j, int)}
        if next_rules:
            for j in next_rules:
                stack.append(j)
            backtrack.append(i)
    backtrack.reverse()
    visited = set()
    for i in backtrack:
        if i not in visited:
            rules[i].eval(rules)
            visited.add(i)
    print(len(rules[0].valids))
    return len(set(rules[0].valids) & {m for m in messages.split('\n')})

def day19p2(raw_data):
    rules_data, messages = raw_data.split("\n\n")
    max_size = max(len(m) for m in messages.split('\n'))
    rules ={
        int(i): Rule(s, max_size) for i, s in (r.split(": ") for r in rules_data.split("\n"))
        }
    stack = [0] # node list to visit
    backtrack = []
    while stack:
        i = stack.pop(0)
        next_rules = {j for j in set(expand(rules[i].rules)) if isinstance(j, int)}
        if next_rules:
            for j in next_rules:
                stack.append(j)
            backtrack.append(i)
    backtrack.reverse()
    visited = set()
    for i in backtrack:
        if i not in visited:
            rules[i].eval(rules)
            visited.add(i)
            rules[i].valids = [v for v in rules[i].valids if len(v)]
    print(len(rules[0].valids))
    return len(set(rules[0].valids) & {m for m in messages.split('\n')})

def day20p1(raw_data):
    sides = collections.defaultdict(list)
    neighbors_count = collections.defaultdict(int)
    for tile_data in raw_data.split("\n\n"):
        tile_data_lines = tile_data.split("\n")
        tile_id = int(tile_data_lines.pop(0).split(" ")[-1][:-1])
        sides[tile_data_lines[0]].append(tile_id)
        sides[tile_data_lines[-1]].append(tile_id)
        sides[tile_data_lines[0][::-1]].append(tile_id)
        sides[tile_data_lines[-1][::-1]].append(tile_id)
        transposed_tile = [''.join(c) for c in zip(*tile_data_lines)]
        sides[transposed_tile[0]].append(tile_id)
        sides[transposed_tile[-1]].append(tile_id)
        sides[transposed_tile[0][::-1]].append(tile_id)
        sides[transposed_tile[-1][::-1]].append(tile_id)
    for side, list_tile in sides.items():
        for tile in list_tile:
            neighbors_count[tile] += len(list_tile) - 1
    for tile_id in neighbors_count:
        neighbors_count[tile_id] //= 2
    product_corner_id = 1
    for tile_id, count in neighbors_count.items():
        if count == 2:
            product_corner_id *= tile_id
    return product_corner_id

def day20p2(raw_data):
    tiles = {}
    for tile_data in raw_data.split("\n\n"):
        lines = tile_data.split("\n")
        tiles[int(lines[0].split(" ")[-1][:-1])] = lines[1:]
    size = len(lines) - 1
    return 2



def day21p1(raw_data):
    foods_list = []
    allergens_list = []
    for line in raw_data.split('\n'):
        line = line.replace(",", "")
        foods, allergens = line[:-1].split(" (contains ")
        foods_list.append(set(foods.split(" ")))
        allergens_list.append(set(allergens.split(" ")))

    all_ingredient = set()
    for food in foods_list:
        all_ingredient |= food

    possible_ingredient = collections.defaultdict(lambda: copy.copy(all_ingredient))
    for food, allergens in zip(foods_list, allergens_list):
        for allergen in allergens:
            possible_ingredient[allergen] &= food

    cannot_contain_allergen = all_ingredient
    for allergen, ingredients in possible_ingredient.items():
        cannot_contain_allergen -= ingredients

    return sum(len(ingredients & cannot_contain_allergen) for ingredients in foods_list)


def day21p2(raw_data):
    foods_list = []
    allergens_list = []
    for line in raw_data.split('\n'):
        line = line.replace(",", "")
        foods, allergens = line[:-1].split(" (contains ")
        foods_list.append(set(foods.split(" ")))
        allergens_list.append(set(allergens.split(" ")))

    all_ingredient = set()
    for food in foods_list:
        all_ingredient |= food

    possible_ingredient = collections.defaultdict(lambda: copy.copy(all_ingredient))
    for food, allergens in zip(foods_list, allergens_list):
        for allergen in allergens:
            possible_ingredient[allergen] &= food

    for _ in range(len(possible_ingredient)):
        for allergen, ingredients in possible_ingredient.items():
            if len(ingredients) == 1:
                for other_allergen in possible_ingredient:
                    if allergen != other_allergen:
                        possible_ingredient[other_allergen] -= ingredients

    allergen_per_ingredient = {}
    for allergen, ingredients in possible_ingredient.items():
        assert len(ingredients) == 1
        allergen_per_ingredient[list(ingredients)[0]] = allergen
    list_ingredients = sorted(
            (ingredient for ingredient in allergen_per_ingredient),
            key = lambda i:allergen_per_ingredient[i])
    return ','.join(list_ingredients)

def day22p1(raw_data):
    player1_data, player2_data = raw_data.split('\n\n')
    deck1 = [int(i) for i in player1_data.split("\n")[1:]]
    deck2 = [int(i) for i in player2_data.split("\n")[1:]]
    while deck1 and deck2:
        card1, card2 = deck1.pop(0), deck2.pop(0)
        if card1 > card2:
            deck1 += [card1, card2]
        elif card2 > card1:
            deck2 += [card2, card1]
        else: print('====')
    count = 0
    deck = deck1 + deck2
    deck.reverse()
    for i,c in enumerate(deck):
        count += c * (i + 1)
    return count


def recursive_game(deck1, deck2): # return True if player 1 wins
    previous1, previous2 = set(), set()
    while deck1 and deck2:
        t1, t2 = tuple(deck1), tuple(deck2)
        if t1 in previous1 or t2 in previous2:
            return True
        previous1.add(t1)
        previous2.add(t2)
        card1, card2 = deck1.pop(0), deck2.pop(0)
        if len(deck1) >= card1 and len(deck2) >= card2:
            if recursive_game(copy.copy(deck1[:card1]), copy.copy(deck2[:card2])):
                deck1 += [card1, card2]
            else:
                deck2 += [card2, card1]
        else:
            if card1 > card2:
                deck1 += [card1, card2]
            elif card2 > card1:
                deck2 += [card2, card1]
    if deck1:
        return True
    return False




def day22p2(raw_data):
    player1_data, player2_data = raw_data.split('\n\n')
    deck1 = [int(i) for i in player1_data.split("\n")[1:]]
    deck2 = [int(i) for i in player2_data.split("\n")[1:]]
    recursive_game(deck1, deck2)
    count = 0
    deck = deck1 + deck2
    deck.reverse()
    for i,c in enumerate(deck):
        count += c * (i + 1)
    return count


def day23p1(raw_data):
    cups = [int(i) - 1 for i in raw_data]
    number = len(cups)
    index = 0 # index of the current cup
    for _ in range(100):
        current_cup = cups[index]
        index = (index + 1) % number
        picked_cups = []
        for _ in range(3):
            if index < len(cups):
                picked_cups.append(cups.pop(index))
            else:
                picked_cups.append(cups.pop(0))
        target = (current_cup - 1 + number) % number
        while target in picked_cups:
            target  = (target - 1 + number) % number
        target_index = cups.index(target)
        for i, c in enumerate(picked_cups):
            cups.insert(i + 1 + target_index, c)
        while cups[index-1] != current_cup:
            cups = cups[-1:] + cups[:-1]
    while cups[0] != 0:
            cups = cups[-1:] + cups[:-1]
    return ''.join([str(c + 1) for c in cups[1:]])


def day23p2(raw_data):
    input_cups = [int(i) for i in raw_data]
    max_input = max(input_cups)
    max_cup_value = 1_000_000

    cups = [i + 1 for i in range(max_cup_value + 1)] # list that take the role of a linked list
    for c1, c2 in zip(input_cups[:-1], input_cups[1:]):
        cups[c1] = c2
    cups[input_cups[-1]] = max_input + 1
    cups[max_cup_value] = input_cups[0] # loop back to 0 

    cup = input_cups[0] # initialize at the first cup
    for _ in range(10_000_000):
        picked = [cups[cup]]
        picked.append(cups[picked[-1]])
        picked.append(cups[picked[-1]])
        target = cup - 1 or max_cup_value
        while target in picked:
            target = target - 1 or max_cup_value
        cups[cup], cups[picked[-1]], cups[target] = cups[picked[-1]], cups[target], picked[0]
        cup = cups[cup]

    return cups[1] * cups[cups[1]]


def day24p1(raw_data):
    black_tile = set()
    # position 2D (x, y)
    # e => (1, 0)
    # w => (-1 , 0)
    # nw => (-1, 1)
    # se => (1, -1)
    # ne => (0, 1)
    # sw => (0, -1)
    for line in raw_data.split("\n"):
        count_NW = line.count("nw")
        count_SW = line.count("sw")
        count_NE = line.count("ne")
        count_SE = line.count("se")
        count_E = line.count("e") - count_NE - count_SE
        count_W = line.count("w") - count_NW - count_SW
        position = (
                count_E + count_SE - count_W - count_NW,
                count_NE + count_NW - count_SW - count_SE
                )
        if position in black_tile:
            black_tile.remove(position)
        else:
            black_tile.add(position)

    return len(black_tile)




def day24p2(raw_data):
    black_tile = set()
    # position 2D (x, y)
    # e => (1, 0)
    # w => (-1 , 0)
    # nw => (-1, 1)
    # se => (1, -1)
    # ne => (0, 1)
    # sw => (0, -1)
    for line in raw_data.split("\n"):
        count_NW = line.count("nw")
        count_SW = line.count("sw")
        count_NE = line.count("ne")
        count_SE = line.count("se")
        count_E = line.count("e") - count_NE - count_SE
        count_W = line.count("w") - count_NW - count_SW
        position = (
                count_E + count_SE - count_W - count_NW,
                count_NE + count_NW - count_SW - count_SE
                )
        if position in black_tile:
            black_tile.remove(position)
        else:
            black_tile.add(position)
    directions = {(1, 0), (-1, 0), (-1, 1), (1, -1), (0, 1), (0, -1)}
    for _ in range(100):
        count = collections.defaultdict(int)
        for x, y in black_tile:
            for dx, dy in directions:
                count[(x + dx, y + dy)] += 1
        black_tile = (
                { tile for tile in black_tile if 1 <= count[tile] <= 2 } |
                { tile for tile in count if count[tile] == 2 and tile not in black_tile }
                )
    return len(black_tile)




