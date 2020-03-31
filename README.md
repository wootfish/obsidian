# obsidian

You will need Python 3.7 or higher.

Setup instructions:

```
$ python3 -m venv venv
$ source venv/bin/activate
(venv) $ pip install -e .
(venv) $ pysmt-install --z3
```

If all goes well, you should be able to run `python examples/circle_and_square.py` with your virtualenv active and see no errors (aside from the deprecation warning).
