from __future__ import annotations
from dataclasses import dataclass


@dataclass
class Term:
    """Base class for every syntactic term form."""
    def __eq__(self, other: Term) -> bool:
        return type(self) == type(other) and repr(self) == repr(other)


@dataclass
class Abs(Term):
    """Lambda abstraction."""
    varname: str
    body: Term

    def __repr__(self) -> str:
        return "λ %s. %s" % (self.varname, repr(self.body))


@dataclass
class App(Term):
    """Term application."""
    left: Term
    right: Term

    def __repr__(self) -> str:
        return "(%s %s)" % (repr(self.left), repr(self.right))


@dataclass
class Var(Term):
    """Just a plain variable."""
    varname: str

    def __repr__(self) -> str:
        return self.varname
