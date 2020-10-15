import pytest


from nbe.evaluator import run_program
from nbe.terms import Var, Abs, App, Term


def to_church(value: int) -> Term:
    if value <= 0:
        return Var("zero")
    else:
        return App(Var("add1"), to_church(value - 1))


CASES = [
# ------------------------------------------------------------------------------
    (
        [
            # Definition of zero
            # \f. \x. x
            (
                "zero", 
                Abs(
                    "f",
                    body=Abs(varname="x", body=Var("x"))
                )
            ),
            # Definition of succ or add1 function
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
            # Definition of the + operator for Church numerals
            # \j. \k. \f. \x. j f (k f x)
            (
                "+", 
                Abs(
                    "j",
                    body=Abs(
                        "k",
                        body=Abs(
                            "f",
                            body=Abs(
                                "x",
                                body=App(
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
        # Now we a ready to define the term 2 + 3
        App(
            App(
                Var("+"), to_church(2)
            ),
            to_church(3)
        ),
        # Which, being normalized, is expected to be equal 5
        Abs(
            "f",
            Abs(
                "x",
                App(
                    Var("f"),
                    App(
                        Var("f"),
                        App(
                            Var("f"),
                            App(
                                Var("f"),
                                App(
                                    Var("f"), Var("x")
                                )
                            )
                        )
                    )
                )
            )
        ),
    ),
]


@pytest.mark.parametrize("context,program,expected", CASES)
def test_runner(context, program, expected):
    normal_form = run_program(term_context=context, term=program)
    print(normal_form)
    assert normal_form == expected
