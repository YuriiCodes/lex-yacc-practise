## How to use?
Create a grammar in grammar.l
```bash
   lex grammar.l
```
that will create a  lex.yy.c file.
```bash
 yacc -d main.y 
```
that will create y.tab.c and y.tab.h files.
```bash 
gcc lex.yy.c y.tab.c -o yourprogram -ll -ly
``` 

that will compile the app
```bash
./yourprogram
```
 that will run the app
# lex-yacc-practise
