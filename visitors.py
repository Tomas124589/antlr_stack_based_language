import antlr4
from antlr4.error.ErrorListener import ErrorListener as BaseErrorListener

from grammar.PjpGrammarParser import PjpGrammarParser
from grammar.PjpGrammarVisitor import PjpGrammarVisitor


class TypeChecker(PjpGrammarVisitor):
    def __init__(self):
        self.vars = {}
        self.type_errors = []

    def visitValue(self, ctx: PjpGrammarParser.ValueContext):
        if ctx.STRING():
            return str(ctx.STRING().getText()[1:-1])
        elif ctx.INT():
            return int(ctx.INT().getText())
        elif ctx.FLOAT():
            return float(ctx.FLOAT().getText())
        elif ctx.BOOL():
            return bool(ctx.BOOL().getText())
        elif ctx.ID():
            return self.vars[ctx.ID().getText()]
        elif ctx.expression():
            return self.visit(ctx.expression())

    def visitVariableDeclaration(self, ctx: PjpGrammarParser.VariableDeclarationContext):
        for _id in ctx.ID():
            self.vars[_id.getText()] = {
                'type': ctx.TYPE().getText(),
                'value': None
            }

    def visitVariableAssignment(self, ctx: PjpGrammarParser.VariableAssignmentContext):
        for _id in ctx.ID():
            declared_type = self.vars[_id.getText()]['type']
            current_type = type(self.visit(ctx.value())).__name__
            if current_type == 'str':
                current_type = 'string'

            is_declared_type_num = declared_type in ['int', 'float']
            is_current_type_num = current_type in ['int', 'float']

            if declared_type != current_type and not (is_declared_type_num and is_current_type_num):
                token = _id.getSymbol()
                self.type_errors.append("Trying to assign {} to {} at {}:{}"
                .format(
                    current_type,
                    declared_type,
                    token.line,
                    token.column
                ))

            self.vars[_id.getText()] = ctx.value().getText()


