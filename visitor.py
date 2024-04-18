from grammar.PjpGrammarParser import PjpGrammarParser
from grammar.PjpGrammarVisitor import PjpGrammarVisitor


class MyVisitor(PjpGrammarVisitor):
    def visitWrite(self, ctx: PjpGrammarParser.WriteContext):
        self.visit(ctx.argumentList())

    def visitArgumentList(self, ctx: PjpGrammarParser.ArgumentListContext):
        res = [self.visit(argument) for argument in ctx.argument()]
        print("".join(res))
        return None

    def visitArgument(self, ctx: PjpGrammarParser.ArgumentContext):
        if ctx.STRING():
            return ctx.STRING().getText()[1:-1]
        elif ctx.INT():
            return ctx.INT().getText()
        elif ctx.FLOAT():
            return ctx.FLOAT().getText()
