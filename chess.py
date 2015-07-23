import sys, copy, random, time

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

# Given a square, returns the piece that is on it.
def lookup(board, square):
	return board[square[0]][int(square[1])]

# Given a piece, returns the square it's on. Works for pawns
# when there is only one left, but please don't.
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

# Gets a promotion piece from the user
def promote(white, sq):
	color = 'w' if white else 'b'
	print "Please select a promotion piece for " + ("white" if white else "black") + " on square " + sq
	res = raw_input().upper()
	if res in 'QRBN':
		return (color + res.lower())
	print 'Not a valid promotion.'
	return promote(white)


# Makes move and returns new board. completely disregards check or 
# color rules, but includes promote
def move(board, fro, to):
	p = board[fro[0]][int(fro[1])]
	if not p:
		raise Exception("No piece to move on this square.")
	new_piece = None
	if (p[1] == 'p') and (to[1] == '1' or to[1] == '8'):
		new_piece = promote((True if p[0] == 'w' else False), to)
	new_board = copy.deepcopy(board)
	new_board[fro[0]][int(fro[1])] = ""
	new_board[to[0]][int(to[1])] = (new_piece if new_piece else p)
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
	elif p == 'Q':
		b = copy.deepcopy(board)
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
				if (sq_num + 1) in range(1, 9):
					ahead = board[sq_let][sq_num + 1]
					if not ahead:
						moveable_squares.append(sq_let + str(sq_num + 1))

				# Two squares forward, if from first rank
				if (sq_num + 2) in range(1, 9):
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
				if (sq_num - 1) in range(1, 9):
					ahead = board[sq_let][sq_num - 1]
					if not ahead:
						moveable_squares.append(sq_let + str(sq_num - 1))
				
				# Two squares forward, if from first rank
				if (sq_num - 2) in range(1, 9):
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

				# En passant
				if ep:
					right_neighbor = chr(ord(sq_let) - 1) + str(sq_num)
					left_neighbor = chr(ord(sq_let) + 1) + str(sq_num)
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

# Gets legal moves for a piece on a particular square.
def get_legal_moves(board, white, sq_let, sq_num, ep=None):
	result = []
	pos = sq_let + str(sq_num)
	for m in get_possible_moves(board, sq_let, sq_num, ep):
		new_board = move(copy.deepcopy(board), pos, m)
		if not in_check(new_board, white):
			result.append(m)
	return result

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

# gets all legal moves considering every piece on the board.
def get_all_legal_moves(board, white, ep):
	moves = []
	for letter in letters:
		for num in range(1, 9):
			piece = board[letter][num]
			if piece:
				piece_color = (True if (piece[0] == 'w') else False)
				if (piece_color == white):
					for m in get_legal_moves(board, white, letter, num, ep):
						moves.append([(letter + str(num)), m])
	return moves
	# moves ~= [['a2', 'a3'], ['b1', 'd3']]

# Random game without en passants or castles.
# Maybe make the board an object with last move
# attribute?
def watch_random_game():
	board = initialize_board()
	white = True
	ep = None
	while True:
		print(board)
		if is_mated(board, white, ep):
			winner = 'white' if white else 'black'
			print(winner + " wins!")
			return
		possible_moves = get_all_legal_moves(board, white, ep)
		if possible_moves == []:
			print("Stalemate!")
		random_move = random.choice(possible_moves)
		print(random_move)
		board = move(board, random_move[0], random_move[1])
		print_board(board)
		time.sleep(0.2)
		white = not white


def get_move_white(board, white):
	pass

def play_computer():
	pass

def play_opponent():
	pass


#############
## Testing ##
#############


def test_get_moves_pawn():
	# Test for white
	a = initialize_board()
	poss = get_possible_moves(a, 'e', 2)
	assert(set(poss) == set(['e3', 'e4']))
	a = move(a, 'e2', 'e3')
	poss = get_possible_moves(a, 'e', 3)
	assert(poss == ['e4'])
	a = move(a, 'e3', 'e5')
	a = move(a, 'd7', 'd5')
	poss = get_possible_moves(a, 'e', 5, 'd5')
	assert(set(poss) == set(['d6', 'e6']))

	# Test for black
	a = initialize_board()
	poss = get_possible_moves(a, 'e', 7)
	assert(set(poss) == set(['e6', 'e5']))
	a = move(a, 'e7', 'e5')
	poss = get_possible_moves(a, 'e', 5)
	assert(poss == ['e4'])
	a = move(a, 'e5', 'e4')
	a = move(a, 'd2', 'd4')
	a = move(a, 'f2', 'f4')
	poss = get_possible_moves(a, 'e', 4, 'd4')
	assert(set(poss) == set(['d3', 'e3']))
	poss = get_possible_moves(a, 'e', 4, 'f4')
	assert(set(poss) == set(['f3', 'e3']))
	
