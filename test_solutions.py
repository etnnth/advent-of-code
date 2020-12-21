import database
import pytest

import year2019
import year2020

years = {2019: 9, 2020: 21}

file = "datas.db"
tests = []


for year, max_day in years.items():
    tests += [(year, day, 1) for day in range(1, max_day + 1)]
    tests += [(year, day, 2) for day in range(1, max_day + 1)]


@pytest.mark.parametrize("year, day, part", tests)
def test_solution(year, day, part, benchmark):
    with database.Database(file) as db:
        raw_data = db.data(year, day)
        if part == 1:
            solution = db.solution1(year, day)
        elif part == 2:
            solution = db.solution2(year, day)
    exec(f"global func;func = year{year}.day{day}p{part}")
    result = str(benchmark(func, raw_data=raw_data))
    assert result == solution
