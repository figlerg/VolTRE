grammar TRE;

expr : atomic_expr								#AtomicExpr
	 | '(' expr ')'								#ParenExpr
     | expr '.' expr							#ConcatExpr
     | expr '*'									#KleeneExpr
     | expr '+' expr							#UnionExpr
     | '<' expr '>' '_' interval				#TimedExpr
     ;

interval : '[' INT ',' INT ']';

atomic_expr : LETTER ;

LETTER : [a-zA-Z] ;
INT : [0-9]+ ;
WS : [ \t\r\n]+ -> skip ;
