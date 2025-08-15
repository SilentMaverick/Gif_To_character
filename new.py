#!/usr/bin/env python3
"""
GIF to ASCII Converter
Converts GIF images to ASCII art with various output options
"""

import argparse
import sys
from PIL import Image, ImageDraw, ImageFont
import numpy as np
from typing import List, Tuple, Optional
import os

# ASCII character table for brightness mapping
ASCII_TABLE = " .:-=+*#%@"
# Alternative tables:
# " .-*:o+8&#@"
# " .'`^\",:;Il!i><~+_-?][}{1)(|\\/tfjrxnuvczXYUJCLQ0OZmwqpdbkhao*#MW&8%B@$"

def convert_to_ascii(input_file: str, out_scale: Tuple[float, float], 
                     use_color: bool = False, fill_color: Tuple[int, int, int] = (255, 255, 255),
                     speed: float = 1.0, inverse: bool = False) -> Tuple[List[List[List[Tuple[str, Tuple[int, int, int]]]]], List[int]]:
    """
    Convert GIF to ASCII representation
    Returns: (pixels, delays)
    """
    try:
        # Open the GIF file
        with Image.open(input_file) as img:
            # Get all frames
            frames = []
            delays = []
            
            try:
                while True:
                    # Convert frame to RGB if needed
                    if img.mode != 'RGB':
                        frame = img.convert('RGB')
                    else:
                        frame = img.copy()
                    
                    # Resize frame according to scale
                    new_size = (int(img.width * out_scale[0]), int(img.height * out_scale[1]))
                    frame = frame.resize(new_size, Image.Resampling.LANCZOS)
                    
                    frames.append(frame)
                    
                    # Get frame delay (convert from centiseconds to milliseconds)
                    delay = img.info.get('duration', 100)  # Default 100ms if no delay info
                    delays.append(int(delay / speed))
                    
                    img.seek(img.tell() + 1)
            except EOFError:
                pass  # End of frames
            
            if not frames:
                print(f"Failed to read image file {input_file}")
                return [], []
            
            print(f"Loaded {len(frames)} frames")
            
            # Process each frame
            out_pixels = []
            for frame_idx, frame in enumerate(frames):
                frame_pixels = []
                frame_array = np.array(frame)
                
                for x in range(frame.width):
                    column = []
                    for y in range(frame.height):
                        pixel = frame_array[y, x]
                        
                        # Check if pixel is transparent/black
                        if np.all(pixel == 0):
                            char = ' '
                            color = fill_color
                        else:
                            # Calculate brightness (average of RGB)
                            brightness = np.mean(pixel[:3])
                            
                            if inverse:
                                brightness = 255 - brightness
                            
                            # Map brightness to ASCII character
                            char_idx = int((brightness / 256.0) * len(ASCII_TABLE))
                            char_idx = min(char_idx, len(ASCII_TABLE) - 1)
                            char = ASCII_TABLE[char_idx]
                            
                            if use_color:
                                color = tuple(pixel[:3])
                            else:
                                color = fill_color
                        
                        column.append((char, color))
                    frame_pixels.append(column)
                
                out_pixels.append(frame_pixels)
            
            return out_pixels, delays
            
    except Exception as e:
        print(f"Error processing {input_file}: {e}")
        return [], []

def generate_gif(font_file: str, chars: List[List[List[Tuple[str, Tuple[int, int, int]]]]], 
                out_file: str, point_size: int, delays: List[int], 
                back_color: Tuple[int, int, int]) -> bool:
    """
    Generate GIF from ASCII characters
    """
    try:
        # Load font
        try:
            font = ImageFont.truetype(font_file, point_size)
        except:
            # Fallback to default font
            font = ImageFont.load_default()
        
        # Calculate character size
        char_width, char_height = font.getbbox('#')[2:4]
        
        if not chars or not chars[0] or not chars[0][0]:
            print("No valid character data")
            return False
        
        # Get dimensions
        width = len(chars[0])
        height = len(chars[0][0])
        
        # Create output images
        out_images = []
        
        for frame_idx, frame_chars in enumerate(chars):
            # Create image for this frame
            img = Image.new('RGB', (char_width * width, char_height * height), back_color)
            draw = ImageDraw.Draw(img)
            
            # Draw each character
            for x in range(width):
                for y in range(height):
                    if x < len(frame_chars) and y < len(frame_chars[x]):
                        char, color = frame_chars[x][y]
                        position = (char_width * x, char_height * y)
                        draw.text(position, char, fill=color, font=font)
            
            out_images.append(img)
        
        # Save as GIF
        if len(out_images) > 1:
            out_images[0].save(
                out_file,
                save_all=True,
                append_images=out_images[1:],
                duration=delays,
                loop=0,
                optimize=False
            )
        else:
            out_images[0].save(out_file)
        
        print(f"Writing {len(out_images)} images to {out_file}")
        return True
        
    except Exception as e:
        print(f"Error generating GIF: {e}")
        return False

