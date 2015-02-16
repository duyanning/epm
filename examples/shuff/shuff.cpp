#include <stdio.h>
//#include "parser.h"

extern int yyparse();

void yyerror(const char* s)
{
	printf("%s\n", s);
}

extern "C" int yywrap()
{
	return 1;
}

int main()
{
	return yyparse();
}

