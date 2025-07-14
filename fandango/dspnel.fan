#!/usr/bin/env fandango fuzz -f

<newline> ::= ('\r'? '\n' | '\r' | '\f') := '\n'
<_> ::= (<any_whitespace> | <newline>)*
<identifier> ::= r'[_$]*[a-zA-Z0-9_$]+'
#<_> ::= " "
#<identifier> ::= "v" <digit>+
<number> ::= <digit>+ ("."  <digit>+)? ( "e" "-"? <digit>+)? ("i" | "j")?
<doccomment> ::= "///" r'[^\r\n\f]'* <newline>
<comment> ::= ("/*"  <char>*  "*/")  | ("//" r'[^\r\n\f]'* <newline>)

<expression> ::= <expr3>

<expr3> ::= \
      <expr4> <_> "==>" <_> <expr4> \
    | <expr4>

<expr4> ::= \
      <expr5> <_> r'or(?![_$a-zA-Z0-9])' <_> <expr5> \
    | <expr5> <_> r'xor(?![_$a-zA-Z0-9])' <_> <expr5> \
    | <expr5>

<expr5> ::= \
      <expr6> <_> r'and(?![_$a-zA-Z0-9])' <_> <expr6> \
    | <expr6>

<expr6> ::= \
      r'not(?![_$a-zA-Z0-9])' <_> <expr7> \
    | <expr7>

<expr7> ::= \
      <expr8> <_> "<" <_> <expr8> \
    | <expr8> <_> "<=" <_> <expr8> \
    | <expr8> <_> ">" <_> <expr8> \
    | <expr8> <_> ">=" <_> <expr8> \
    | <expr8> <_> "==" <_> <expr8> \
    | <expr8> <_> "!=" <_> <expr8> \
    | <expr8>

<expr8> ::= \
      <expr9> <_> "|" <_> <expr9> \
    | <expr9>

<expr9> ::= \
      <expr10> <_> "&" <_> <expr10> \
    | <expr10>

<expr10> ::= \
      <expr11> <_> "<<" <_> <expr11> \
    | <expr11> <_> ">>" <_> <expr11> \
    | <expr11>

<expr11> ::= \
      <expr12> <_> "+" <_> <expr12> \
    | <expr12> <_> "-" <_> <expr12> \
    | <expr12>

<expr12> ::= \
      <expr13> <_> "*" <_> <expr13> \
    | <expr13> <_> "/" <_> <expr13> \
    | <expr13> <_> "%" <_> <expr13> \
    | <expr13>

<expr13> ::= \
      "~" <_> <expr14> \
    | <expr14>

<expr14> ::= \
      <expr15> <_> "^" <_> <expr15> \
    | <expr15>

<expr15> ::= \
      <expr16> <_> "'" \
    | <expr16>

<expr16> ::= \
      <expr17> "." <identifier> \
    | <expr17>

<expr17> ::= \
      <number> \
    | <identifier> \
    | "(" <_> <expression> <_> ")" \
    | "[" <_> <rows> <_> "]"

<constructor_type> ::= \
      <identifier> ("." <identifier>)*

<type_expression> ::= <constructor_type> \
    | "[" <_> <type_expression> <_> ";" <_> <expression>? <_> "]" \
    | <constructor_type> "<" <_> <type_expression> <_> ">" \

<expresion_list> ::= <expression> <_> ("," <_> <expression>)*

<row_remainder> ::= r'for(?![_$a-zA-Z0-9])' <identifier> <_> r'in(?![_$a-zA-Z0-9])' <_> <expression> <_> ".." <_> <expression>
<row> ::= <expresion_list> <row_remainder>?
<rows> ::= <row> <_> ("," <_> <row>)*

<assumptions> ::= r'requires(?![_$a-zA-Z0-9])' <_> <expresion_list>
<guarantees> ::= r'ensures(?![_$a-zA-Z0-9])' <_> <expresion_list>

<param_qualifier> ::= r'in(?![_$a-zA-Z0-9])' | r'out(?![_$a-zA-Z0-9])' | r'state(?![_$a-zA-Z0-9])'
<parameter> ::= <param_qualifier>? <_> <identifier> (":" <_> <type_expression>)? ( <_> "=" <expression> )?
<parameters_elt> ::= <doccomment>? <parameter> <_> "," <_> <comment>?
<parameters_list> ::= (<parameters_elt> <_>)*

<protofunction> ::= <doccomment>? <_> \
     (r'kernel(?=\s)' | r'fn(?![_$a-zA-Z0-9])' | r'quickcheck(?![_$a-zA-Z0-9])' ) <_> \
     <identifier> "(" <_> \
     <parameters_list> \
     ")" <_> \
     <assumptions>? <_> \
     <guarantees>? <_> \
     <block>

<stmt> ::=  \
      <comment> \
    | <identifier> <_> ("=" | "*=" | "+=" | "-=") <_> <expression> <_> ";" \
    | r'return(?![_$a-zA-Z0-9])' <_> <expression>? <_> ";" \
    | <protofunction> \
    | r'let(?![_$a-zA-Z0-9])' <_> <identifier> <_> (":" <_> <type_expression> )? ( <_> "=" <expression> )? <_> ";" \
    | <block>

<block> ::= "{" <_> (<stmt> <_>)* <_> "}"

<start> ::= <_> <stmt>* <_>