-- A strong password has
--    at least 15 characters
--    uppercase letters
--    lowercase letters
--    numbers

import Data.Char

strong :: String -> Bool
strong xs
       | (length xs) < 15 = False
       | not (any (Data.Char.isNumber) xs) = False
       | not (any (Data.Char.isUpper) xs) = False
       | not (any (Data.Char.isLower) xs) = False
       | otherwise = True


strong2 :: String -> Bool
strong2 xs = all ($ xs) [minLen,
                         any Data.Char.isUpper,
                         any Data.Char.isLower,
                         any Data.Char.isNumber
                        ]
      where minLen s = length s > 14

main = print (strong2 "laksjfawFeoafe1ff")
