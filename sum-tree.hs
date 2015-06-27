--sum up all the nodes/leaves of a tree.

data Tree2 a = Leaf a | Node2 a (Tree2 a) (Tree2 a) deriving (Show, Eq)
leafTree :: Tree2 Int
leafTree =
         Node2 3
           (Node2 4
              (Leaf 1) (Leaf 2)
           )
           (Leaf 5)

add :: Tree2 Int -> Int
add (Leaf x) = x
add (Node2 x l r) = x + add(l) + add(r)

bb = add leafTree


main = print (bb)
