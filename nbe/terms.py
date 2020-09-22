from __future__ import annotations


class Term:
    """Base class for every syntactic term form."""
    def __eq__(self, other: Term) -> bool:
        return type(self) == type(other) and repr(self) == repr(other)


class Abs(Term):
    """Lambda abstraction."""
    def __repr__(self) -> str:
        return "λ %s. %s" % (self.varname, repr(self.body))

    def __init__(self, varname: str, body: Term) -> None:
        self.varname = varname
        self.body = body


class App(Term):
    """Term application."""
    def __repr__(self) -> str:
        return "(%s %s)" % (repr(self.left), repr(self.right))

    def __init__(self, left: Term, right: Term) -> None:
        self.left = left
        self.right = right


class Var(Term):
    """Just a plain variable."""
    def __repr__(self) -> str:
        return self.varname

    def __init__(self, varname: str) -> None:
        self.varname = varname
