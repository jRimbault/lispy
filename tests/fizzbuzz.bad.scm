(defun divisible (x y) (= 0 (% x y)))

(defun fizzbuzz (i)
    (cond
        ((divisible i 15) (quote FizzBuzz))
        ((divisible i 3)  (quote Fizz))
        ((divisible i 5)  (quote Buzz))
        (else             i)))

(print (map fizzbuzz (range 1 101)))

; (map (lambda (i)
;     (display
;         (cond
;             ((= 0 (% i 15)) (quote FizzBuzz))
;             ((= 0 (% i 3)) (quote Fizz))
;             ((= 0 (% i 5)) (quote Buzz))
;             (else             i))))
;     (range 1 101))
