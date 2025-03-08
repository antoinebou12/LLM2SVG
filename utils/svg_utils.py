import random
import math
from typing import Dict, List, Tuple, Union, Optional

def generate_color_palette(base_color: str = None, count: int = 5) -> List[str]:
    """Generate a harmonious color palette."""
    if base_color is None:
        # Generate a random base color if none provided
        hue = random.randint(0, 360)
        base_color = f"hsl({hue}, 70%, 50%)"
    
    # For now, just return some random colors
    palette = []
    for i in range(count):
        # Generate colors with varying hue
        hue = (random.randint(0, 360) + i * 60) % 360
        saturation = random.randint(60, 100)
        lightness = random.randint(40, 70)
        palette.append(f"#{random.randint(0, 255):02x}{random.randint(0, 255):02x}{random.randint(0, 255):02x}")
    
    return palette

def hex_to_rgb(hex_color: str) -> Tuple[int, int, int]:
    """Convert hex color to RGB tuple."""
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

def rgb_to_hex(rgb: Tuple[int, int, int]) -> str:
    """Convert RGB tuple to hex color."""
    return f"#{rgb[0]:02x}{rgb[1]:02x}{rgb[2]:02x}"

def create_svg_rect(x: float, y: float, width: float, height: float, 
                   fill: str, stroke: str = None, stroke_width: float = None,
                   opacity: float = None, rx: float = None, ry: float = None) -> str:
    """Create an SVG rect element with the given parameters."""
    attributes = []
    attributes.append(f'x="{x}"')
    attributes.append(f'y="{y}"')
    attributes.append(f'width="{width}"')
    attributes.append(f'height="{height}"')
    attributes.append(f'fill="{fill}"')
    
    if stroke is not None:
        attributes.append(f'stroke="{stroke}"')
    if stroke_width is not None:
        attributes.append(f'stroke-width="{stroke_width}"')
    if opacity is not None:
        attributes.append(f'opacity="{opacity}"')
    if rx is not None:
        attributes.append(f'rx="{rx}"')
    if ry is not None:
        attributes.append(f'ry="{ry}"')
    
    return f'  <rect {" ".join(attributes)} />\n'

def create_svg_circle(cx: float, cy: float, r: float, 
                     fill: str, stroke: str = None, stroke_width: float = None,
                     opacity: float = None) -> str:
    """Create an SVG circle element with the given parameters."""
    attributes = []
    attributes.append(f'cx="{cx}"')
    attributes.append(f'cy="{cy}"')
    attributes.append(f'r="{r}"')
    attributes.append(f'fill="{fill}"')
    
    if stroke is not None:
        attributes.append(f'stroke="{stroke}"')
    if stroke_width is not None:
        attributes.append(f'stroke-width="{stroke_width}"')
    if opacity is not None:
        attributes.append(f'opacity="{opacity}"')
    
    return f'  <circle {" ".join(attributes)} />\n'

def create_svg_ellipse(cx: float, cy: float, rx: float, ry: float,
                      fill: str, stroke: str = None, stroke_width: float = None,
                      opacity: float = None) -> str:
    """Create an SVG ellipse element with the given parameters."""
    attributes = []
    attributes.append(f'cx="{cx}"')
    attributes.append(f'cy="{cy}"')
    attributes.append(f'rx="{rx}"')
    attributes.append(f'ry="{ry}"')
    attributes.append(f'fill="{fill}"')
    
    if stroke is not None:
        attributes.append(f'stroke="{stroke}"')
    if stroke_width is not None:
        attributes.append(f'stroke-width="{stroke_width}"')
    if opacity is not None:
        attributes.append(f'opacity="{opacity}"')
    
    return f'  <ellipse {" ".join(attributes)} />\n'

def create_svg_path(d: str, fill: str = "none", stroke: str = None, 
                   stroke_width: float = None, opacity: float = None) -> str:
    """Create an SVG path element with the given parameters."""
    attributes = []
    attributes.append(f'd="{d}"')
    attributes.append(f'fill="{fill}"')
    
    if stroke is not None:
        attributes.append(f'stroke="{stroke}"')
    if stroke_width is not None:
        attributes.append(f'stroke-width="{stroke_width}"')
    if opacity is not None:
        attributes.append(f'opacity="{opacity}"')
    
    return f'  <path {" ".join(attributes)} />\n'

def create_svg_polygon(points: List[Tuple[float, float]], fill: str, 
                      stroke: str = None, stroke_width: float = None,
                      opacity: float = None) -> str:
    """Create an SVG polygon element with the given parameters."""
    points_str = " ".join(f"{x},{y}" for x, y in points)
    attributes = []
    attributes.append(f'points="{points_str}"')
    attributes.append(f'fill="{fill}"')
    
    if stroke is not None:
        attributes.append(f'stroke="{stroke}"')
    if stroke_width is not None:
        attributes.append(f'stroke-width="{stroke_width}"')
    if opacity is not None:
        attributes.append(f'opacity="{opacity}"')
    
    return f'  <polygon {" ".join(attributes)} />\n'

def create_svg_line(x1: float, y1: float, x2: float, y2: float,
                   stroke: str, stroke_width: float = 1,
                   opacity: float = None) -> str:
    """Create an SVG line element with the given parameters."""
    attributes = []
    attributes.append(f'x1="{x1}"')
    attributes.append(f'y1="{y1}"')
    attributes.append(f'x2="{x2}"')
    attributes.append(f'y2="{y2}"')
    attributes.append(f'stroke="{stroke}"')
    attributes.append(f'stroke-width="{stroke_width}"')
    
    if opacity is not None:
        attributes.append(f'opacity="{opacity}"')
    
    return f'  <line {" ".join(attributes)} />\n'

