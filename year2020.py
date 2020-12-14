import itertools
import collections
import copy
import math


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
    groups = raw_data.split('\n\n')
    count = 0
    for group in groups:
        count += len(set(group.replace('\n','')))
    return count

def day6p2(raw_data):
    groups = raw_data.split('\n\n')
    count = 0
    for group in groups:
        answers = group.split('\n')
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
    for rule in raw_data.split('\n'):
        bags = rule.split(',')
        base = bags.pop(0)
        for bag in bags[:]:
            if bag != "no other":
                quantity = int(bag.split(' ')[0])
                bag = ' '.join(bag.split(' ')[1:])
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
    contain, _= parse7(raw_data)
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
    lines = raw_data.split('\n')
    acc = 0
    index = 0
    indexs = [0]
    while True:
        if "nop" in lines[index]:
            index += 1
        elif "acc" in lines[index]:
            acc += int(lines[index].split(' ')[-1])
            index += 1
        elif "jmp" in lines[index]:
            index += int(lines[index].split(' ')[-1])
        if index in indexs:
            break
        indexs.append(index)
    return acc


def day8p2(raw_data):
    raw_lines = raw_data.split('\n')
    l = len(raw_lines)
    positions = [i for i, line in enumerate(raw_lines) if "jmp" in line or "nop" in line]
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
                acc += int(lines[index].split(' ')[-1])
                index += 1
            elif "jmp" in lines[index]:
                index += int(lines[index].split(' ')[-1])
            if index in indexs or index >= l or index < 0:
                break
            indexs.append(index)
        if index == l:
            return acc


def day9p1(raw_data):
    numbers = [int(n) for n in raw_data.split()]
    for i, number in enumerate(numbers[25:]):
        if number not in (a + b for a,b in itertools.combinations(numbers[i:i + 25], 2)):
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
            r = numbers[j:j + i]
            s = sum_before[j + i] - sum_before[j]
            if s == key:
                return min(r) + max(r)


def day10p1(raw_data):
    adapters = [int(i) for i in raw_data.split('\n')]
    adapters.sort()
    joltages = [0] + adapters + [adapters[-1] + 3]
    diff = [l - f for l, f in zip(joltages[1:], joltages[:-1])]
    return diff.count(1) * diff.count(3)


def day10p2(raw_data):
    adapters =[int(i) for i in raw_data.split('\n')]
    adapters.sort()
    joltages = collections.defaultdict(int)
    joltages[0] = 1
    for adapter in adapters:
        for i in range(1, 4):
            joltages[adapter] += joltages[adapter -i]
    return joltages[adapters[-1]]



class Seats:
    def __init__(self, raw_data):
        self.seats = [list(r) for r in raw_data.split('\n')]
        self.size = (len(self.seats), len(self.seats[0]))
        self.directions = [d for d in itertools.product(range(-1, 2), repeat=2)if d != ( 0, 0)]
        self.positions_seats = []
        for i, j in itertools.product(*(range(s) for s in self.size)):
            if self.seats[i][j] != '.':
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
            if 0 <= i + di < si and 0 <= j + dj < sj and self.seats[i + di][j + dj] != '.':
                self.close_seats[(i, j)].append((i + di, j + dj))

    def add_visible(self, i, j):
        si, sj = self.size
        for di, dj in self.directions:
            ii, jj = i, j
            while 0 <= ii + di < si and 0 <= jj + dj < sj:
                ii += di
                jj += dj
                if self.seats[ii][jj] != '.':
                    if (ii, jj) != (i, j):
                        self.visible_seats[(i, j)].append((ii, jj))
                    break

    def close_seats_count(self, i, j):
        count = 0
        for ii, jj in self.close_seats[(i, j)]:
            if self.seats[ii][jj] == '#':
                count += 1
        return count

    def changes_close(self):
        changes = []
        for i, j in self.positions_seats:
            count = self.close_seats_count(i, j)
            if self.seats[i][j] == '#' and count >= 4:
                changes.append((i, j, 'L'))
            elif self.seats[i][j] == 'L' and count == 0:
                changes.append((i, j, '#'))
        return changes

    def visible_seats_count(self, i, j):
        count = 0
        si, sj = self.size
        for ii, jj in self.visible_seats[(i, j)]:
            if self.seats[ii][jj] == '#':
                count += 1
        return count

    def changes_visible(self):
        changes = []
        for i, j in self.positions_seats:
            count = self.visible_seats_count(i, j)
            if self.seats[i][j] == '#' and count >= 5:
                changes.append((i, j, 'L'))
            elif self.seats[i][j] == 'L' and count == 0:
                changes.append((i, j, '#'))
        return changes

    def count(self):
        return sum(r.count('#') for r in self.seats)


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
    moves = raw_data.split('\n')
    for move in moves:
        o, d = move[0], int(move[1:])
        if o == 'N':
            y += d
        elif o == 'S':
            y -= d
        elif o == 'E':
            x += d
        elif o == 'W':
            x -= d
        elif o == 'F':
            if orientation == 0:
                x += d
            if orientation == 180:
                x -= d
            if orientation == 90:
                y -= d
            if orientation == 270:
                y += d
        elif 'R' == o:
            orientation += d
            orientation += 360
            orientation %= 360
        elif 'L' == o:
            orientation -= d
            orientation += 3600
            orientation %= 360
        else:
            print(move)
    return abs(x) + abs(y)

