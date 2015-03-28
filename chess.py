import sys

letters = "abcdefgh"
pieces = ['R', 'N', 'B', 'Q', 'K', 'B', 'N', 'R']

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


def print_board(board):
	buf = "\n"
	for i in range(8):
		buf = buf + '_'
	buf = buf + '\n'
	for i in range(8, 0, -1):
		for let in letters:
			cell = board[let][i]
			if not cell:
				buf = buf + '|  '
			else:
				buf = buf + '|' + board[let][i]
		buf = buf + '|\n'

	for i in range(8):
		buf = buf + '_'
	buf = buf + '\n'
	
	sys.stdout.write(buf)

def get_legal_piece_moves(board, sq_num, sq_let):
	pass


print_board(initialize_board())

