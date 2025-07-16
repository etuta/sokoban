ngs.py`

## Assets
- **Graphics:** `graphics/skins/standard/` (BMP and PNG files)
- **Sounds:** `sounds/tada.wav` (win notification)
- **Levelsets:** `levelsets/` (many levels included)

## Credits
- Levelsets by David W. Skinner (http://users.bentonrea.com/~sasquatch/)
- Thanks to the Python, Pygame, and SDL communities
- Special thanks to all players and testers!
- 
# Sokoban

This is a Python implementation of the classic Sokoban game, originally created in 1981 by Hiroyuki Imabayashi. In Sokoban, you push boxes around a warehouse, trying to get them to their storage locations (marked with X's). You can only push boxes (not pull), and the puzzle is solved when all boxes are on storage locations.

## Features
- Classic Sokoban gameplay with intuitive controls
- Multiple levelsets included: "Microban I-III" (easier) and "Sasquatch I-VIII" (harder)
- Save and load your progress per levelset
- Undo, reset, and cheat options (if enabled in settings)
- Step counter and level display
- Sound support (toggle in settings)
- Customizable graphics via skins (default: "standard")
- Menu navigation and in-game controls via keyboard

## Getting Started

1. **Install Python 3 and pygame**
   - Download Python: https://www.python.org/downloads/
   - Install pygame: `pip install pygame`

2. **Clone the repository**
   ```sh
   git clone https://github.com/etuta/sokoban.git
   cd sokoban
   ```

3. **Run the game**
   ```sh
   python3 startme.py
   ```

## Controls
- Arrow keys: Move player
- `u`: Undo move
- `s`: Save level progress
- `l`: Load saved progress
- `r`: Reset level
- `ESC`: Quit game
- `c`: Cheat (skip level, if enabled in settings)

## Configuration
- All settings are in `settings.py` (resolution, fullscreen, sound, skin, framerate, etc.)
- No command-line arguments; all configuration is via `setti