def generate_ascii_animation(out_file: str, out_pixels: List[List[List[Tuple[str, Tuple[int, int, int]]]]], 
                            delays: List[int]) -> bool:
    """
    Generate ASCII animation file
    """
    try:
        with open(out_file, 'w') as f:
            for frame_idx, frame in enumerate(out_pixels):
                f.write(f"Frame {frame_idx + 1} (Delay: {delays[frame_idx]}ms):\n")
                f.write("-" * 50 + "\n")
                
                # Write frame content
                if frame and frame[0]:
                    for y in range(len(frame[0])):
                        for x in range(len(frame)):
                            if x < len(frame) and y < len(frame[x]):
                                char, _ = frame[x][y]
                                f.write(char)
                        f.write('\n')
                
                f.write('\n')
        
        print(f"ASCII animation saved to {out_file}")
        return True
        
    except Exception as e:
        print(f"Error generating ASCII animation: {e}")
        return False

def write_ascii(out_file: str, ascii_data: List[List[Tuple[str, Tuple[int, int, int]]]]) -> bool:
    """
    Write single frame ASCII to file
    """
    try:
        with open(out_file, 'w') as f:
            if ascii_data and ascii_data[0]:
                for y in range(len(ascii_data[0])):
                    for x in range(len(ascii_data)):
                        if x < len(ascii_data) and y < len(ascii_data[x]):
                            char, _ = ascii_data[x][y]
                            f.write(char)
                    f.write('\n')
        
        print(f"ASCII output saved to {out_file}")
        return True
        
    except Exception as e:
        print(f"Error writing ASCII: {e}")
        return False

def handle_arguments():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(
        description="Convert GIF images to ASCII art",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python new.py input.gif
  python new.py input.gif --scale 0.5 0.5 --out output.gif
  python new.py input.gif --size 16 --color --inverse
        """
    )
    
    parser.add_argument('input_file', help='Input GIF file')
    parser.add_argument('--scale', nargs=2, type=float, default=[1.0, 1.0],
                       help='Output scale x y (range 0.0-1.0, default: 1.0 1.0)')
    parser.add_argument('--speed', type=float, default=1.0,
                       help='Animation speed multiplier (default: 1.0)')
    parser.add_argument('--inverse', action='store_true',
                       help='Invert brightness')
    parser.add_argument('--font', default='font.ttf',
                       help='Font file to use (default: font.ttf)')
    parser.add_argument('--out', default='out.gif',
                       help='Output file name (default: out.gif)')
    parser.add_argument('--size', type=int, default=12,
                       help='Font point size (default: 12)')
    parser.add_argument('--ascii', action='store_true',
                       help='Output ASCII text instead of GIF')
    parser.add_argument('--transparent', action='store_true',
                       help='Use transparent background')
    parser.add_argument('--backcolor', nargs=3, type=int, default=[0, 0, 0],
                       help='Background color R G B (default: 0 0 0)')
    parser.add_argument('--fillcolor', nargs=3, type=int, default=[255, 255, 255],
                       help='Fill color R G B (default: 255 255 255)')
    parser.add_argument('--color', action='store_true',
                       help='Use original image colors')
    
    args = parser.parse_args()
    
    # Validate scale
    if not (0.0 < args.scale[0] <= 1.0 and 0.0 < args.scale[1] <= 1.0):
        print("Scale must be between 0.0 and 1.0")
        sys.exit(1)
    
    return args

def main():
    """Main function"""
    args = handle_arguments()
    
    # Check if input file exists
    if not os.path.exists(args.input_file):
        print(f"Input file {args.input_file} not found")
        sys.exit(1)
    
    # Set colors
    back_color = tuple(args.backcolor)
    fill_color = tuple(args.fillcolor)
    
    if args.transparent:
        back_color = (0, 0, 0, 0)  # Transparent
    
    print("Converting...")
    
    # Convert to ASCII
    ascii_data, delays = convert_to_ascii(
        args.input_file, 
        tuple(args.scale), 
        args.color, 
        fill_color, 
        args.speed, 
        args.inverse
    )
    
    if not ascii_data:
        print("Conversion failed")
        sys.exit(1)
    
    print("Generating output...")
    
    # Generate output
    if args.ascii:
        # Output ASCII text
        if len(ascii_data) == 1:
            # Single frame
            success = write_ascii(args.out, ascii_data[0])
        else:
            # Multiple frames
            success = generate_ascii_animation(args.out, ascii_data, delays)
    else:
        # Output GIF
        success = generate_gif(args.font, ascii_data, args.out, args.size, delays, back_color)
    
    if success:
        print("Done!")
    else:
        print("Output generation failed")
        sys.exit(1)

if __name__ == "__main__":
    main()