def create_svg_group(elements: List[str], transform: str = None, opacity: float = None) -> str:
    """Create an SVG group containing the given elements."""
    attributes = []
    
    if transform is not None:
        attributes.append(f'transform="{transform}"')
    if opacity is not None:
        attributes.append(f'opacity="{opacity}"')
    
    if attributes:
        group_start = f'  <g {" ".join(attributes)}>\n'
    else:
        group_start = '  <g>\n'
    
    group_content = ''.join(elements)
    group_end = '  </g>\n'
    
    return group_start + group_content + group_end

def validate_svg_size(svg: str, max_size: int = 10000) -> bool:
    """Validate that the SVG size is within limits."""
    return len(svg.encode('utf-8')) <= max_size

def optimize_svg(svg: str) -> str:
    """Perform basic optimizations to reduce SVG size."""
    # Remove unnecessary whitespace and line breaks
    optimized = svg.replace('\n', '').replace('  ', '')
    
    # Round decimal values to reduce size
    # This is a simple regex-based approach that could be improved
    import re
    pattern = r'(\d+\.\d{3,})'
    
    def round_match(match):
        num = float(match.group(1))
        return f"{num:.2f}"
    
    optimized = re.sub(pattern, round_match, optimized)
    
    return optimized

def svg_to_png(svg_content: str, output_path: Optional[str] = None, 
              width: Optional[int] = None, height: Optional[int] = None) -> Optional[bytes]:
    """
    Convert SVG content to PNG using cairosvg.
    
    Args:
        svg_content: The SVG content as a string
        output_path: Optional path to save the PNG file
        width: Optional width for the PNG
        height: Optional height for the PNG
        
    Returns:
        Bytes of PNG data if output_path is None, otherwise None
    """
    try:
        import cairosvg
        
        # Set conversion options
        kwargs = {}
        if width:
            kwargs['width'] = width
        if height:
            kwargs['height'] = height
            
        # Convert SVG to PNG
        if output_path:
            cairosvg.svg2png(bytestring=svg_content.encode('utf-8'), 
                            write_to=output_path, **kwargs)
            return None
        else:
            png_data = cairosvg.svg2png(bytestring=svg_content.encode('utf-8'), **kwargs)
            return png_data
    except ImportError:
        raise ImportError("cairosvg is required for SVG to PNG conversion. Install it with 'pip install cairosvg'.")


def generate_shapes(extracted: Dict[str, List[str]], width: int, height: int, color_map: Dict[str, str]) -> List[str]:
    """Generate SVG elements for shapes."""
    elements = []
    colors = [color_map.get(color.lower(), '#ff0000') for color in extracted['colors']] if extracted['colors'] else generate_color_palette()
    
    # Determine which shapes to create
    if 'circle' in extracted['shapes']:
        cx, cy = width // 2, height // 2
        radius = min(width, height) // 3
        elements.append(create_svg_circle(cx, cy, radius, 
                                         colors[0] if colors else '#ff0000', 
                                         stroke='#000000', 
                                         stroke_width=2))
    
    if 'square' in extracted['shapes']:
        size = min(width, height) // 2
        x = (width - size) // 2
        y = (height - size) // 2
        elements.append(create_svg_rect(x, y, size, size, 
                                       colors[0] if colors else '#00ff00', 
                                       stroke='#000000', 
                                       stroke_width=2))
    
    if 'triangle' in extracted['shapes']:
        side = min(width, height) // 2
        cx, cy = width // 2, height // 2
        points = [
            (cx, cy - side // 2),
            (cx - side // 2, cy + side // 2),
            (cx + side // 2, cy + side // 2)
        ]
        elements.append(create_svg_polygon(points, 
                                         colors[0] if colors else '#0000ff', 
                                         stroke='#000000', 
                                         stroke_width=2))
    
    if 'rectangle' in extracted['shapes']:
        rect_width = width // 2
        rect_height = height // 3
        x = (width - rect_width) // 2
        y = (height - rect_height) // 2
        elements.append(create_svg_rect(x, y, rect_width, rect_height, 
                                       colors[0] if colors else '#ffff00', 
                                       stroke='#000000', 
                                       stroke_width=2))
    
    if 'star' in extracted['shapes']:
        # Create a 5-pointed star
        cx, cy = width // 2, height // 2
        outer_radius = min(width, height) // 3
        inner_radius = outer_radius // 2
        points = []
        for i in range(10):
            radius = outer_radius if i % 2 == 0 else inner_radius
            angle = math.pi * i / 5
            x = cx + radius * math.sin(angle)
            y = cy - radius * math.cos(angle)
            points.append((x, y))
        elements.append(create_svg_polygon(points, 
                                         colors[0] if colors else '#ff00ff', 
                                         stroke='#000000', 
                                         stroke_width=2))
    
    # If no specific shapes were mentioned, create a random shape
    if not elements:
        shape_type = random.choice(['circle', 'square', 'triangle', 'rectangle'])
        if shape_type == 'circle':
            cx, cy = width // 2, height // 2
            radius = min(width, height) // 3
            elements.append(create_svg_circle(cx, cy, radius, 
                                            colors[0] if colors else '#ff0000', 
                                            stroke='#000000', 
                                            stroke_width=2))
        elif shape_type == 'square':
            size = min(width, height) // 2
            x = (width - size) // 2
            y = (height - size) // 2
            elements.append(create_svg_rect(x, y, size, size, 
                                          colors[0] if colors else '#00ff00', 
                                          stroke='#000000', 
                                          stroke_width=2))
    
    return elements