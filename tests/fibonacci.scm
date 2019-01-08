#!/usr/bin/env lispy
; print out the fibonacci sequence

(let fib (lambda (n)
    (if (< n 2)
        1
        (+ (fib (- n 1)) (fib (- n 2))))))
(print (map fib (range 10)))
