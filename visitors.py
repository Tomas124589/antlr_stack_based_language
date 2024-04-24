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

    def add_instruction(self, instruction: str):
        self.output_file.write(instruction + "\n")

    def visitWrite(self, ctx: PjpGrammarParser.WriteContext):
        values = self.visit(ctx.valueList())

        self.add_instruction('print {}'.format(len(values)))

    def visitRead(self, ctx: PjpGrammarParser.ReadContext):
        pass

    def visitValueList(self, ctx: PjpGrammarParser.ValueListContext):
        return [str(self.visit(value)) for value in ctx.value()]

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
            self.vars[_id.getText()] = ctx.value().getText()

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
        return ctx.STRING().getText()[1:-1]  # Odstranění uvozovek

    def visitConcatExpression(self, ctx):
        left = ctx.STRING(0).getText()[1:-1]
        right = ctx.STRING(1).getText()[1:-1]
        return left + right

    def visitParenExpression(self, ctx):
        return self.visit(ctx.expression())


class ErrorListener(BaseErrorListener):
    def syntaxError(self, recognizer: antlr4.Parser, offendingSymbol, line, column, msg, e):
        stack = recognizer.getRuleInvocationStack()

        print('Rule stack:', stack)
        print('Line {}: {} at {}: {}'.format(line, column, offendingSymbol, msg))
