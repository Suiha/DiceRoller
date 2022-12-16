import sys
from antlr4 import *
from ExprLexer import ExprLexer
from ExprParser import ExprParser
from MyExprVisitor import MyExprVisitor


def main(argv):
    input = InputStream("""
    Roll1 = roll 3 d 7;
    print(Roll1);
    Roll2 = roll 1d 4 + 2;
    print(Roll2);
    Roll3 = roll 2d 12 + 1d 4;
    print(Roll3);
    Percentile = roll 1d 100;
    print(Percentile);
    Advantage = roll 2 d20 1;
    print(Advantage);
    Disadvantage = roll 1 d20 2;
    print(Disadvantage);
    Crit = roll 5 d8 3;
    print(Crit);
    Save = roll 10 d6 4;
    print(Save);
    Combo = roll 1d 8 + 1 d20 1;
    print(Combo);
    randChar1 = roll 1 randchar 0;
    randChar2 = roll 1 randchar 5;
    """.replace("\n", " "))

    lexer = ExprLexer(input)
    stream = CommonTokenStream(lexer)
    parser = ExprParser(stream)
    tree = parser.prog()

    res = MyExprVisitor().visitProg(tree)  # Evaluate the expression

if __name__ == '__main__':
    main(sys.argv)