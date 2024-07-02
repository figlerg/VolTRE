grammar TRE;

expr : atomic_expr								#AtomicExpr
	 | '(' expr ')'								#ParenExpr
     | expr '.' expr							#ConcatExpr
     | expr '*'									#KleeneExpr
     | expr '+'									#PlusExpr
     | expr '+' expr							#UnionExpr
     | '<' expr '>' '_' interval				#TimedExpr
     ;

interval : '[' INT ',' INT ']';

//atomic_expr : LETTER ;
//LETTER : [a-zA-Z] ;

atomic_expr : IDENTIFIER;
IDENTIFIER : [a-zA-Z_][a-zA-Z0-9_]* ;


INT : [0-9]+ ;
WS : [ \t\r\n]+ -> skip ;

// Rule to handle Python-style comments
COMMENT : '#' ~[\r\n]* -> skip ;