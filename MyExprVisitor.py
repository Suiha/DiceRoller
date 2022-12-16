import math
import random

from ExprParser import ExprParser
from ExprVisitor import ExprVisitor


class MyExprVisitor(ExprVisitor):
    def __init__(self):
        super(MyExprVisitor, self).__init__()
        self.stack = []  # Stack to evaluate the expression
        self.variables = {}  # Dictionary to keep track of the variables

    # Visit a parse tree produced by ExprParser#prog.
    # def visitProg(self, ctx: ExprParser.ProgContext):
    #    return self.visit(ctx.expr())  # Just visit the self expression


    def visitAssignStmt(self, ctx: ExprParser.AssignStmtContext):
        self.visit(ctx.exp)
        self.variables[str(ctx.var.text)] = self.stack.pop()


    def visitPrintStmt(self, ctx: ExprParser.PrintStmtContext):
        var = str(ctx.var.text)
        if var not in self.variables:
            print(f'{var} is undefined\n')
        else:
            print(f"{var} result: {self.variables[var]}\n")


    # Visit a parse tree produced by ExprParser#infixExpr.
    def visitInfixExpr(self, ctx: ExprParser.InfixExprContext):
        self.visit(ctx.left)  # Evaluate the left expression and push to stack
        self.visit(ctx.right)  # Evaluate the right expression and push to stack

        b = self.stack.pop()
        a = self.stack.pop()
        c = None

        if ctx.OP_D20():
            c = self.roll(a, 20, b)
        elif ctx.OP_D4():
            c = self.roll(a, 4, b)
        elif ctx.OP_D6():
            c = self.roll(a, 6, b)
        elif ctx.OP_D8():
            c = self.roll(a, 8, b)
        elif ctx.OP_D10():
            c = self.roll(a, 10, b)
        elif ctx.OP_D12():
            c = self.roll(a, 12, b)
        elif ctx.OP_D100():
            c = self.roll(a, 100, b)
        elif ctx.OP_D():
            c = self.roll(a, b, 0)
        elif ctx.OP_ADD():
            c = a + b
            print('{} + {} = {}'.format(a, b, c))
        elif ctx.OP_SUB():
            c = a - b
            print('{} - {} = {}'.format(a, b, c))
        elif ctx.OP_RANDCHAR():
            c = self.randChar(a, b)

        self.stack.append(c)
        return c

    # Helper function for rolling
    # ad indicates the modifier, 0 meaning normal, 1 meaning advantage, 2 meaning disadvantage,
    # 3 meaning crit, 4 meaning save
    def roll(self, n, d, ad):
        tmp = ""
        if ad == 1:
            tmp = " adv"
        elif ad == 2:
            tmp = " dis"
        elif ad == 3:
            tmp = " crit"
        elif ad == 4:
            tmp = " save"
        string = "{}d{}{}: [".format(n, d, tmp)
        if ad > 0 and ad < 3:
            string += "("
        if d == 100:
            lo = 0
            hi = 99
        else:
            lo = 1
            hi = d
        res = 0
        for i in range(n):
            rand = random.randint(lo, hi)
            res += rand
            if i == 0:
                string += "{}".format(rand)
            else:
                string += " + {}".format(rand)
        if ad == 1 or ad == 2:
            string += ") ("
            res2 = 0
            for i in range(n):
                rand = random.randint(lo, hi)
                res2 += rand
                if i == 0:
                    string += "{}".format(rand)
                else:
                    string += " + {}".format(rand)
            string += ")"
            if ad == 1:
                res = max(res, res2)
            else:
                res = min(res, res2)
        elif ad == 3:
            string += " ({})".format(res)
            res *= 2
        elif ad == 4:
            string += " ({})".format(res)
            res = int(math.floor(res/2))
        string += "] {}".format(res)
        print(string)
        return res

    def randChar(self, n, b):
        if n == 0:
            return
        string = "Random Character Stats:"
        total = 0
        for i in range(6):
            string += "\n\t4d6: ("
            tmp = []
            for j in range(4):
                rand = random.randint(1, 6)
                string += "{} ".format(str(rand))
                tmp.append(rand)
            tmp.remove(min(tmp))
            res = sum(tmp)
            total += res
            if b == 0:
                string += "\b) = {}".format(res)
            else:
                string += "\b) + {} = {}".format(b, res)
        string += "\nTotal: {}\n".format(total)
        print(string)
        self.randChar(n-1, b)

    # Visit a parse tree produced by ExprParser#numberExpr.
    def visitNumberExpr(self, ctx: ExprParser.NumberExprContext):
        c = int(str(ctx.INT()))  # Found a number, just insert to stack
        self.stack.append(c)
        return c

    '''
    def visitStringExpr(self, ctx:ExprParser.StringExprContext):
        c = str(ctx.__str__())
        self.stack.append(c)
        return c
    '''
    '''
    # Visit a parse tree produced by ExprParser#parensExpr.
    def visitParensExpr(self, ctx: ExprParser.ParensExprContext):
        return self.visit(ctx.expr())  # Since enclosed by parents, just visit expr
    '''