def test_get_moves_knight():
	a = initialize_board()
	poss = get_possible_moves(a, 'b', 1)
	assert(set(poss) == set(['a3', 'c3']))
	a = move(a, 'b1', 'c3')
	poss = get_possible_moves(a, 'c', 3)
	assert(set(poss) == set(['a4', 'b5', 'd5', 'e4', 'b1']))
	a = move(a, 'c3', 'd5')
	poss = get_possible_moves(a, 'd', 5)
	assert(set(poss) == set(['e7', 'f6', 'f4', 'e3', 'c3', 'b4', 'b6', 'c7']))

def test_get_moves_bishop():
	a = initialize_board()
	poss = get_possible_moves(a, 'f', 1)
	assert(poss == [])
	a = move(a, 'e2', 'e4')
	poss = get_possible_moves(a, 'f', 1)
	assert(set(poss) == set(['e2', 'd3', 'c4', 'b5', 'a6']))
	a = move(a, 'f1', 'c4')
	poss = get_possible_moves(a, 'c', 4)
	assert(set(poss) == set(['d5', 'e6', 'f7', 'd3', 'e2', 'f1', 'b3', 'b5', 'a6']))

def test_get_moves_rook():
	a = initialize_board()
	poss = get_possible_moves(a, 'a', 1)
	assert(poss == [])
	a = move(a, 'a2', 'a4')
	poss = get_possible_moves(a, 'a', 1)
	assert(set(poss) == set(['a2', 'a3']))
	a = move(a, 'a1', 'c4')
	poss = get_possible_moves(a, 'c', 4)
	assert(set(poss) == set(['c3', 'c5', 'c6', 'c7', 'b4', 'd4', 'e4', 'f4', 'g4', 'h4']))

def test_get_moves_queen():
	a = initialize_board()
	poss = get_possible_moves(a, 'd', 1)
	assert(poss == [])
	a = move(a, 'c2', 'c4')
	poss = get_possible_moves(a, 'd', 1)
	assert(set(poss) == set(['c2', 'b3', 'a4']))
	a = move(a, 'd1', 'c2')
	poss = get_possible_moves(a, 'c', 2)
	assert(set(poss) == set(['c3', 'd3', 'e4', 'f5', 'g6', 'h7', 'd1', 'b3', 'a4']))

def test_get_moves_king():
	a = initialize_board()
	poss = get_possible_moves(a, 'e', 1)
	assert(poss == [])
	a = move(a, 'e2', 'e4')
	poss = get_possible_moves(a, 'e', 1)
	assert(poss == ['e2'])
	a = move(a, 'e1', 'e3')
	poss = get_possible_moves(a, 'e', 3)
	assert(set(poss) == set(['d4', 'f4', 'f3', 'e2', 'd3']))
	a = move(a, 'e3', 'g5')
	a = move(a, 'g7', 'g6')
	poss = get_possible_moves(a, 'g', 5)
	assert(set(poss) == set(['f6', 'g6', 'h6', 'h5', 'h4', 'g4', 'f5', 'f4']))

# Test if mated with four move checkmate
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
	a = move(a, 'g1', 'f3')
	assert(in_check(a, True) == True)
	assert(is_mated(a, True) == False)
	assert(set(get_legal_moves(a, True, 'f', 3)) == set(['h4']))

# A move is considered legal if after doing it
# the player is no longer in check.
def test_get_legal_moves():
	a = empty_board()
	a['c'][4] = 'wK'
	a['d'][4] = 'wp'
	a['f'][5] = 'bR'
	a['h'][8] = 'bK'
	assert(get_legal_moves(a, True, 'd', 4) == ['d5'])
	a = move(a, 'f5', 'f4')
	assert(get_legal_moves(a, True, 'd', 4) == [])

	# Can't move a piece if still in check afterwards:
	a = move(a, 'd4', 'b4')
	assert(get_legal_moves(a, True, 'b', 4) == [])

def run_tests():
	test_get_moves_pawn()
	test_get_moves_knight()
	test_get_moves_bishop()
	test_get_moves_rook()
	test_get_moves_queen()
	test_get_moves_king()
	test_is_mated()
	test_get_legal_moves()
	print "All tests passed."


# run_tests()

watch_random_game()

# def fix_bug():
# 	board = {'a': {1: 'wR', 2: '', 3: 'wN', 4: 'wp', 5: 'bp', 6: '', 7: 'bR', 8: ''}, 'c': {1: '', 2: '', 3: '', 4: 'wB', 5: '', 6: '', 7: 'bp', 8: ''}, 'b': {1: '', 2: '', 3: '', 4: '', 5: 'bp', 6: '', 7: '', 8: 'bK'}, 'e': {1: '', 2: '', 3: '', 4: '', 5: '', 6: '', 7: '', 8: ''}, 'd': {1: '', 2: '', 3: '', 4: '', 5: 'wp', 6: '', 7: 'wp', 8: ''}, 'g': {1: '', 2: '', 3: '', 4: '', 5: 'bp', 6: '', 7: '', 8: ''}, 'f': {1: 'wK', 2: '', 3: 'wp', 4: 'bp', 5: '', 6: '', 7: '', 8: 'bQ'}, 'h': {1: '', 2: '', 3: '', 4: 'wp', 5: '', 6: 'bB', 7: '', 8: ''}}
# 	print_board(board)
# 	is_mated(board, False, None)

# fix_bug()
