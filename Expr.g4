grammar Expr;

prog: stmts EOF;

stmts: stmt+;

stmt: var=ID '=' 'roll' exp=expr ';'            #assignStmt
    | 'print(' var=ID ')' ';'                   #printStmt
    ;

expr: left=expr op='d20' right=expr             #infixExpr
    | left=expr op=('d4'|'d6') right=expr       #infixExpr
    | left=expr op=('d8'|'d10') right=expr      #infixExpr
    | left=expr op=('d12'|'d100') right=expr    #infixExpr
    | left=expr op='d' right=expr               #infixExpr
    | left=expr op=('+'|'-') right=expr         #infixExpr
    | left=expr op='randchar' right=expr        #infixExpr
    | INT                                       #numberExpr
    ;

OP_D20: 'd20';
OP_D4: 'd4';
OP_D6: 'd6';
OP_D8: 'd8';
OP_D10: 'd10';
OP_D12: 'd12';
OP_D100: 'd100';
OP_D: 'd';
OP_ADD: '+';
OP_SUB: '-';
OP_RANDCHAR: 'randchar';

NEWLINE : [\r\n]+ ;
INT     : [0-9]+ ;
ID      : [A-Za-z][A-Za-z0-9]*;
WS      : [ \t\r\n] -> channel(HIDDEN);

