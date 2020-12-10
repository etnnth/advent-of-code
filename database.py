"""
Database getter and setter

"""

import argparse
import sqlite3
from typing import List


class Database:
    def __init__(self, file: str):
        self.file = file
        self.cursor = None
        self.connection = None

    def __enter__(self):
        self.connection = sqlite3.connect(self.file)
        self.cursor = self.connection.cursor()
        self.cursor.execute(
            """CREATE TABLE IF NOT EXISTS puzzles (
                id integer PRIMARY KEY,
                year integer,
                day integer,
                part1 text,
                part2 text,
                data text,
                solution1 text,
                solution2 text)"""
        )
        return self

    def __exit__(self, type, value, traceback):
        self.connection.close()

    def add_puzzle(self, year: int, day: int, data: str):
        self.cursor.execute(
            "INSERT INTO puzzles (year, day, data) VALUES (?, ?, ?)", (year, day, data)
        )
        self.connection.commit()

    def update_statement(self, year: int, day: int, parts: List[str]):
        part1 = part2 = ""
        if len(parts) == 1:
            part1 = parts[0]
        elif len(parts) == 2:
            part1, part2 = parts
        self.cursor.execute(
            "UPDATE puzzles SET part1 = ?, part2 = ? WHERE year = ? AND day = ?",
            (part1, part2, year, day),
        )
        self.connection.commit()

    def data(self, year: int, day: int) -> str:
        self.cursor.execute(
            "SELECT data FROM puzzles WHERE year = ? AND day = ?", (year, day)
        )
        return self.cursor.fetchone()[0]

    def solution1(self, year: int, day: int) -> str:
        self.cursor.execute(
            "SELECT solution1 FROM puzzles WHERE year = ? AND day = ?", (year, day)
        )
        return self.cursor.fetchone()[0]

    def solution2(self, year: int, day: int) -> str:
        self.cursor.execute(
            "SELECT solution2 FROM puzzles WHERE year = ? AND day = ?", (year, day)
        )
        return self.cursor.fetchone()[0]

    def update_solutions(self, year, day, solution1, solution2):
        self.cursor.execute(
            "UPDATE puzzles SET solution1 = ?, solution2 = ? WHERE year = ? AND day = ?",
            (solution1, solution2, year, day),
        )
        self.connection.commit()



if __name__ == "__main__":
    import fetch

    parser = argparse.ArgumentParser()
    parser.add_argument("action", choices=["add", "update", "solutions"])
    parser.add_argument("year", type=int, help="year")
    parser.add_argument("day", type=int, help="day")
    args = parser.parse_args()
    with Database("datas.db") as db:
        if args.action == "add":
            db.add_puzzle(args.year, args.day, fetch.data(args.year, args.day))
        elif args.action == "update":
            db.update_statement(
                args.year, args.day, fetch.statement(args.year, args.day)
            )
        elif args.action == "solutions":
            solution1 = input("Solution for part 1:")
            solution2 = input("Solution for part 2:")
            db.update_solutions(args.year, args.day, solution1, solution2)
