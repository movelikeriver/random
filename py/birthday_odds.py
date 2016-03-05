"""
https://community.topcoder.com/stat?c=problem_statement&pm=1848&rd=4675

Problem Statement for BirthdayOdds
Problem Statement


Here is an interesting factoid: "On the planet Earth, if there are at least 23 people in a room, the chance that two of them have the same birthday is greater than 50%." You would like to come up with more factoids of this form. Given two integers (minOdds and daysInYear), your method should return the fewest number of people (from a planet where there are daysInYear days in each year) needed such that you can be at least minOdds% sure that two of the people have the same birthday. See example 0 for further information.
 
Definition

Class:BirthdayOdds
Method:minPeople
Parameters:int, int
Returns:int
Method signature:int minPeople(int minOdds, int daysInYear)
(be sure your method is public)
    
 
Notes
-Two people can have the same birthday without being born in the same year.
-You may assume that the odds of being born on a particular day are (1 / daysInYear).
-You may assume that there are no leap years.
 
Constraints
-minOdds will be between 1 and 99, inclusive.
-daysInYear will be between 1 and 10000, inclusive.
-For any number of people N, the odds that two people will have the same birthday (in a room with N people, on a planet with daysInYear days in each year) will not be within 1e-9 of minOdds. (In other words, you don't need to worry about floating-point precision for this problem.)
 
Examples
0)


75

5

Returns: 4

We must be 75% sure that at least two of the people in the room have the same birthday. This is equivalent to saying that the odds of everyone having different birthdays is 25% or less.

    If there is only one person in the room, the odds are 5/5 or 100% that nobody shares a birthday.
    If there are two people in the room, the odds are 5/5 * 4/5 = 80% that nobody shares a birthday. This is because the second person has 4 "safe" days on which his birthday could fall, out of 5 possible days in the year.
    If there are three people in the room, the odds of no overlap are 5/5 * 4/5 * 3/5 = 48%.
    If there are four people in the room, the odds are 5/5 * 4/5 * 3/5 * 2/5 = 19.2%. This means that you can be (100% - 19.2%) = 80.8% sure that two or more of them do, in fact, have the same birthday.

We only need to be 75% sure of this, which was untrue for three people but true for four. Therefore, your method should return 4.
1)


50

365

Returns: 23

The factoid from the problem statement. If there are 22 people in a room, the odds of a shared birthday are roughly 47.57%. With 23 people, these odds jump to 50.73%, which is greater than or equal to the 50% needed.
2)


1

365

Returns: 4

Another example from planet Earth. The odds of a repeat birthday among only four people are roughly 1.64%.
3)


84

9227

Returns: 184

This problem statement is the exclusive and proprietary property of TopCoder, Inc. Any unauthorized use or reproduction of this information without the prior written consent of TopCoder, Inc. is strictly prohibited. (c)2010, TopCoder, Inc. All rights reserved.
This problem was used for:
       Single Round Match 174 Round 1 - Division I, Level One
       Single Round Match 174 Round 1 - Division II, Level Two
"""


def min_people(min_odds, days_in_year):
    """It's the same as the problem below:

    Find min K for:
    1 * 364/365 * 363/365 * 362/365 * ... (365-K)/365 <= (1 - min_odds/100)
    """
    target = 1.0 - min_odds / 100.0
    k = 1
    p = 1
    while p > target:
        p *= (1.0 - float(k) / days_in_year)
        k += 1
    return k


# main

test_cases = [(75, 5, 4),
              (50, 365, 23)]
for (min_odds, days_in_year, ret) in test_cases:
    act = min_people(min_odds, days_in_year)
    print ret, '=', act
    assert ret == act

print 'PASS'

