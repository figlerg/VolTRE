grammar TRE;

file : expr EOF ;

expr : EPS																				#EpsExpr
	 |atomic_expr																		#AtomicExpr
	 | '(' expr ')'																		#ParenExpr
     | expr '*'																			#KleeneExpr
     | expr '.' expr																	#ConcatExpr
     | expr '+'																			#PlusExpr
     | expr '+' expr																	#UnionExpr
     | expr '&' expr																	#IntersectionExpr
     | '<' expr '>' '_' interval														#TimedExpr
     | '{' (rename_token ',')* rename_token '}' expr									#RenameExpr
     ;

interval : '[' INT ',' (INT | INF) ']';

//atomic_expr : LETTER ;
//LETTER : [a-zA-Z] ;

EPS : 'EPS';
INF : 'INF' | 'oo' | 'inf';

atomic_expr : IDENTIFIER;
rename_token : atomic_expr ':' atomic_expr;

IDENTIFIER : [a-zA-Z_][a-zA-Z0-9_]* ;


INT : [0-9]+ ;
WS : [ \t\r\n]+ -> skip ;

// Rule to handle Python-style comments
COMMENT : '#' ~[\r\n]* -> skip ;