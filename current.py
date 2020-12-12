import year2019
import year2020
import database


year = 2020
day = 12
f = f"year{year}.day{day}"

with database.Database('datas.db') as db:
    raw_data = db.data(year, day)


test_data = """F10
N3
F7
R90
F11"""

print(f"test p1: {eval(f'{f}p1(test_data)')}")
print(f"test p2: {eval(f'{f}p2(test_data)')}")

print(f"part1: {eval(f'{f}p1(raw_data)')}")
print(f"part2: {eval(f'{f}p2(raw_data)')}")
