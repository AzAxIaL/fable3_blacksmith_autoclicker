# Fable 3 Blacksmith Auto-Clicker  
  
A python script that uses OpenCV to play the blacksmith game in Fable 3.  



The game requires you to press a key (1 or 2) depending on the colored square in a sequence.
If you succeed in hitting all the squares in a sequence, the cash multiplier increases (up to 10), at which point, the speed increases.

## Requirements
#### Code requirements
- Python 3.6 or higher
- OpenCV 4.51 (recommend opencv-contrib-python==4.5.1.48)
- Numpy
- PIL

#### Game requirements
- Fable 3 running at 1920x1080 (I haven't tested it on other resolutions...yet)
- If using an NVIDIA card, remove the vsync 30 fps lock by following [this guide](https://steamcommunity.com/sharedfiles/filedetails/?id=196292201) to run at 60+ fps (this improves the screen reading).
- Maximum graphics settings, if possible (again, to improve screen reading).

## Instructions

 1. Clone this repo.
 2. Run Fable 3 and find a blacksmith game (easiest is in Bowerstone Market).
 3. Remember to switch to keyboard controls, not controller, before starting the game, 
 4. Tab out and run the script
 5. You will have 20 seconds to start the game before the script auto-terminates (Adjust the `limit` value)
 6. Sit back and watch the money roll in

## Known Issues

The script can achieve a 90% accuracy rate in terms of continuation; some blocks in a sequence may be missed. Tweaking the `theshold` value will adjust the sensitivity.

[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)