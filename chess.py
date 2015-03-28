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
	if white:
		if p[0] == 'w':
			return False
		else:
			if p[1] == 'K':
				raise Exception("White allowed to take black King.")
			else:
				return False
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

def get_legal_piece_moves(board, sq_let, sq_num):

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
					moveable_squares.append(sq_let + str(sq_num))	
				break
			else:
				moveable_squares.append(sq_let)

		# iterate up. Constant letter index.
		it_u = range(sq_num + 1, 9)
		for num in it_u:
			if board[sq_let][num]:
				if can_take_on(board, sq_let, num, white_turn):
					moveable_squares.append(sq_let + str(sq_num))	
				break
			else:
				moveable_squares.append(sq_let)

		# iterate left. Constant number index.
		it_l = (letter.split(sq_let))[0][::-1]
		for ch in it_l:
			if board[ch][sq_num]:
				if can_take_on(board, ch, sq_num, white_turn):
					moveable_squares.append(ch + str(sq_num))	
				break
			else:
				moveable_squares.append(ch + str(sq_num))

		# iterate right. Constant number index.
		it_r = (letter.split(sq_let))[0]
		for ch in it_r:
			if board[ch][sq_num]:
				if can_take_on(board, ch, sq_num, white_turn):
					moveable_squares.append(ch + str(sq_num))	
				break
			else:
				moveable_squares.append(ch + str(sq_num))

	elif p == 'N':
		pass
	elif p == 'B':
		pass
	elif p == 'Q':
		pass
	elif p == 'K':
		pass
	elif p == 'p':
		pass
	else:
		raise Exception("This square is empty.")


def black_is_mated(board, r_l):
	pass

print_board(empty_board())

