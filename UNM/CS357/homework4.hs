module Homework4 where

--No other imports allowed
import qualified Data.List as L

--4.1 Genome Lists (40pts)
possibleDNA :: String
possibleDNA = "AGCT"


insertions :: String -> [String]
insertions xs = concatMap (insertionHelper xs) indices
	where indices = [0..(length xs)]


-- Each time helper is run, it should generate 4 lists,
-- i.e. "GC" 0 gives ["AGC", "GGC", "CGC", "TGC"]
insertionHelper :: String -> Int -> [String]
insertionHelper xs index = [ys ++ [x] ++ zs | x <- possibleDNA]
	where (ys, zs) = splitAt index xs


deletions :: String -> [String]
deletions xs = map (deleteHelper xs) indices
	where indices = [0..((length xs) - 1)]


-- Takes a string and returns a new string with the index removed
deleteHelper :: String -> Int -> String
deleteHelper xs index = ys ++ zs
	where (ys, z:zs) = splitAt index xs


substitutions :: String -> [String]
substitutions xs = concatMap (subsHelper xs) indices
	where indices = [0..(length xs - 1)]


subsHelper :: String -> Int -> [String]
subsHelper xs index = [ys ++ [x] ++ zs | x <- possibleDNA]
	where (ys, z:zs) = splitAt index xs


-- Switch one character in place, then map the swapped character cons'ed onto
-- transpositions of remaining characters
transpositions :: String -> [String]
transpositions [x] = []
transpositions (x:y:ys) = (y:x:ys) : map (x:) (transpositions (y:ys))


--4.2 Sorting (20pts)
insert :: Ord a => a -> [a] -> [a]
insert num [] = [num]
insert num (x:xs) = if num <= x then num : x : xs else x : insert num xs

isort :: Ord a => [a] -> [a]
isort [] = []
isort (x:xs) = insert x (isort xs)

-- Lines gives each line, we sort all the lines and then concat+intersperse
-- "\n" (called intercalate). Lastly, we write to the file fn2.
fileisort :: String -> String -> IO ()
fileisort fn1 fn2 = writeFile fn2 (L.intercalate "\n" (isort (lines fn1)))


--4.3 Game Trees (40pts)
-- Instead of X and O, we use (R)ed and (G)reen
data Field = B | R | G
             deriving (Eq, Ord, Show)
type Board = [Field]

strategyForRed :: Board -> Int
strategyForRed board = bestMoveIndex board R

strategyForGreen :: Board -> Int
strategyForGreen board = bestMoveIndex board G


-- Adding a ton of code from the book below
size :: Int
size = 3

next :: Field -> Field
next G = R
next B = B
next R = G


empty :: Board
empty = replicate (size * size) B

full :: Board -> Bool
full = all (/= B)

turn :: Board -> Field
turn g = if os <= xs then G else R
	where
		os = length (filter (== G) g)
		xs = length (filter (== R) g)

wins :: Field -> Board -> Bool
wins p g = any line (rows ++ cols ++ dias)
	where
		line = all (== p)
		rows = [[g !! (offset + (n * size)) | offset <- [0..size-1]  ] | n <- [0..size-1]]
		cols = [[g !! ((n * size) + offset) | n <- [0..size-1]] | offset <- [0..size-1]]
		dias = [diag g, diag (reverse g)]


diag :: Board -> [Field]
diag g = [g !! ((n * size) + n) | n <- [0..size-1]]


won :: Board -> Bool
won g = wins G g || wins R g


valid :: Board -> Int -> Bool
valid g i = 0 <= i && i < size^2 && g !! i == B


move :: Board -> Int -> Field -> [Board]
move g i p =
	if valid g i then [xs ++ [p] ++ ys] else []
	where (xs, B:ys) = splitAt i g

--chop :: Int -> [a] -> [[a]]
--chop n [] = []
--chop n xs = take n xs : chop n (drop n xs)

data Tree a = Node a [Tree a]
							deriving Show

gametree :: Board -> Field -> Tree Board
gametree g p = Node g [gametree g' (next p) | g' <- moves g p]

moves :: Board -> Field -> [Board]
moves g p
	| won g = []
	| full g = []
	| otherwise = concat [move g i p | i <- [0..(size^2)-1]]

prune :: Int -> Tree a -> Tree a
prune 0 (Node x _) = Node x []
prune n (Node x ts) = Node x [prune (n-1) t | t <- ts]

depth :: Int
depth = 9

minimax :: Tree Board -> Tree (Board, Field)
minimax (Node g [])
	| wins G g = Node (g,G) []
	| wins R g = Node (g,R) []
	| otherwise = Node (g,B) []
minimax (Node g ts)
	| turn g == G = Node (g, minimum ps) ts'
	| turn g == R = Node (g, maximum ps) ts'
		where
			ts' = map minimax ts
			ps = [p | Node (_,p) _ <- ts']

bestmove :: Board -> Field -> Board
bestmove g p = head [g' | Node (g', p') _ <- ts, p' == best]
							where
								tree = prune depth (gametree g p)
								Node (_,best) ts = minimax tree

-- Best move is great because it gives us the board with the best move,
-- but what if I just want the index of the best move?
bestMoveIndex :: Board -> Field -> Int
bestMoveIndex oldB f = diffIndex oldB newB
	where newB = bestmove oldB f

-- Takes 2 boards, finds the element that is different and returns it's index
diffIndex :: Board -> Board -> Int
diffIndex (x:xs) (y:ys) = if x /= y then 0 else 1 + diffIndex xs ys


--4.4 (Optional) Drawing Game Trees and Strategies (30pts EC)
drawStrategy :: Bool -> String -> IO ()
drawStrategy = undefined
