import numpy
import itertools
import collections
import copy


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
    for i in range(2, l):
        for j in range(l - i):
            r = numbers[j:j + i]
            s = sum(r)
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


def day11p1(raw_data):
    print(raw_data)
    return 1


def day11p2(raw_data):
    return 2



