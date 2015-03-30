import sys, copy

letters = "abcdefgh"
pieces = ['R', 'N', 'B', 'Q', 'K', 'B', 'N', 'R']

# Generates an empty board. for testing
def empty_board():
	board = {}
	for j in letters:
		board[j] = {1:"", 2:"", 3:"", 4:"", 5:"", 6:"", 7:"", 8:""}
	return board

# Returns an inital board setup
def initialize_board():
	board = {}
	for j in letters:
		board[j] = {1:"", 2:"", 3:"", 4:"", 5:"", 6:"", 7:"", 8:""}

	# Add white pieces to board
	for i in range(len(letters)):
		board[letters[i]][1] = ('w' + pieces[i])
	# Add black pieces to board
	for i in range(len(letters)):
		board[letters[i]][8] = ('b' + pieces[i])
	# Add white pawns to board
	for i in range(len(letters)):
		board[letters[i]][2] = 'wp'
	# Add black pawns to board
	for i in range(len(letters)):
		board[letters[i]][7] = 'bp'

	return board


def square_is_black(let, num):
	return (((ord(let) + num) % 2) == 1)

def lookup(board, square):
	return board[square[0]][int(square[1])]

def square_lookup(board, piece):
	pawns = 0
	pawn_loc = ''
	for letter in letters:
		for num in range(1, 9):
			p = board[letter][num]
			if p:
				if p[1] == 'p':
					pawns = pawns + 1
					pawn_loc = p
				else:
					if p == piece:
						return (letter + str(num))
	if piece[1] == 'p':
		if pawns == 1:
			return pawn_loc
		if pawns == 0:
			raise Exception("There aren't any pawns, you twat")
		if pawns > 1:
			raise Exception("There are multiple pawns, you twat")
	else:
		return ""
		



def print_board(board):
	buf = "\n  "
	for i in range(25):
		buf = buf + '_'
	buf = buf + '\n'

	for i in range(8, 0, -1):
		for let in letters:
			if let == 'a':
				buf = buf + str(i) + ' '
			cell = board[let][i]
			if not cell:
				if square_is_black(let, i):
					buf = buf + '|::'
				else:
					buf = buf + '|  '
			else:
				buf = buf + '|' + cell
		buf = buf + '|\n'
	buf = buf + '  '
	for i in range(25):
		buf = buf + '-'
	buf = buf + '\n   '
	for let in letters:
		buf = buf + let + '  '
	buf = buf + '\n'
	sys.stdout.write(buf)

# Makes move and returns new board. completely disregards check or 
# color rules.
def move(board, fro, to):
	p = board[fro[0]][int(fro[1])]
	if not p:
		raise Exception("No piece to move on this square.")
	new_board = copy.deepcopy(board)
	new_board[fro[0]][int(fro[1])] = ""
	new_board[to[0]][int(to[1])] = p
	return new_board

# takes a board, a turn, and a square. If the piece on the square
# is not the same color as the piece making the move, or the piece
# is a king, then cannot take.
def can_take_on(board, sq_let, sq_num, white):
	p = board[sq_let][sq_num]
	if p == "":
		raise Exception("Tried to capture on an empty square")
	if white:
		if p[0] == 'w':
			return False
		else:
			return True
	else:
		if p[0] == 'b':
			return False
		else:
			return True

# Where a given piece could move if there were
# no other pieces on the board
#   def get_theoretical_piece_moves(board, sq_num, sq_let):

# Gets possible moves, disregarding check. requires a prev
# (previous move location) to check for en passant.

