from grammar.PjpGrammarParser import PjpGrammarParser
from grammar.PjpGrammarVisitor import PjpGrammarVisitor


class MyVisitor(PjpGrammarVisitor):
    def __init__(self):
        self.vars = {}

    def visitWrite(self, ctx: PjpGrammarParser.WriteContext):
        self.visit(ctx.valueList())

    def visitValueList(self, ctx: PjpGrammarParser.ValueListContext):
        res = [str(self.visit(value)) for value in ctx.value()]

        print("".join(res))
        return None

    def visitValue(self, ctx: PjpGrammarParser.ValueContext):
        if ctx.STRING():
            return ctx.STRING().getText()[1:-1]
        elif ctx.INT():
            return ctx.INT().getText()
        elif ctx.FLOAT():
            return ctx.FLOAT().getText()
        elif ctx.BOOL():
            return ctx.BOOL().getText()
        elif ctx.ID():
            return self.vars[ctx.ID().getText()]
        elif ctx.expression():
            return self.visit(ctx.expression())

    def visitVariableDeclaration(self, ctx: PjpGrammarParser.VariableDeclarationContext):
        for _id in ctx.ID():
            self.vars[_id.getText()] = None

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
