--cabal install random

module Main (
  main
  ) where

import System.Random

main = do
  g <- getStdGen
  print $ take 10 (randomRs ('a', 'z') g)
  print $ take 10 (randomRs ('0', '9') g)
  print $ take 10 (randomRs (0, 9) g :: [Double])
  print $ take 10 (randomRs ('0', '9') g)
  g2 <- getStdGen
  print $ take 10 (randomRs ('0', '9') g2)