def get_possible_moves(board, sq_let, sq_num, ep=None):
	piece = board[sq_let][sq_num]
	white_turn = (piece[0] == 'w')
	moveable_squares = []
	p = piece[1]

	# A rook can move up down left or right.
	if p == 'R':
		# iterate down. Constant letter index.
		it_d = range(sq_num - 1, 0, -1)
		for num in it_d:
			if board[sq_let][num]:
				if can_take_on(board, sq_let, num, white_turn):
					moveable_squares.append(sq_let + str(num))	
				break
			else:
				moveable_squares.append(sq_let + str(num))

		# iterate up. Constant letter index.
		it_u = range(sq_num + 1, 9)
		for num in it_u:
			if board[sq_let][num]:
				if can_take_on(board, sq_let, num, white_turn):
					moveable_squares.append(sq_let + str(num))	
				break
			else:
				moveable_squares.append(sq_let + str(num))

		# iterate left. Constant number index.
		it_l = (letters.split(sq_let))[0][::-1]
		for ch in it_l:
			if board[ch][sq_num]:
				if can_take_on(board, ch, sq_num, white_turn):
					moveable_squares.append(ch + str(sq_num))	
				break
			else:
				moveable_squares.append(ch + str(sq_num))

		# iterate right. Constant number index.
		it_r = (letters.split(sq_let))[1]
		for ch in it_r:
			if board[ch][sq_num]:
				if can_take_on(board, ch, sq_num, white_turn):
					moveable_squares.append(ch + str(sq_num))	
				break
			else:
				moveable_squares.append(ch + str(sq_num))

		return moveable_squares


	elif p == 'N':
		# [letter delta, number delta]
		deltas = [[1, 2], [2, 1], [2, -1], [1, -2], [-1, -2], [-2, -1], [-2, 1], [-1, 2]]
		for d in deltas:
			new_l = chr(ord(sq_let) + d[0])
			new_n = sq_num + d[1]
			if (new_l in letters) and (new_n in range(1, 9)):
				if board[new_l][new_n]:
					if can_take_on(board, new_l, new_n, white_turn):
						moveable_squares.append(new_l + str(new_n))
				else:
					moveable_squares.append(new_l + str(new_n))
		return moveable_squares
	elif p == 'B':
		deltas_ur = []
		deltas_dr = []
		deltas_dl = []
		deltas_ul = []
		for i in range(1, 8):
			deltas_ur.append([i, i])
			deltas_dr.append([i, -i])
			deltas_dl.append([-i, -i])
			deltas_ul.append([-i, i])
		deltas = [deltas_ur, deltas_dr, deltas_dl, deltas_ul]
		for d in deltas:
			for poss in d:
				new_l = chr(ord(sq_let) + poss[0])
				new_n = sq_num + poss[1]
				if (new_l in letters) and (new_n in range(1, 9)):
					if board[new_l][new_n]:
						if can_take_on(board, new_l, new_n, white_turn):
							moveable_squares.append(new_l + str(new_n))	
						break
					else:
						moveable_squares.append(new_l + str(new_n))
		return moveable_squares

	# Same as all of the moves a rook and a bishop combined could make.
	# a pretty chessy solution.
	elif p == 'Q':
		b = board
		symbol = 'w' if white_turn else 'b'
		b[sq_let][sq_num] = symbol + 'R'
		r_moves = get_possible_moves(b, sq_let, sq_num)
		b[sq_let][sq_num] = symbol + 'B'
		b_moves = get_possible_moves(b, sq_let, sq_num)
		return r_moves + b_moves
	elif p == 'K':
		deltas = [[-1, 1], [0, 1], [1, 1], [1, 0], [1, -1], [0, -1], [-1, -1], [-1, 0]]
		for d in deltas:
			if (chr(ord(sq_let) + d[0])) in letters and (sq_num + d[1]) in range(1, 9):
				sq = (chr(ord(sq_let) + d[0])) + str(sq_num + d[1])
				val = lookup(board, sq)
				if val:
					if can_take_on(board, sq[0], int(sq[1]), white_turn):
						moveable_squares.append(sq)
				else:
					moveable_squares.append(sq)
		return moveable_squares
	elif p == 'p':
		if white_turn:
			if (sq_num + 1) in range(1, 9):
				#Directly forward
				ahead = board[sq_let][sq_num + 1]
				if not ahead:
					moveable_squares.append(sq_let + str(sq_num + 1))

				# Two squares forward, if from first rank
				two_ahead = board[sq_let][sq_num + 2]
				if (not ahead) and (not two_ahead) and (sq_num == 2):
					moveable_squares.append(sq_let + str(sq_num + 2))

				# Taking diagonally
				front_left = chr(ord(sq_let) - 1) + str(sq_num + 1)
				if front_left[0] in letters:
					val = lookup(board, front_left)
					if val:
						if val[0] == 'b':
							moveable_squares.append(front_left)
				front_right = chr(ord(sq_let) + 1) + str(sq_num + 1)
				if front_right[0] in letters:
					val = lookup(board, front_right)
					if val:
						if val[0] == 'b':
							moveable_squares.append(front_right)
				right_neighbor = chr(ord(sq_let) + 1) + str(sq_num)
				left_neighbor = chr(ord(sq_let) - 1) + str(sq_num)

				# En passant
				if ep:
					if ep == right_neighbor:
						moveable_squares.append(front_right)
					if ep == left_neighbor:
						moveable_squares.append(front_left)

		else:
			if (sq_num - 1) in range(1, 9):
				#Directly forward
				ahead = board[sq_let][sq_num - 1]
				if not ahead:
					moveable_squares.append(sq_let + str(sq_num - 1))
				
				# Two squares forward, if from first rank
				two_ahead = board[sq_let][sq_num - 2]
				if (not ahead) and (not two_ahead) and (sq_num == 7):
					moveable_squares.append(sq_let + str(sq_num - 2))

				# Taking diagonally
				front_left = chr(ord(sq_let) + 1) + str(sq_num - 1)
				if front_left[0] in letters:
					val = lookup(board, front_left)
					if val:
						if val[0] == 'w':
							moveable_squares.append(front_left)
				front_right = chr(ord(sq_let) - 1) + str(sq_num - 1)
				if front_right[0] in letters:
					val = lookup(board, front_right)
					if val:
						if val[0] == 'w':
							moveable_squares.append(front_right)
				right_neighbor = chr(ord(sq_let) - 1) + str(sq_num)
				left_neighbor = chr(ord(sq_let) + 1) + str(sq_num)

				# En passant
				if ep:
					if ep == right_neighbor:
						moveable_squares.append(front_right)
					if ep == left_neighbor:
						moveable_squares.append(front_left)
		return moveable_squares

	else:
		raise Exception("This square is empty.")


