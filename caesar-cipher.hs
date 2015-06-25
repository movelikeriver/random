-- Q: Write a Caesar Cipher function called cipher
-- cipher :: [Char] -> Int -> [Char]
--
-- Usage:
--   ghc caesar-cipher.hs
--   ./caesar-cipher

import Data.Char

opLetter :: Char -> Int -> Char
opLetter x n
       | ((x >= 'a') && (x <= 'z')) = chr( (((ord x - 97) + n) `mod` 26) + 97)
       | ((x >= 'A') && (x <= 'Z')) = chr( (((ord x - 97) + n) `mod` 26) + 65)
       | otherwise = x

cipher :: [Char] -> Int -> [Char]
cipher [] n = []
cipher xs n = (opLetter (head xs) n) : (cipher (tail xs) n)


main = print (cipher "hello" 3)
