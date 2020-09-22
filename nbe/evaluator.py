from __future__ import annotations


from typing import List, Tuple


from .terms import Term, Var, Abs, App
from .exceptions import EvaluationError

# to avoid import cycles
from . import context


class Value:
    """Base class for every value"""
    pass


class Neutral:
    """Base class for every neutral value"""
    pass


class NVar(Neutral):
    def __init__(self, varname: str) -> None:
        self.varname = varname


class NApp(Neutral):
    def __init__(self, left: Neutral, right: Value) -> None:
        self.left = left
        self.right = right


class VClosure(Value):
    """A closure value
    """
    def __init__(self, context: context.Context, name: str, term: Term):
        self.context = context
        self.name = name
        self.term = term


class VNeutral(Value):
    """A neutral value
    """
    def __init__(self, neutral: Neutral) -> None:
        self.neutral = neutral


def fresh_name(names: List[str], name: str) -> str:
    if name not in names:
        return name
    else:
        return fresh_name(names, name + "'")


def lookupvar(context: context.Context, name: str) -> Value:
    get_result = context.get(name)
    if get_result is None:
        raise EvaluationError(
            "Variable %s is unbound in %s" % (name, repr(context))
        )

    return get_result


def do_apply(rator: Value, rand: Value) -> Value:
    """Performs application of one value on another
    """
    if isinstance(rator, VClosure):
        return evaluate(
            context=rator.context.forkwith(
                name=rator.name, value=rand
            ),
            term=rator.term
        )
    elif isinstance(rator, VNeutral):
        return VNeutral(NApp(rator.neutral, rand))
    else:
        raise EvaluationError("How to apply %s to %s?" % (repr(rator), repr(rand)))


def evaluate(context: context.Context, term: Term) -> Value:
    """Converts a term into it's value form.
    """
    if isinstance(term, Var):
        return lookupvar(context, term.varname)
    elif isinstance(term, Abs):
        return VClosure(context=context.fork(), name=term.varname, term=term.body)
    elif isinstance(term, App):
        return do_apply(
            evaluate(context, term.left),
            evaluate(context, term.right),
        )
    else:
        raise EvaluationError("How to evaluate %s?" % repr(term))


def init_context(term_context: List[Tuple[str, Term]]) -> context.Context:
    """Build the initial value context from name-term pairs.
    """
    current_value_context = context.Context()
    if not term_context:
        return context.Context()
    for (name, term) in term_context:
        value = evaluate(context=current_value_context, term=term)
        current_value_context = current_value_context.forkwith(name, value)
    return current_value_context


def read_back(names: List[str], value: Value) -> Term:
    """Reads back (or reifies) values into their term like form.
    """
    if isinstance(value, VNeutral):
        if isinstance(value.neutral, NVar):
            return Var(varname=value.neutral.varname)
        elif isinstance(value.neutral, NApp):
            return App(
                read_back(names, VNeutral(value.neutral.left)),
                read_back(names, value.neutral.right)
            )
        else:
            raise EvaluationError("%s value is misconfigured" % repr(value))
    elif isinstance(value, VClosure):
        new_name = fresh_name(names, value.name)
        return Abs(
            new_name,
            read_back(
                [new_name] + names, do_apply(value, VNeutral(NVar(new_name)))
            )
        )
    else:
        raise EvaluationError("How to read back %s?" % repr(value))


def normalize(term: Term) -> Term:
    """Here goes the magic - the combination of term evaluation followed by
    reading the result back into syntax form gives you a normal form.
    """
    return read_back(
        names=list(),
        value=evaluate(
            context=init_context(term_context=list()),
            term=term
        )
    )


def run_program(term_context: List[Tuple[str, Term]], term: Term) -> Term:
    """Runs a term inside a value context, computed out of term_context thing
    """
    return read_back(
        # geting names out of term_context
        names=[item[0] for item in term_context],
        value=evaluate(
            context=init_context(term_context), term=term
        )
    )
