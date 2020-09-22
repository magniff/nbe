import pytest


from nbe.evaluator import run_program
from nbe.terms import Var, Abs, App, Term


def to_church(value: int) -> Term:
    if value <= 0:
        return Var("zero")
    else:
        return App(Var("add1"), to_church(value - 1))


CASES = [
    (
# ------------------------------------------------------------------------------
        [
            # \f. \x. x
            (
                "zero", 
                Abs(
                    "f",
                    body=Abs(varname="x", body=Var("x"))
                )
            ),
            # \n. \f. \x. f (n f x)
            (
                "add1", 
                Abs(
                    "n",
                    body=Abs(
                        varname="f", body=Abs(
                            "x", body=App(
                                Var("f"),
                                App(
                                    App(
                                        Var("n"), Var("f")
                                    ),
                                    Var("x")
                                )
                            )
                        )
                    )
                )
            ),
            # \j. \k. \f. \x. j f (k f x)
            (
                "+", 
                Abs(
                    "j",
                    body=Abs(
                        "k", body=Abs(
                            "f", body=Abs(
                                "x", body=App(
                                    App(
                                        Var("j"), Var("f")
                                    ),
                                    App(
                                        App(
                                            Var("k"), Var("f")
                                        ),
                                        Var("x")
                                    )
                                )
                            )
                        )
                    )
                )
            ),
        ],
        App(
            App(
                Var("+"), to_church(2)
            ),
            to_church(3)
        ),
        None,
    ),
# ------------------------------------------------------------------------------
]


@pytest.mark.parametrize("context,program,expected", CASES)
def test_runner(context, program, expected):
    print(run_program(term_context=context, term=program))
