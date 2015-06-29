module Main (
       main
) where

import System.Random  --cabal install random


getPair :: [Int] -> [(Int, Int)]
getPair [] = []
getPair [x] = []
getPair (x:y:s) = (x, y) : (getPair s)


ques :: [(Int, Int)] -> IO ()
ques [] = putStrLn ""
ques ((x,y):xs) = do
     putStrLn ((show x) ++ " + " ++ (show y) ++ " = ?")
     let expect = x+y
     actual <- readLn :: IO Int
     if actual == expect
     then putStrLn "Right!"
     else putStrLn "Wrong!"
     ques xs  --a Haskell FP recursive style to do for-loop equivalent in imperative language


main = do
     putStrLn "How many questions do you want (3-20)?"
     totalnum <- readLn :: IO Int

     g <- getStdGen
     let ss = take (totalnum*2) (randomRs (0, 9) g :: [Int])
     let pairs = getPair ss
     ques pairs
