#!/usr/bin/env lispy
; print out the fibonacci sequence

(defun fib (n)
    (if (< n 2)
        1
        (+ (fib (- n 1)) (fib (- n 2)))))


(let default 10)


(defun try-get-int (x) (try (int x) default))


(defun get-length (get-arg args)
    (if (< 1 (length args))
        (try-get-int (get-arg args))
        default))


(defun fibonacci (args)
    (print (map fib (range (get-length (compose car cdr) args)))))


(fibonacci args)
