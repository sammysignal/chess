import sys

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
	
	royal_loc = {'wQ':'d1', 'wK':'e1', 'bQ':'d8', 'bK':'e8'}

	return board, royal_loc

def square_is_black(let, num):
	return (((ord(let) + num) % 2) == 1)

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
			if p[1] == 'K':
				raise Exception("White allowed to take black King.")
			else:
				return True
	else:
		if p[0] == 'b':
			return False
		else:
			if p[1] == 'K':
				raise Exception("Black allowed to take white King.")
			else:
				return True
# Where a given piece could move if there were
# no other pieces on the board
#   def get_theoretical_piece_moves(board, sq_num, sq_let):

# Gets possible moves, disregarding check. requires a prev
# (previous move location) to check for en passant.

def get_possible_moves(board, sq_let, sq_num, prev, prev_prev):
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
		pass
	elif p == 'p':
		if white_turn:
			if (sq_num + 1) in range(1, 9):
				ahead = board[sq_let][sq_num + 1]
				if not ahead:
					moveable_squares.append(sq_let + str(sq_num))

	else:
		raise Exception("This square is empty.")


def is_mated(board, r_l, white):
	pass

def in_check(board, white):
	pass

def play_computer():
	pass

def play_opponent():
	pass


a, b = initialize_board()

a['e'][2] = ""
a['e'][4] = 'wp'
print_board(a)

print get_possible_moves(a, 'b', 1, "", "")



