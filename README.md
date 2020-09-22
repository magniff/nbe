# nbe
[Normalization by Evaluation](https://en.wikipedia.org/wiki/Normalisation_by_evaluation) (NbE for short) done in Python.
The only test example I've provided shows how the algorithm handles normalization of the term `(2 + 3)`, encoded ala Church.

```bash
$ pytest tests/ -s
. tests/test_runner.py λ f. λ x. (f (f (f (f (f x)))))  # aka 5
```
