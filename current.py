import year2019
import year2020
import database


year = 2020
day = 22
f = f"year{year}.day{day}"

with database.Database("datas.db") as db:
    raw_data = db.data(year, day)

test_data1 = """Player 1:
9
2
6
3
1

Player 2:
5
8
4
7
10"""


test_data2 = test_data1

print(f"test p1: {eval(f'{f}p1(test_data1)')}")
print(f"test p2: {eval(f'{f}p2(test_data2)')}")

print(f"part1: {eval(f'{f}p1(raw_data)')}")
print(f"part2: {eval(f'{f}p2(raw_data)')}")
