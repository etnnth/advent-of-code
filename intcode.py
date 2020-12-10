

class Computer:
    def __init__(self, index, program):
        self.index = index
        self.program = program
        self.modes = [0, 0, 0]
        self.rel = 0

    def run(self, inputs = None):
        while True:
            instruction = self.program[self.index]
            instruction, optcode = divmod(instruction, 100)
            instruction, self.modes[0] = divmod(instruction, 10)
            self.modes[2], self.modes[1] = divmod(instruction, 10)
            if optcode == 99:
                return "HALT"
            if optcode == 1:
                self.set(3, self.get(1) + self.get(2))
                self.index += 4
            elif optcode == 2:
                self.set(3, self.get(1) * self.get(2))
                self.index += 4
            elif optcode == 3:
                if len(inputs) == 0:
                    return "INPUT"
                self.set(1, inputs.pop(0))
                self.index += 2
            elif optcode == 4:
                output = self.get(1)
                self.index += 2
                return output
            elif optcode == 5:
                if self.get(1) != 0:
                    self.index = self.get(2)
                else:
                    self.index += 3
            elif optcode == 6:
                if self.get(1) == 0:
                    self.index = self.get(2)
                else:
                    self.index += 3
            elif optcode == 7:
                self.set(3, int(self.get(1) < self.get(2)))
                self.index += 4
            elif optcode == 8:
                self.set(3, int(self.get(1) == self.get(2)))
                self.index += 4
            elif optcode == 9:
                self.rel += self.get(1)
                self.index += 2


    def get(self, index):
        mode = self.modes[index - 1]
        if mode == 0:
            return self.program[self.program[self.index + index]]
        if mode == 1:
            return self.program[self.index + index]
        if mode == 2:
            return self.program[self.program[self.index + index] + self.rel]

    def set(self, index, value):
        mode = self.modes[index - 1]
        if mode == 0:
            self.program[self.program[self.index + index]] = value
        elif mode == 1:
            self.program[self.index + index] = value
        elif mode == 2:
            self.program[self.program[self.index + index] + self.rel] = value


