module Main (
       main
) where

removeFirst x [] = []
removeFirst x (y:ys)
        | x == y      = ys
        | otherwise   = y : removeFirst x ys

perms [] = [[]]
perms xs = [x:p | x <- xs, p <- perms (removeFirst x xs)]

revList :: [Int] -> [Int]
revList [] = []
revList (x:xs) = (revList xs) ++ [x]


main = do
     print (removeFirst 3 [1, 3, 2, 3])
     print (perms [1, 2, 2, 3])
     print (revList [1, 2, 3])
     print (foldl (++) "c" ["a", "b"])
     print (foldr (++) "c" ["a", "b"])
