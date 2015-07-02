-- everything about tree and bin-tree

module Main (
       main
) where

-- Arbitrary tree
data Tree a = Node a [Tree a] deriving Show

treeHeight (Node _ []) = 1
treeHeight (Node _ xs) = 1 + maximum (map treeHeight xs)

treeSum (Node x []) = x
treeSum (Node x xs) = x + (foldr (+) 0 (map treeSum xs))

treeMax (Node x []) = x
treeMax (Node x xs) = maximum (x : (map treeMax xs))

treePreorder (Node x []) = [x]
treePreorder (Node x xs) = [x] ++ (foldr (++) [] (map treePreorder xs))

treePosorder (Node x []) = [x]
treePosorder (Node x xs) = (foldr (++) [] (map treePosorder xs)) ++ [x]


-- Binary tree
data BinTree a = Empty | Leaf a (BinTree a) (BinTree a) deriving Show

binTreeHeight Empty = 0
binTreeHeight (Leaf _ l r) = 1 + maximum (map binTreeHeight [l, r])

binTreeSum Empty = 0
binTreeSum (Leaf x l r) = x + binTreeSum l + binTreeSum r

binTreeMax Empty = 0
binTreeMax (Leaf x l r) = maximum (x : (map binTreeMax [l, r]))

binTreePreorder Empty = []
binTreePreorder (Leaf x l r) = [x] ++ (foldr (++) [] (map binTreePreorder [l, r]))

binTreeInorder Empty = []
binTreeInorder (Leaf x l r) = (binTreeInorder l) ++ [x] ++ (binTreeInorder r)

binTreePosorder Empty = []
binTreePosorder (Leaf x l r) = (foldr (++) [] (map binTreePosorder [l, r])) ++ [x]


main = do
     let t1 = Node 3 [
                   Node 4 [],
                   Node 5 [
                        Node 8 [],
                        Node 9 [
                             Node 10 []
                        ]
                   ],
                   Node 6 []
              ]
     print t1
     print ("height:" ++ show (treeHeight t1),
            "sum:" ++ show (treeSum t1),
            "max:" ++ show (treeMax t1))
     print ("treePreorder:", treePreorder t1)
     print ("treePosorder:", treePosorder t1)

     let t2 = Leaf 3
                  (Leaf 4
                      (Leaf 5 Empty Empty)
                      (Leaf 6
                          Empty
                          (Leaf 7 Empty Empty))
                  )
                  (Leaf 3 Empty Empty)
     print t2
     print ("height:" ++ show (binTreeHeight t2),
            "sum:" ++ show (binTreeSum t2),
            "max:" ++ show (binTreeMax t2))
     print ("binTreePreorder:", binTreePreorder t2)
     print ("binTreeInorder:", binTreeInorder t2)
     print ("binTreePosorder:", binTreePosorder t2)
