[![Build Status](https://travis-ci.com/jRimbault/lispy.svg?token=CwMJm5Y5zqHzpCQTevzz&branch=master)](https://travis-ci.com/jRimbault/lispy)

Depends on Python 3.6

```bash
$ ./bin/lispy
Welcome to the lispy interpreter
(lispy) > (let tenner (range 10))
(lispy) > (map (lambda x (+ x 1)) tenner)
(1 2 3 4 5 6 7 8 9 10)
(lispy) >
$ ./bin/lispy tests/fibonacci.cl 10
(1 1 2 3 5 8 13 21 34 55)
```

Building a standalone executable :
```bash
$ make freeze
# or
$ pip install --user pyinstaller
$ pyinstaller bin/lispybin.py -n lispy --onefile
```

Running tests :
```bash
$ make tests
# or
$ pip install --user pytest
$ pytest
```
