module Main where

ques :: Int -> Int -> ([Char], [Char])
ques x y = ((show x) ++ " + " ++ (show y) ++ " = ?", show (x+y))

main = do
     let (q, a) = ques 3 4
     putStrLn q
     i <- getLine
     putStrLn (if a == i
               then "Right!"
               else "Wrong!")