class MyVisitor(PjpGrammarVisitor):
    def __init__(self):
        self.vars = {}
        self.output_file = open("bytecode.txt", "w")
        self.last_declared_type = None
        self.last_label_id = -1

    def push(self, val):
        type = self.infer_bytecode_type(val)
        if type != '?':
            self.add_instruction('push {} {}'.format(type, val))
        return val

    def add_instruction(self, instruction: str):
        self.output_file.write(instruction + "\n")

    @staticmethod
    def infer_bytecode_type(val):
        return MyVisitor.type_2_bytecode_type(type(val).__name__)

    @staticmethod
    def type_2_bytecode_type(_type: str):
        if _type == 'str' or _type == 'string':
            return 'S'
        elif _type == 'int':
            return 'I'
        elif _type == 'float':
            return 'F'
        elif _type == 'bool':
            return 'B'
        else:
            print('unknown type {}'.format(_type))
            return '?'

    @staticmethod
    def get_type_default_value(_type: str):
        if _type == 'S':
            return '""'
        elif _type == 'I':
            return 0
        elif _type == 'F':
            return 0.0
        elif _type == 'B':
            return False
        else:
            print('unknown type {}'.format(_type))
            return 'UNKNOWN'

    def get_next_label_id(self):
        self.last_label_id = self.last_label_id + 1
        return self.last_label_id

    def visitProgram(self, ctx: PjpGrammarParser.ProgramContext):
        [self.visit(value) for value in ctx.statement()]
        self.output_file.close()

    def visitWrite(self, ctx: PjpGrammarParser.WriteContext):
        [self.visit(value) for value in ctx.expression()]

        self.add_instruction('print {}'.format(len(ctx.expression())))

    def visitRead(self, ctx: PjpGrammarParser.ReadContext):
        for _id in ctx.ID():
            _type = self.vars[_id.getText()]['type']

            self.add_instruction('read {}'.format(self.type_2_bytecode_type(_type)))
            self.add_instruction('save {}'.format(_id))

    def visitValue(self, ctx: PjpGrammarParser.ValueContext):
        if ctx.STRING():
            return str(ctx.STRING().getText())
        elif ctx.INT():
            return int(ctx.INT().getText())
        elif ctx.FLOAT():
            return float(ctx.FLOAT().getText())
        elif ctx.BOOL():
            return bool(ctx.BOOL().getText())
        elif ctx.expression():
            return self.visit(ctx.expression())

    def visitVariableDeclaration(self, ctx: PjpGrammarParser.VariableDeclarationContext):
        for _id in ctx.ID():
            self.last_declared_type = _type = self.type_2_bytecode_type(ctx.TYPE().getText())
            value = self.get_type_default_value(_type)

            self.vars[_id.getText()] = {
                'type': ctx.TYPE().getText(),
                'value': value
            }

            self.push(value)
            self.add_instruction('save {}'.format(_id))

    def visitVariableAssignment(self, ctx: PjpGrammarParser.VariableAssignmentContext):
        pushed = False
        for _id in reversed(ctx.ID()):
            val = self.visit(ctx.value())
            _type = self.vars[_id.getText()]['type']

            uminus = _type in ['int', 'float'] and val < 0
            if uminus:
                val = abs(val)

            if not pushed:
                self.push(val)
                pushed = True

            if type(val) is int and _type == 'float':
                self.add_instruction('itof')

            if uminus:
                self.add_instruction('uminus')
            self.add_instruction('save {}'.format(_id))
            self.add_instruction('load {}'.format(_id))

            self.vars[_id.getText()]['value'] = val

        self.add_instruction('pop')

    def visitAddSubExpression(self, ctx):
        left = self.visit(ctx.expression(0))
        right = self.visit(ctx.expression(1))

        if ctx.op.type == PjpGrammarParser.ADD:
            self.add_instruction('add')
            return left + right
        elif ctx.op.type == PjpGrammarParser.SUB:
            self.add_instruction('sub')
            return left - right

    def visitMulDivModExpression(self, ctx):
        left = self.visit(ctx.expression(0))
        right = self.visit(ctx.expression(1))

        if type(left) is float and type(right) is int:
            self.add_instruction('itof')

        if ctx.op.type == PjpGrammarParser.MUL:
            self.add_instruction('mul')
            return left * right
        elif ctx.op.type == PjpGrammarParser.DIV:
            self.add_instruction('div')
            return left / right
        elif ctx.op.type == PjpGrammarParser.MOD:
            self.add_instruction('mod')
            return left % right

    def visitNumberExpression(self, ctx):
        if ctx.INT():
            val = int(ctx.INT().getText())
        elif ctx.FLOAT():
            val = float(ctx.FLOAT().getText())

        return self.push(val)

    def visitStringExpression(self, ctx):
        return self.push(ctx.STRING().getText())

    def visitBoolExpression(self, ctx: PjpGrammarParser.BoolExpressionContext):
        return self.push(ctx.BOOL().getText() == 'true')

    def visitConcatExpression(self, ctx):
        left = ctx.STRING(0).getText()
        right = ctx.STRING(1).getText()

        self.push(left)
        self.push(right)

        self.add_instruction('concat')
        return left + right

    def visitParenExpression(self, ctx):
        return self.visit(ctx.expression())

    def visitIdExpression(self, ctx: PjpGrammarParser.IdExpressionContext):
        self.add_instruction('load {}'.format(ctx.ID().getText()))

    def visitLesserGreaterExpression(self, ctx: PjpGrammarParser.LesserGreaterExpressionContext):
        is_left_int = float(ctx.expression()[0].getText()).is_integer()
        is_right_int = float(ctx.expression()[1].getText()).is_integer()

        left = self.visit(ctx.expression()[0])
        if is_left_int and not is_right_int:
            self.add_instruction('itof')

        right = self.visit(ctx.expression()[1])

        if is_right_int is int and not is_left_int:
            self.add_instruction('itof')

        if ctx.op.type == PjpGrammarParser.LT:
            self.add_instruction('lt')
            result = left < right
        else:
            self.add_instruction('gt')
            result = left > right

        return result

    def visitEqualNotEqualExpression(self, ctx: PjpGrammarParser.EqualNotEqualExpressionContext):
        self.visit(ctx.expression()[0])
        self.visit(ctx.expression()[1])

        if ctx.op.type == PjpGrammarParser.EQ:
            self.add_instruction('eq')
        else:
            self.add_instruction('eq')
            self.add_instruction('not')

    def visitLogicalExpression(self, ctx: PjpGrammarParser.LogicalExpressionContext):
        self.visit(ctx.expression()[0])
        self.visit(ctx.expression()[1])

        if ctx.op.type == PjpGrammarParser.AND:
            self.add_instruction('and')
        else:
            self.add_instruction('or')

    def visitNotExpression(self, ctx: PjpGrammarParser.NotExpressionContext):
        self.visit(ctx.expression())
        self.add_instruction('not')
        return ctx

    def visitIfStatement(self, ctx: PjpGrammarParser.IfStatementContext):
        self.visit(ctx.expression())

        fjmp_label = self.get_next_label_id()
        self.add_instruction('fjmp {}'.format(fjmp_label))
        self.visit(ctx.statement()[0])

        jmp_label = self.get_next_label_id()
        self.add_instruction('jmp {}'.format(jmp_label))
        self.add_instruction('label {}'.format(fjmp_label))
        self.visit(ctx.statement()[1])

        self.add_instruction('label {}'.format(jmp_label))

    def visitIfStatementBody(self, ctx: PjpGrammarParser.IfStatementBodyContext):
        self.visit(ctx.expression())

        fjmp_label = self.get_next_label_id()
        self.add_instruction('fjmp {}'.format(fjmp_label))
        [self.visit(value) for value in ctx.statement()]

        jmp_label = self.get_next_label_id()
        self.add_instruction('jmp {}'.format(jmp_label))
        self.add_instruction('label {}'.format(fjmp_label))
        self.add_instruction('label {}'.format(jmp_label))


class ErrorListener(BaseErrorListener):
    def syntaxError(self, recognizer: antlr4.Parser, offendingSymbol, line, column, msg, e):
        stack = recognizer.getRuleInvocationStack()

        print('Rule stack:', stack)
        print('Line {}: {} at {}: {}'.format(line, column, offendingSymbol, msg))
