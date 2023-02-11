import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import RegularPolygon
import utils as u

BEEHIVE_IMAGE = "images/beehive.png"
MATRIX_IMAGE = "images/table.png"
SOLUTIONS_IMAGE = "images/solutions.png"
BLUE = "#73C3CF"
RED = "#EC4A49"
WHITE = "#FFFFFF"
BLACK = "#000000"
GREY = "#CCCCCC"


def print_matrix(mat: np.full, date: str, rows: int) -> None:
	# Changing the default  plot font-family for monospace
	plt.rcParams['font.family'] = 'monospace'

	fig, ax = plt.subplots()

	# Convert mat (np array) to list of list
	brut = mat.tolist()

	# Bold the first list of the list (the first row of the matrix)
	bolded = u.add_bold(brut[0])

	# Creating a new list, add the list bolded to that list and then add the other part of the matrix
	data = [bolded]

	for e in brut[1:]:
		data.append(e)

	# Making bold the first column (0) from row 1 to row ROW-1 and the last column from row 1 to row ROW-1
	for i in range(1, rows):
		data[i] = u.convert_position_bold(0, data[i])
		data[i] = u.convert_position_bold((len(data[0]) - 1), data[i])

	# Making the last row bold from column 1 to column column-2
	for i in range(1, len(data[0]) - 1):
		data[len(data) - 1] = u.convert_position_bold(i, data[len(data) - 1])

	ax.set_title("PARAULÒGIC " + date)

	# Disable or not show graph axis (x, y)
	ax.axis('tight')
	ax.axis('off')

	# Create table
	the_table = plt.table(cellText=data, loc='center')

	table_props = the_table.properties()
	table_cells = table_props

	# Hide table lines
	for cel in table_cells:
		for key, cell in the_table.get_celld().items():
			cell.set_linewidth(0)

	plt.savefig(MATRIX_IMAGE, dpi=600)


def create_matrix(letters: list, d_number: dict, d_individual: dict) -> np.full:
	letters = sorted(letters)
	columns = len(d_number.keys()) + 2

	rows = len(letters) + 2

	# Calculating total (m[ROWS-1][columns-1])
	total = sum(n for n in d_number.values())
	total = str(total)

	# Initializing np matrix with total value
	m = np.full((rows, columns), total)

	# Assigning fix positions
	m[0][0] = ''
	m[rows - 1][0] = "Σ"
	m[0][columns - 1] = "Σ"

	for i in range(1, len(letters) + 1):
		# Writing letters in 0 column
		m[i][0] = letters[i - 1]
		letter = m[i][0]

		# Checking if a letter has words of all lengths appearing in the game
		equal = u.compare_two_arrays(list(d_number.keys()), list(d_individual[letter].keys()), True)
		different = u.compare_two_arrays(list(d_number.keys()), list(d_individual[letter].keys()), False)

		# '0' in the position if the letter has no words with its length
		for dif in different:
			pos = u.get_position(dif, list(d_number.keys())) + 1
			m[i][pos] = '0'

		suma = 0

		for eq in equal:
			pos = u.get_position(eq, list(d_number.keys())) + 1
			m[i][pos] = d_individual[letter][eq]
			suma = suma + int(d_individual[letter][eq])

		m[i][columns - 1] = str(suma)

	for i in range(1, len(d_number.keys()) + 1):
		# Writing first row values (numbers)
		m[0][i] = list(d_number.keys())[i - 1]

		# Writing last row numbers (adders)
		m[rows - 1][i] = list(d_number.values())[i - 1]

	return m


def create_beehive(letters: list, date: str) -> None:
	colors = get_colors(letters)
	labels = get_labels(letters)

	coord = [
		[0, 0, 0], [1.25, 0, 0], [-1.25, 0, 0], [-0.625, -0.8660254, 1], [0.625, -0.8660254, 1],
		[-0.625, 0.8660254, -1], [0.625, 0.8660254, -1]
	]

	text_colors = [[WHITE], [BLACK], [BLACK], [BLACK], [BLACK], [BLACK], [BLACK]]

	# Horizontal cartesian coords
	hcoord = [c[0] for c in coord]

	# Vertical cartersian coords
	vcoord = [2. * np.sin(np.radians(60)) * (c[1] - c[2]) / 3. for c in coord]

	plt.rcParams['font.family'] = 'monospace'

	fig, ax = plt.subplots(1)
	ax.set_aspect('equal')
	ax.set_title("PARAULÒGIC " + date)
	ax.axis('off')

	# Add some coloured hexagons
	for x, y, c, tc, l in zip(hcoord, vcoord, colors, text_colors, labels):
		color = c[0].lower()  # matplotlib understands lower case words for colours
		t_color = tc[0].lower()
		hexagon = RegularPolygon((x, y), numVertices=6, radius=2. / 3., facecolor=color, alpha=1)
		ax.add_patch(hexagon)
		# Also add a text label
		ax.text(x, y + 0, l[0], color=t_color, ha='center', va='center', size=20, family='sans-serif')

	# Also add scatter points in hexagon centres
	ax.scatter(hcoord, vcoord, c=[c[0].lower() for c in colors], alpha=0)

	plt.savefig(BEEHIVE_IMAGE, dpi=600)


def get_colors(letters: list) -> list:
	found = False

	if len(letters) == 6:
		found = True

	if found:
		colors = [[RED], [BLUE], [BLUE], [BLUE], [BLUE], [BLUE], [GREY]]
	else:
		colors = [[RED], [BLUE], [BLUE], [BLUE], [BLUE], [BLUE], [BLUE]]

	return colors


def get_labels(letters: list) -> list:
	found = False

	center = letters[-1].upper()
	l0 = letters[0].upper()
	l1 = letters[1].upper()
	l2 = letters[2].upper()
	l3 = letters[3].upper()
	l4 = letters[4].upper()
	l5 = letters[5].upper()

	if len(letters) == 6:
		found = True

	if found:
		labels = [center, l0, l1, l2, l3, l4, ' ']
	else:
		labels = [center, l0, l1, l2, l3, l4, l5]

	return labels


def create_draw(letters: list) -> str:
	if len(list(letters)) == 7:
		center = letters[-1]
		l0 = letters[0]
		l1 = letters[1]
		l2 = letters[2]
		l3 = letters[3]
		l4 = letters[4]
		l5 = letters[5]

		center = u.EMOJI_LETTERS[u.UPPER_LETTERS.index(center.upper())]

		message = (
			f"{l0.upper()}, {l1.upper()}, {l2.upper()}, {center}, {l3.upper()}, {l4.upper()}, {l5.upper()}\n\n"
		)
	else:
		center = letters[-1]
		l0 = letters[0]
		l1 = letters[1]
		l2 = letters[2]
		l3 = letters[3]
		l4 = letters[4]

		center = u.EMOJI_LETTERS[u.UPPER_LETTERS.index(center.upper())]

		message = (
			f"{l0.upper()}, {l1.upper()}, {l2.upper()}, {center}, {l3.upper()}, {l4.upper()}\n\n"
		)

	return message


def create_image_from_string(string: str, date: str) -> None:
	plt.rcParams['font.family'] = 'monospace'
	plt.figure()

	plt.title("PARAULÒGIC " + date)

	t = string
	plt.text(-0.135, 0.5, t, ma='center', va='center', wrap=True)
	plt.axis('off')
	plt.savefig(SOLUTIONS_IMAGE, dpi=600)
