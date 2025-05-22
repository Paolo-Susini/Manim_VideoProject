Here's a README.md file for your code with  prefixed to each line as requested:

# Quizzone Animation - ManimGL Project

## Overview
This project creates an interactive quiz animation using ManimGL, featuring 3D trajectories, image animations, and timed questions.

## Requirements
- Python 3.7+
- manimGL (https://github.com/3b1b/manim)
- Additional dependencies: numpy, opencv-python, Pillow

## Installation
1. Clone the manimGL repository:
   ```bash
   git clone https://github.com/3b1b/manim.git
   ```
2. Install required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## File Structure
- `Quizzone.py`: Main animation script
- `utils.py`: Helper functions (must be in same directory)
- `Guests/`: Directory containing guest question data (.pkl files)
- `Images/`: Contains all image assets

## Usage
Run the animation with:
```bash
manimgl Quizzone.py Quizzone
```

## Key Features
- 3D spiral trajectories with custom axes
- Randomized guest selection from .pkl files
- Image resizing and animation
- Interactive quiz format with timed questions
- Special effects for correct answers

## Customization
You can modify:
- `config.pixel_height/width`: Output resolution
- `config.frame_height/width`: Scene dimensions
- `time_s` and `time`: Animation durations
- Guest questions in the `Guests/` directory

## Notes
- Ensure all image paths are correct for your system
- The script uses current time for random seeding
- Requires properly formatted .pkl files for guest data

## Example Command
```bash
manimgl Quizzone.py Quizzone -w --hd
```
(Renders at 1280x720 resolution)