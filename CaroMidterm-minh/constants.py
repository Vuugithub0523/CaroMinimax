# ---------
# CONSTANTS
# ---------

# --- PIXELS ---

WIDTH = 600
HEIGHT = 600

ROWS = 10  # 10x10 board
COLS = 10  # 10x10 board
SQSIZE = WIDTH // COLS  # Square size for 10x10 (60px per square)

LINE_WIDTH = 7  # Thinner lines for smaller squares
CIRC_WIDTH = 5  # Thinner circles
CROSS_WIDTH = 8  # Thinner crosses

RADIUS = SQSIZE // 3  # Radius for circles

OFFSET = 15  # Smaller offset for better visibility in smaller squares

# --- COLORS ---

BG_COLOR = (28, 170, 156)
LINE_COLOR = (23, 145, 135)
CIRC_COLOR = (239, 231, 200)  # Light cream color for O
CROSS_COLOR = (66, 66, 66)    # Dark gray for X