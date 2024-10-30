from rply import LexerGenerator

lg = LexerGenerator()

lg.add('NUMBER', r'\d+(\.\d+)?(e(-)?\d+)?(i|j)?')
lg.add('DOCCOMMENT', r'(///.*)')
lg.add('COMMENT', r'(/\*(.|\n)*?\*/)|(//.*)')
lg.add('IMPLY', r'==>')
lg.add('SUB_ASSIGN', r'-=')
lg.add('ADD_ASSIGN', r'\+=')
lg.add('MUL_ASSIGN', r'\*=')
lg.add('MODULO', r'%')
lg.add('PLUS', r'\+')
lg.add('MINUS', r'-')
lg.add('MUL', r'\*')
lg.add('DIV', r'/')
lg.add('LEQ', r'<=')
lg.add('GEQ', r'>=')
lg.add('POW', r'\^')
lg.add('BTRIGHT', r'>>')
lg.add('BTLEFT', r'<<')
lg.add('BITNEG', r'~')
lg.add('LT', r'<(?!<)')
lg.add('GT', r'>(?!>)')
lg.add('PIPE', r'\|')
lg.add('AMPERSAND', r'&')
lg.add('AND', r'and(?![_$a-zA-Z0-9])')
lg.add('OR', r'or(?![_$a-zA-Z0-9])')
lg.add('XOR', r'xor(?![_$a-zA-Z0-9])')
lg.add('NOT', r'not(?![_$a-zA-Z0-9])')
lg.add('DEQUALS', r'==')
lg.add('DIFFERENT', r'!=')
lg.add('OPEN_PARENS', r'\(')
lg.add('CLOSE_PARENS', r'\)')
lg.add('OPEN_BRACKETS', r'{')
lg.add('CLOSE_BRACKETS', r'}')
lg.add('OPEN_SQBRACKET', r'\[')
lg.add('CLOSE_SQBRACKET', r'\]')

lg.add('KERNEL', r'kernel(?=\s)')
lg.add('RETURN', r'return(?![_$a-zA-Z0-9])')
lg.add('IF', r'(if|where)(?![_$a-zA-Z0-9])')
lg.add('FOR', r'for(?![_$a-zA-Z0-9])')
lg.add('ENSURES', r'ensures(?![_$a-zA-Z0-9])')
lg.add('REQUIRES', r'requires(?![_$a-zA-Z0-9])')
lg.add('ELSE', r'else(?![_$a-zA-Z0-9])')
lg.add('LET', r'let(?![_$a-zA-Z0-9])')
lg.add('QUICKCHECK', r'quickcheck(?![_$a-zA-Z0-9])')
lg.add('FUNCTION', r'fn(?![_$a-zA-Z0-9])')

lg.add('RANGE', r'\.\.')
lg.add('DOT', r'\.(?!\.)')

lg.add('EQUALS', r'=')
lg.add('DDOTS', r':')
lg.add('COMMA', r',')
lg.add('SEMICOLON', r';')

lg.add('IN', r'in(?![_$a-zA-Z0-9])')
lg.add('OUT', r'out(?![_$a-zA-Z0-9])')
lg.add('STATE', r'state(?![_$a-zA-Z0-9])')

lg.add('PRIME', r'\'')
lg.add('IDENTIFIER', r'[_$]*[a-zA-Z0-9_$]+')
lg.ignore(r'\s+')

lexer = lg.build()
