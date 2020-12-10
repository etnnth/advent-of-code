import copy
import math
import itertools
import numpy
import collections
import intcode

def day1p1(raw_data):
    return sum(int(m) // 3 - 2 for m in raw_data.split("\n"))


def day1p2(raw_data):
    sum_mass = 0
    for m in (int(m) for m in raw_data.split("\n")):
        while m // 3 - 2 > 0:
            m = m // 3 - 2
            sum_mass += m
    return sum_mass


def day2p1(raw_data):
    program = [int(o) for o in raw_data.split(",")]
    program[1] = 12
    program[2] = 2
    computer = intcode.Computer(0, program)
    computer.run()
    return program[0]


def day2p2(raw_data):
    program = [int(o) for o in raw_data.split(",")]
    for noun, verb in itertools.product(range(100), range(100)):
        p = copy.copy(program)
        p[1], p[2] = noun, verb
        computer = intcode.Computer(0, p)
        computer.run()
        if p[0] == 19690720:
            return 100 * noun + verb


def lines_intersect(lines):
    points = [[0], [0]]
    for i, line in enumerate(lines):
        for command in line:
            if command[0] == "R":
                direction = 1
            elif command[0] == "L":
                direction = -1
            elif command[0] == "U":
                direction = 1j
            elif command[0] == "D":
                direction = -1j
            for j in range(int(command[1:])):
                points[i].append(points[i][-1] + direction)
    distance = math.inf
    points1, points2 = [*map(numpy.asarray, points)]
    return points1, points2, numpy.intersect1d(points1, points2)


def day3p1(raw_data):
    lines = [line.split(",") for line in raw_data.split("\n")]
    distance = math.inf
    _, _, intersect = lines_intersect(lines)
    for p in intersect:
        d = int(abs(numpy.real(p)) + abs(numpy.imag(p)))
        if d > 0 and d < distance:
            distance = d
    return distance


def day3p2(raw_data):
    lines = [line.split(",") for line in raw_data.split("\n")]
    distance = math.inf
    points1, points2, intersect = lines_intersect(lines)
    for p in intersect:
        d = numpy.argwhere(points1 == p)[0, 0] + numpy.argwhere(points2 == p)[0, 0]
        if d > 0 and d < distance:
            distance = d
    return distance


def day4p1(raw_data):
    minimum, maximum = [int(i) for i in raw_data.split('-')]
    counter = 0
    for comb in itertools.combinations_with_replacement("0123456789", 6):
        n = ''.join(comb)
        if int(n) > maximum:
            break
        if int(n) < minimum:
            continue
        if any(n.count(i) > 1 for i in n):
            counter += 1
    return counter

def day4p2(raw_data):
    minimum, maximum = [int(i) for i in raw_data.split('-')]
    counter = 0
    for comb in itertools.combinations_with_replacement("0123456789", 6):
        n = ''.join(comb)
        if int(n) > maximum:
            break
        if int(n) < minimum:
            continue
        if any(n.count(i) == 2 for i in n):
            counter += 1
    return counter

def day5p1(raw_data):
    program = [int(i) for i in raw_data.split(',')]
    computer = intcode.Computer(0, program)
    outputs = ["START"]
    while outputs[-1] != "HALT":
        outputs.append(computer.run([1]))
    return outputs[-2]

def day5p2(raw_data):
    program = [int(i) for i in raw_data.split(',')]
    computer = intcode.Computer(0, program)
    outputs = ["START"]
    while outputs[-1] != "HALT":
        outputs.append(computer.run([5]))
    return outputs[-2]


def day6p1(raw_data):
    orbits = collections.defaultdict(list)
    for orbit in raw_data.split('\n'):
        a, b = orbit.split(')')
        orbits[a].append(b)
    counter = 0
    stack = [("COM", 0)]
    while stack:
        p, n = stack.pop(0)
        counter += n
        for o in orbits[p]:
            stack.append((o, n + 1))
    return counter

def day6p2(raw_data):
    precedent = collections.defaultdict(str)
    for orbit in raw_data.split('\n'):
        a, b = orbit.split(')')
        precedent[b] = a
    san_to_com = ["SAN"]
    you_to_com = ["YOU"]
    while san_to_com[-1] != "COM":
        san_to_com.append(precedent[san_to_com[-1]])
    while you_to_com[-1] != "COM":
        you_to_com.append(precedent[you_to_com[-1]])
    y = set(you_to_com)
    s = set(san_to_com)
    return len(y - s) + len(s - y) - 2


def day7p1(raw_data):
    program = [int(i) for i in raw_data.split(',')]
    maximum = 0
    for sequence in itertools.permutations([*range(5)]):
        signal = 0
        for i in sequence:
            computer = intcode.Computer(0, copy.copy(program))
            signal = computer.run([i, signal])
        if maximum < signal:
            maximum = signal
    return maximum

def day7p2(raw_data):
    program = [int(i) for i in raw_data.split(',')]
    maximum = 0
    for sequence in itertools.permutations([*range(5, 10)]):
        signals = [0] * 5
        computers = [intcode.Computer(0, copy.copy(program)) for _ in range(5)]
        for i, computer in enumerate(computers):
            computer.run([sequence[i]])
        signal = None
        while True:
            if signal == "HALT":
                break
            for i, computer in enumerate(computers):
                signal = computer.run([signals[i]])
                if signal != "HALT":
                    signals[(i + 1) % 5] = signal
        if maximum < signals[0]:
            maximum = signals[0]
    return maximum


def day8p1(raw_data):
    layer_size = 25 * 6
    layers = [raw_data[i*layer_size:(i+1)*layer_size]
            for i in range(len(raw_data)//layer_size)]
    count_0_per_layers = [l.count('0') for l in layers]
    pos_min = count_0_per_layers.index(min(count_0_per_layers))
    return layers[pos_min].count('1') * layers[pos_min].count('2')

def day8p2(raw_data):
    layer_size = 25 * 6
    layers = [raw_data[i*layer_size:(i+1)*layer_size]
            for i in range(len(raw_data)//layer_size)]
    image = [list(layers[0][i*25:(i+1)*25]) for i in range(6)]
    for i, j in itertools.product(range(25), range(6)):
        for layer in layers:
            if layer[i + 25*j] != '2':
                image[j][i] = {'1':'#', '0':' '}[layer[i + 25*j]]
                break
    print(*map(''.join,image), sep='\n')
    return 'LBRCE'


def day9p1(raw_data):
    program = {i:int(v) for i, v in enumerate(raw_data.split(','))}
    computer = intcode.Computer(0, program)
    return computer.run([1])


def day9p2(raw_data):
    program = {i:int(v) for i, v in enumerate(raw_data.split(','))}
    computer = intcode.Computer(0, program)
    return computer.run([2])



def day10p1(raw_data):
    data = raw_data.split('\n')
    l, h = len(data[0]), len(data)
    lignes = []
    return 1

def day10p2(raw_data):
    return 1





