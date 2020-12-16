import year2019
import year2020
import database


year = 2020
day = 16
f = f"year{year}.day{day}"

with database.Database('datas.db') as db:
    raw_data = db.data(year, day)

test_data1 = """class: 1-3 or 5-7
row: 6-11 or 33-44
seat: 13-40 or 45-50

your ticket:
7,1,14

nearby tickets:
7,3,47
40,4,50
55,2,20
38,6,12"""


test_data2 = """class: 0-1 or 4-19
row: 0-5 or 8-19
seat: 0-13 or 16-19

your ticket:
11,12,13

nearby tickets:
3,9,18
15,1,5
5,14,9"""

print(f"test p1: {eval(f'{f}p1(test_data1)')}")
print(f"test p2: {eval(f'{f}p2(test_data2)')}")

print(f"part1: {eval(f'{f}p1(raw_data)')}")
print(f"part2: {eval(f'{f}p2(raw_data)')}")
