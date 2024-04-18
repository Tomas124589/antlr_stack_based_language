from grammar.PjpGrammarParser import PjpGrammarParser
from grammar.PjpGrammarVisitor import PjpGrammarVisitor


class MyVisitor(PjpGrammarVisitor):
    def __init__(self):
        self.vars = {}

    def visitWrite(self, ctx: PjpGrammarParser.WriteContext):
        self.visit(ctx.valueList())

    def visitValueList(self, ctx: PjpGrammarParser.ValueListContext):
        res = [self.visit(value) for value in ctx.value()]
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

    def visitVariableDeclaration(self, ctx: PjpGrammarParser.VariableDeclarationContext):
        self.vars[ctx.ID().getText()] = None

    def visitVariableAssignment(self, ctx: PjpGrammarParser.VariableAssignmentContext):
        self.vars[ctx.ID().getText()] = ctx.value().getText()
