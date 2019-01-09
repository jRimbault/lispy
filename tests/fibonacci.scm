#!/usr/bin/env lispy
; print out the fibonacci sequence

(defun fib (n)
    (if (< n 2)
        1
        (+ (fib (- n 1)) (fib (- n 2)))))


(defun get-length (get-arg args)
    (if (< 1 (length args))
        (int (get-arg args))
        10))


(defun fibonacci (args)
    (print (map fib (range (get-length (compose car cdr) args)))))


(fibonacci args)
