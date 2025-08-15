# GIF to ASCII Converter

A Python tool that converts GIF images to ASCII art with various output options.

## Features

- Convert GIF images to ASCII art
- Support for animated GIFs (multiple frames)
- Adjustable output scale and speed
- Color options (original colors or custom fill colors)
- Multiple output formats (GIF, ASCII text)
- Brightness inversion option
- Customizable font size and background colors

## Installation

1. Make sure you have Python 3.7+ installed
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Basic Usage
```bash
python new.py input.gif
```

### Advanced Options
```bash
# Scale down output (0.5x0.5)
python new.py input.gif --scale 0.5 0.5

# Use original colors
python new.py input.gif --color

# Invert brightness
python new.py input.gif --inverse

# Output as ASCII text instead of GIF
python new.py input.gif --ascii --out output.txt

# Custom font size
python new.py input.gif --size 16

# Custom colors
python new.py input.gif --backcolor 0 0 0 --fillcolor 255 255 0

# Adjust animation speed
python new.py input.gif --speed 2.0
```

### Command Line Arguments

- `input_file`: Input GIF file (required)
- `--scale x y`: Output scale (0.0-1.0, default: 1.0 1.0)
- `--speed`: Animation speed multiplier (default: 1.0)
- `--inverse`: Invert brightness
- `--font`: Font file to use (default: font.ttf)
- `--out`: Output file name (default: out.gif)
- `--size`: Font point size (default: 12)
- `--ascii`: Output ASCII text instead of GIF
- `--transparent`: Use transparent background
- `--backcolor r g b`: Background color RGB (default: 0 0 0)
- `--fillcolor r g b`: Fill color RGB (default: 255 255 255)
- `--color`: Use original image colors

## Examples

### Convert with custom scale
```bash
python new.py animation.gif --scale 0.3 0.3 --out small_ascii.gif
```

### Create ASCII text output
```bash
python new.py logo.gif --ascii --out logo.txt
```

### Inverted colors with custom fill
```bash
python new.py image.gif --inverse --fillcolor 0 255 0 --out inverted.gif
```

## Output Formats

1. **GIF**: Creates a new GIF with ASCII characters (default)
2. **ASCII Text**: Plain text file with ASCII art frames

## Dependencies

- Pillow (PIL) - Image processing
- NumPy - Numerical operations
- argparse - Command line argument parsing

## Notes

- The tool automatically detects animated GIFs and processes all frames
- Frame delays are preserved in the output
- For best results, use monospaced fonts
- Scale values between 0.1 and 1.0 work best for most images 