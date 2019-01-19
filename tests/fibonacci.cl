#!/usr/bin/env lispy
; print out the fibonacci sequence

(defun fib (n)
    (if (< n 2)
        1
        (+ (fib (- n 1)) (fib (- n 2)))))


(let default 10)


(defun try-get-int (x)
    (try
        (int x)
        (do (print error)
            default)))


(defun get-length (get-arg args) ; gets the length of the sequence to print
    (if (< 1 (length args))
        (try-get-int (get-arg args))
        default))


(defun fibonacci (args) ; main
    (do (let arg1 (compose car cdr))
        (let len (get-length arg1 args))
        (let sequence (map fib (range len)))
        (print sequence)))


(fibonacci args)
