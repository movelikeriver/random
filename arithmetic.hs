module Main (
       main
) where

import System.Random  --cabal install random
import System.Exit

getPair :: [Int] -> [(Int, Int)]
getPair [] = []
getPair [x] = []
getPair (x:y:s) = (x, y) : (getPair s)


--a Haskell FP recursive style to do for-loop equivalent in imperative language
ques :: [(Int, Int)] -> Int -> IO (Int)
ques [] sc = do
      putStrLn ""
      return sc
ques ((x,y):xs) sc = do
     putStrLn ((show x) ++ " + " ++ (show y) ++ " = ?")
     let expect = x+y
     actual <- readLn :: IO Int
     if actual == expect
     then do
          putStrLn "Right!"
          ques xs (sc+1)
     else do
          putStrLn "Wrong!"
          ques xs sc


--main :: IO ExitCode
main = do
     putStrLn "How many questions do you want (3-20)?"
     totalnum <- readLn :: IO Int

     if totalnum < 3
     then do
          putStrLn ("Please input a digit >= 3, exit...")
          exitFailure
     else putStrLn "Start..."

     g <- getStdGen
     let ss = take (totalnum*2) (randomRs (0, 9) g :: [Int])
     let pairs = getPair ss
     score <- ques pairs 0
     putStrLn ("Full score: " ++ (show totalnum) ++ ". Your score: " ++ (show score))
