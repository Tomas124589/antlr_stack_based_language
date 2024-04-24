import antlr4
from antlr4.error.ErrorListener import ErrorListener as BaseErrorListener
from antlr4.tree.Tree import TerminalNodeImpl

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

            if declared_type != current_type:
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

    def push(self, val):
        type = self.infer_bytecode_type(val)
        if type != '?':
            self.add_instruction('push {} {}'.format(type, val))

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

    def visitWrite(self, ctx: PjpGrammarParser.WriteContext):
        values = self.visit(ctx.valueList())

        for value in values:
            if type(value) is TerminalNodeImpl:
                self.add_instruction('load {}'.format(value.getText()))
            elif type(value) is PjpGrammarParser.LesserGreaterExpressionContext:
                left = self.visit(value.expression()[0])
                right = self.visit(value.expression()[1])

                self.push(left)
                if type(left) is int and type(right) is float:
                    self.add_instruction('itof')

                self.push(right)
                if type(right) is int and type(left) is float:
                    self.add_instruction('itof')

                if value.op.type == PjpGrammarParser.LT:
                    self.add_instruction('lt')
                else:
                    self.add_instruction('gt')
            elif type(value) is PjpGrammarParser.EqualNotEqualExpressionContext:
                left = self.visit(value.expression()[0])
                right = self.visit(value.expression()[1])

                self.push(left)
                self.push(right)

                if value.op.type == PjpGrammarParser.EQ:
                    self.add_instruction('eq')
                else:
                    self.add_instruction('eq')
                    self.add_instruction('not')
            else:
                self.push(value)

        self.add_instruction('print {}'.format(len(values)))

    def visitRead(self, ctx: PjpGrammarParser.ReadContext):
        pass

    def visitValueList(self, ctx: PjpGrammarParser.ValueListContext):
        return [self.visit(value) for value in ctx.value()]

    def visitValue(self, ctx: PjpGrammarParser.ValueContext):
        if ctx.STRING():
            return str(ctx.STRING().getText())
        elif ctx.INT():
            return int(ctx.INT().getText())
        elif ctx.FLOAT():
            return float(ctx.FLOAT().getText())
        elif ctx.BOOL():
            return bool(ctx.BOOL().getText())
        elif ctx.ID():
            self.add_instruction('load {}'.format(ctx.ID().getText()))
            self.add_instruction('pop')
            return ctx.ID()
        elif ctx.expression():
            return self.visit(ctx.expression())

    def visitVariableDeclaration(self, ctx: PjpGrammarParser.VariableDeclarationContext):
        for _id in ctx.ID():
            type = self.type_2_bytecode_type(ctx.TYPE().getText())
            value = self.get_type_default_value(type)

            self.vars[_id.getText()] = {
                'type': ctx.TYPE().getText(),
                'value': value
            }

            self.push(value)
            self.add_instruction('save {}'.format(_id))

    def visitVariableAssignment(self, ctx: PjpGrammarParser.VariableAssignmentContext):
        for _id in ctx.ID():
            val = self.visit(ctx.value())

            self.push(val)
            self.add_instruction('save {}'.format(_id))

            self.vars[_id.getText()]['value'] = val

    def visitAddSubExpression(self, ctx):
        left = self.visit(ctx.expression(0))
        right = self.visit(ctx.expression(1))

        if ctx.op.type == PjpGrammarParser.ADD:
            return left + right
        elif ctx.op.type == PjpGrammarParser.SUB:
            return left - right

    def visitMulDivModExpression(self, ctx):
        left = self.visit(ctx.expression(0))
        right = self.visit(ctx.expression(1))

        if ctx.op.type == PjpGrammarParser.MUL:
            return left * right
        elif ctx.op.type == PjpGrammarParser.DIV:
            return left / right
        elif ctx.op.type == PjpGrammarParser.MOD:
            return left % right

    def visitNumberExpression(self, ctx):
        if ctx.INT():
            return int(ctx.INT().getText())
        elif ctx.FLOAT():
            return float(ctx.FLOAT().getText())

    def visitStringExpression(self, ctx):
        return ctx.STRING().getText()

    def visitConcatExpression(self, ctx):
        left = ctx.STRING(0).getText()[1:-1]
        right = ctx.STRING(1).getText()[1:-1]
        return left + right

    def visitParenExpression(self, ctx):
        return self.visit(ctx.expression())

    def visitLesserGreaterExpression(self, ctx: PjpGrammarParser.LesserGreaterExpressionContext):
        return ctx

    def visitEqualNotEqualExpression(self, ctx: PjpGrammarParser.EqualNotEqualExpressionContext):
        return ctx


class ErrorListener(BaseErrorListener):
    def syntaxError(self, recognizer: antlr4.Parser, offendingSymbol, line, column, msg, e):
        stack = recognizer.getRuleInvocationStack()

        print('Rule stack:', stack)
        print('Line {}: {} at {}: {}'.format(line, column, offendingSymbol, msg))
