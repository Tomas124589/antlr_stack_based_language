import sys


class VirtualMachine:
    def __init__(self, byte_code: str):
        self.stack = []
        self.vars = {}
        self.jumps = {}
        self.current_line = 0
        self.instructions = byte_code.split('\n')

        self.exec_methods = []
        for name in dir(self):
            if name.startswith('exec_'):
                method = getattr(self, name)
                if callable(method):
                    self.exec_methods.append(method)

    @staticmethod
    def autoconvert_bytecode_type(value, _type):
        if _type == 'F':
            return float(value)
        elif _type == 'I':
            return int(value)
        elif _type == 'S':
            return str(value)[1:-1]
        elif _type == 'B':
            return value == 'true'
        else:
            print('ERROR: Undefined type {}'.format(_type))
            exit(1)

    @staticmethod
    def bytecode_type_2_type(_type):
        if _type == 'F':
            return float
        elif _type == 'I':
            return int
        elif _type == 'S':
            return str
        elif _type == 'B':
            return bool
        else:
            print('ERROR: Undefined type {}'.format(_type))
            exit(1)

    def exec_add(self, args: str | None):
        left = self.stack.pop()
        right = self.stack.pop()

        self.stack.append(left + right)

    def exec_sub(self, args: str | None):
        left = self.stack.pop()
        right = self.stack.pop()

        self.stack.append(left - right)

    def exec_mul(self, args: str | None):
        left = self.stack.pop()
        right = self.stack.pop()

        self.stack.append(left * right)

    def exec_div(self, args: str | None):
        right = self.stack.pop()
        left = self.stack.pop()

        if type(right) is int and type(right) == type(left):
            self.stack.append(left // right)
        else:
            self.stack.append(left / right)

    def exec_mod(self, args: str | None):
        right = self.stack.pop()
        left = self.stack.pop()

        self.stack.append(left % right)

    def exec_uminus(self, args: str | None):
        self.stack.append(-self.stack.pop())

    def exec_concat(self, args: str | None):
        right = self.stack.pop()
        left = self.stack.pop()

        self.stack.append(left + right)

    def exec_and(self, args: str | None):
        right = self.stack.pop()
        left = self.stack.pop()

        self.stack.append(left and right)

    def exec_or(self, args: str | None):
        right = self.stack.pop()
        left = self.stack.pop()

        self.stack.append(left or right)

    def exec_gt(self, args: str | None):
        right = self.stack.pop()
        left = self.stack.pop()

        self.stack.append(left > right)

    def exec_lt(self, args: str | None):
        right = self.stack.pop()
        left = self.stack.pop()

        self.stack.append(left < right)

    def exec_eq(self, args: str | None):
        right = self.stack.pop()
        left = self.stack.pop()

        self.stack.append(left == right)

    def exec_not(self, args: str | None):
        self.stack.append(not self.stack.pop())

    def exec_itof(self, args: str | None):
        self.stack.append(float(self.stack.pop()))

    def exec_push(self, args: str | None):
        [_type, value] = args.split(' ', 1)

        self.stack.append(self.autoconvert_bytecode_type(value, _type))

    def exec_pop(self, args: str | None):
        self.stack.pop()

    def exec_load(self, args: str | None):
        self.stack.append(self.vars[str(args)])

    def exec_save(self, args: str | None):
        self.vars[str(args)] = self.stack.pop()

    def exec_jmp(self, args: str | None):
        self.current_line = self.jumps[int(args)]

    def exec_fjmp(self, args: str | None):
        if not self.stack.pop():
            self.current_line = self.jumps[int(args)]

    def exec_print(self, args: str | None):
        values = []
        for i in range(int(args)):
            values.append(self.stack.pop())

        print(" ".join(map(str, reversed(values))))

    def exec_read(self, args: str | None):
        target_type = self.bytecode_type_2_type(str(args))

        value = input()

        if target_type is bool:
            value = value == 'true'

        self.stack.append(target_type(value))

    def execute(self):
        self.calculate_labels()

        while self.current_line < len(self.instructions):
            instruction_str = self.instructions[self.current_line]
            self.current_line = self.current_line + 1
            instruction_split = instruction_str.split(' ', 1)
            instruction_args = None if len(instruction_split) == 1 else instruction_split[1]

            for method in self.exec_methods:
                if method.__name__ == 'exec_' + instruction_split[0]:
                    method(instruction_args)
                    break

    def calculate_labels(self):
        for i, instruction_str in enumerate(self.instructions):
            instruction_split = instruction_str.split(' ', 1)

            if instruction_split[0] == 'label':
                self.jumps[int(instruction_split[1])] = i


if __name__ == '__main__':
    if len(sys.argv) == 2:
        with open(sys.argv[1], 'r') as file:
            vm = VirtualMachine(file.read())
            vm.execute()
    else:
        print('No bytecode path specified')