def in_check(board, white):
	color = 'w' if white else 'b'
	opp_color = 'b' if white else 'w'
	king = color + 'K'
	king_loc = square_lookup(board, king)
	for letter in letters:
		for num in range(1, 9):
			address = letter + str(num)
			val = lookup(board, address)
			if val:
				if val[0] == opp_color:
					if king_loc in get_possible_moves(board, letter, num):
						return True
	return False

# Iterate through every single potential move.
# if still in check after every one of those moves,
# then it is checkmate.
def is_mated(board, white, ep=None):
	color = 'w' if white else 'b'
	for letter in letters:
		for num in range(1, 9):
			address = letter + str(num)
			val = lookup(board, address)
			if val:
				if val[0] == color:
					for m in get_possible_moves(board, letter, num, ep):
						test_board = copy.deepcopy(board)
						b = move(test_board, address, m)
						if not in_check(b, white):
							return False
	return True


def play_computer():
	pass

def play_opponent():
	pass


#############
## Testing ##
#############


def test_get_moves_pawn():
	a = initialize_board()
	poss = get_possible_moves(a, 'e', 2)
	assert(set(poss) == set(['e3', 'e4']))
	a = move(a, 'e2', 'e5')
	a = move(a, 'd7', 'd5')
	poss = get_possible_moves(a, 'e', 5, 'd5')
	assert(set(poss) == set(['d6', 'e6']))

def test_get_moves_knight():
	a = initialize_board()
	poss = get_possible_moves(a, 'b', 1)
	assert(set(poss) == set(['a3', 'c3']))
	a = move(a, 'b1', 'c3')
	poss = get_possible_moves(a, 'c', 3)
	assert(set(poss) == set(['a4', 'b5', 'd5', 'e4', 'b1']))


def test_is_mated():
	a = initialize_board()
	a = move(a, 'f2', 'f4')
	assert(in_check(a, True) == False)
	assert(is_mated(a, True) == False)
	assert(in_check(a, False) == False)
	assert(is_mated(a, False) == False)
	a = move(a, 'e7', 'e6')
	a = move(a, 'g2', 'g4')
	assert(in_check(a, True) == False)
	assert(is_mated(a, True) == False)
	assert(in_check(a, False) == False)
	assert(is_mated(a, False) == False)
	a = move(a, 'd8', 'h4')
	assert(in_check(a, True) == True)
	assert(is_mated(a, True) == True)


def run_tests():
	test_get_moves_pawn()
	test_get_moves_knight()
	test_is_mated()
	print "All tests passed."


run_tests()




