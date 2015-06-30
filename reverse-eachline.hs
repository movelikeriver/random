--given a file containing some text, create an output file with everything in reverse in each line

module Main (
       main
) where

import System.IO

main = do
     theInput <- readFile "input.txt"
     let ins = lines theInput
     let ins2 = map (\x -> (reverse x) ++ "\n") ins
     writeFile "output.txt" (foldr (++) "" ins2)
