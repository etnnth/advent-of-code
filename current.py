import year2019
import year2020
import database


year = 2020
day = 14
f = f"year{year}.day{day}"

with database.Database('datas.db') as db:
    raw_data = db.data(year, day)


test_data = """mask = XXXXXXXXXXXXXXXXXXXXXXXXXXXXX1XXXX0X
mem[8] = 11
mem[7] = 101
mem[8] = 0"""


test_data2 = """mask = 000000000000000000000000000000X1001X
mem[42] = 100
mask = 00000000000000000000000000000000X0XX
mem[26] = 1"""

print(f"test p1: {eval(f'{f}p1(test_data)')}")
print(f"test p2: {eval(f'{f}p2(test_data2)')}")

print(f"part1: {eval(f'{f}p1(raw_data)')}")
print(f"part2: {eval(f'{f}p2(raw_data)')}")
