class Term:
    pass


class Abs(Term):
    def __repr__(self) -> str:
        return "λ %s. %s" % (self.varname, repr(self.body))

    def __init__(self, varname: str, body: Term) -> None:
        self.varname = varname
        self.body = body


class App(Term):
    def __repr__(self) -> str:
        return "(%s %s)" % (repr(self.left), repr(self.right))

    def __init__(self, left: Term, right: Term) -> None:
        self.left = left
        self.right = right


class Var(Term):
    def __repr__(self) -> str:
        return self.varname

    def __init__(self, varname: str) -> None:
        self.varname = varname