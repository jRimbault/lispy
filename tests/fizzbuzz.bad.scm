; TODO implement 'cond'
(define fizzbuzz (lambda (x)
    (if (= 0 (% x 3))
        (if (= 0 (% x 5))
            (quote FizzBuzz)
            (quote Fizz))
        (if (= 0 (% x 5))
            (quote Buzz)
            x))))

(map display (map fizzbuzz (range 1 101)))
