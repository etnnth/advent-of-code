import year2019
import year2020
import database


year = 2020
day = 13
f = f"year{year}.day{day}"

with database.Database('datas.db') as db:
    raw_data = db.data(year, day)


test_data = """939
7,13,x,x,59,x,31,19"""

print(f"test p1: {eval(f'{f}p1(test_data)')}")
print(f"test p2: {eval(f'{f}p2(test_data)')}")

print(f"part1: {eval(f'{f}p1(raw_data)')}")
print(f"part2: {eval(f'{f}p2(raw_data)')}")
