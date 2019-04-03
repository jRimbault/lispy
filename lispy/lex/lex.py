from rply import LexerGenerator


lg = LexerGenerator()

end_quote = r"(?![\s\)\]\}])"

identifier = r'[^()\[\]{}\'"\s;]+'

lg.add("LPAREN", r"\(")
lg.add("RPAREN", r"\)")
lg.add("LBRACKET", r"\[")
lg.add("RBRACKET", r"\]")
lg.add("LCURLY", r"\{")
lg.add("RCURLY", r"\}")
lg.add("HLCURLY", r"#\{")
lg.add("QUOTE", r"\'%s" % end_quote)
lg.add("QUASIQUOTE", r"`%s" % end_quote)
lg.add("UNQUOTESPLICE", r"~@%s" % end_quote)
lg.add("UNQUOTE", r"~%s" % end_quote)
lg.add("DISCARD", r"#_")
lg.add("HASHSTARS", r"#\*+")
lg.add(
    "BRACKETSTRING",
    r"""(?x)
    \# \[ ( [^\[\]]* ) \[
    \n?
    ((?:\n|.)*?)
    \] \1 \]
    """,
)
lg.add("HASHOTHER", r"#%s" % identifier)
lg.add("IDENTIFIER", identifier)

lg.ignore(r";.*(?=\r|\n|$)")
lg.ignore(r"\s+")

lexer = lg.build()
