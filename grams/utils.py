import random, string
from collections import Counter

TILE_COUNT = 144
TILE_MAP = {
    'A': 13,
    'B': 3,
    'C': 3,
    'D': 6,
    'E': 18,
    'F': 3,
    'G': 4,
    'H': 3,
    'I': 12,
    'J': 2,
    'K': 2,
    'L': 5,
    'M': 3,
    'N': 8,
    'O': 11,
    'P': 3,
    'Q': 2,
    'R': 9,
    'S': 6,
    'T': 9,
    'U': 6,
    'V': 3,
    'W': 3,
    'X': 2,
    'Y': 3,
    'Z': 2
}

def getTilesAsList():
    tiles = []
    for letter in TILE_MAP:
        tiles += [letter]*TILE_MAP[letter]
    random.shuffle(tiles)
    return tiles

# Generate a hash to share with other players
def generateUrlKey(stringLength=20):
    chars = string.ascii_uppercase + string.digits + string.ascii_lowercase
    return ''.join([random.choice(chars) for i in range(stringLength)])

# Depending on how many players there are, each player starts with a certain number of tiles
def getStartTileCount(numPlayers):
    if numPlayers in range(2, 5):
        return 21
    elif numPlayers in range(5,7):
        return 15
    elif numPlayers in range(7, 9):
        return 11

# Player's grid is serialized as strings concatenated with newlines
def deserializeGrid(gridString):
    grid = list(gridString.replace(" ", "").replace("\n", ""))

# Make sure the player's grid aligns with the old state to prevent cheating
def validatePeel(oldGrid, oldRack, newGrid):
    oldState = Counter(deserializeGrid(oldGrid) + list(oldRack))
    newState = Counter(deserializeGrid(newGrid))
    return oldState == newState

# Find all horizontal and vertical sequences
# TODO: compare against dictionary API
def validateBananas(grid):
    return true
