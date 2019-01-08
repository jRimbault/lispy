#!/usr/bin/env lispy
; print out the fibonacci sequence

(let fib (lambda (n)
    (if (< n 2)
        1
        (+ (fib (- n 1)) (fib (- n 2))))))


(let l (cond
    ((< 1 (length args))
        (int (car (cdr args))))
    (else 10)))

(print (map fib (range l)))