def day12p2(raw_data):
    wx, wy = 10, 1
    x, y = 0, 0
    moves = raw_data.split('\n')
    for move in moves:
        o, d = move[0], int(move[1:])
        if o == 'N':
            wy += d
        elif o == 'S':
            wy -= d
        elif o == 'E':
            wx += d
        elif o == 'W':
            wx -= d
        elif o == 'F':
            x += wx * d
            y += wy * d
        elif 'R' == o:
            wx, wy = wx * ( d == 0 ) - wx * ( d == 180 ) - wy * ( d == 270 ) + wy * ( d == 90 ), \
                     wy * ( d == 0 ) - wy * ( d == 180 ) + wx * ( d == 270 ) - wx * ( d == 90 )
        elif 'L' == o:
            wx, wy = wx * ( d == 0 ) - wx * ( d == 180 ) + wy * ( d == 270 ) - wy * ( d == 90 ), \
                     wy * ( d == 0 ) - wy * ( d == 180 ) - wx * ( d == 270 ) + wx * ( d == 90 )
        else:
            print(move)
    return abs(x) + abs(y)


def day13p1(raw_data):
    time, buses = raw_data.split('\n')
    time = int(time)
    buses = [int(b) for b in buses.split(',') if b not in 'x']
    depart_time = math.inf
    bus_id = 0
    for b in buses:
        t = math.ceil(time/b) * b
        if depart_time > t:
            depart_time = t
            bus_id = b
    return (depart_time - time) * bus_id


def day13p2(raw_data):
    _, buses = raw_data.split('\n')
    buses = [(int(b), i) for i, b in enumerate(buses.split(',')) if b not in 'x']
    timestamp = 0
    step = 1
    for b, i in buses:
        while (timestamp + i) % b != 0:
            timestamp += step
        step = (step * b) // math.gcd(step, b)
    return timestamp





def day14p1(raw_data):
    lines = raw_data.split('\n')
    mem = {}
    for line in lines:
        if 'mask' in line:
            mask = line.split(' = ')[-1]
        if 'mem' in line:
            value = bin(int(line.split(' = ')[-1]))[2:].rjust(36, '0')
            addr = int(line.split(']')[0][4:])
            result = ''.join([m if m != 'X' else v for v, m in zip(value, mask)])
            mem[addr] = int(result, 2)
    return sum([m for m in mem.values()])


def day14p2(raw_data):
    lines = raw_data.split('\n')
    mem = {}
    for line in lines:
        if 'mask' in line:
            mask = line.split(' = ')[-1]
        if 'mem' in line:
            value = int(line.split(' = ')[-1])
            addr = bin(int(line.split(']')[0][4:]))[2:].rjust(36, '0')
            result = [m if m != '0' else v for v, m in zip(addr, mask)]
            positions = [i for i, v in enumerate(result) if v == 'X']
            count = result.count('X')
            for bits in itertools.product(['0', '1'], repeat=count):
                for p, b in zip(positions, bits):
                    result[p] = b
                mem[int(''.join(result), 2)] = value
    return sum([m for m in mem.values()])


