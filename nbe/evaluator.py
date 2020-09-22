from typing import List, Tuple
from .terms import Term, Var, Abs, App
from .exceptions import EvaluationError
from . import context


class Value:
    pass


class VClosure(Value):
    def __init__(self, context: context.Context, name: str, term: Term):
        self.context = context
        self.name = name
        self.term = term


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
    else:
        raise EvaluationError("How to apply %s to %s?" % (repr(rator), repr(rand)))


def evaluate(context: context.Context, term: Term) -> Value:
    """Convers term into a value form
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


def run_program(term_context: List[Tuple[str, Term]], term: Term) -> Value:
    """Runs a term inside a value context, computed out of term_context thing
    """
    return evaluate(
        context=init_context(term_context), term=term
    )


def init_context(term_context: List[Tuple[str, Term]]) -> context.Context:
    current_value_context = context.Context()
    if not term_context:
        return context.Context()
    for (name, term) in term_context:
        value = evaluate(context=current_value_context, term=term)
        current_value_context = current_value_context.forkwith(name, value)
    return current_value_context
