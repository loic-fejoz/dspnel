from rply import LexerGenerator

lg = LexerGenerator()

lg.add('NUMBER', r'\d+(\.\d+)?(e(-)?\d+)?(i|j)?')

lg.add('PLUS', r'\+')
lg.add('MINUS', r'-')
lg.add('MUL', r'\*')
lg.add('DIV', r'/')
lg.add('LT', r'<')
lg.add('GT', r'>')
lg.add('OPEN_PARENS', r'\(')
lg.add('CLOSE_PARENS', r'\)')
lg.add('OPEN_BRACKETS', r'{')
lg.add('CLOSE_BRACKETS', r'}')
lg.add('OPEN_SQBRACKET', r'\[')
lg.add('CLOSE_SQBRACKET', r'\]')

lg.add('KERNEL', r'kernel')
lg.add('RETURN', r'return')
lg.add('IF', r'if')
lg.add('FOR', r'for')
lg.add('ENSURES', r'ensures')
lg.add('REQUIRES', r'requires')
lg.add('ELSE', r'else')
lg.add('LET', r'let')
lg.add('QUICKCHECK', r'quickek')
lg.add('FUNCTION', r'fn')

lg.add('RANGE', r'\.\.')
lg.add('DOT', r'\.')

lg.add('EQUALS', r'=')
lg.add('DDOTS', r':')
lg.add('COMMA', r',')
lg.add('SEMICOLON', r';')

lg.add('IN', r'in')
lg.add('OUT', r'out')
lg.add('STATE', r'state')


lg.add('IDENTIFIER', r'[_$]*[a-zA-Z0-9_$]+')
lg.ignore(r'\s+')

lexer = lg.build()