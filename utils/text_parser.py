from typing import Dict, List, Set, Tuple, Optional
import re

class TextParser:
    """Parse text descriptions to extract relevant information for SVG generation."""
    
    def __init__(self):
        """Initialize the text parser with common vocabularies."""
        self.color_terms = {
            'red', 'scarlet', 'crimson', 'blue', 'sky-blue', 'navy', 'azure',
            'green', 'emerald', 'lime', 'yellow', 'gold', 'amber', 'purple',
            'violet', 'lavender', 'magenta', 'orange', 'tangerine', 'pink',
            'fuchsia', 'rose', 'brown', 'chocolate', 'tan', 'beige', 'black',
            'white', 'gray', 'silver', 'turquoise', 'teal', 'aqua', 'cyan',
            'indigo', 'copper', 'bronze', 'pewter', 'ivory', 'ebony', 
            'chestnut', 'ginger', 'wine', 'aubergine', 'charcoal'
        }
        
        self.shape_terms = {
            'circle', 'square', 'triangle', 'rectangle', 'oval', 'ellipse',
            'polygon', 'hexagon', 'octagon', 'pentagon', 'star', 'cube',
            'pyramid', 'sphere', 'cone', 'cylinder', 'prism', 'diamond',
            'parallelogram', 'trapezoid', 'rhombus', 'crescent', 'arc'
        }
        
        self.pattern_terms = {
            'striped', 'checkered', 'dotted', 'spotted', 'floral', 'zigzag',
            'wavy', 'plaid', 'herringbone', 'houndstooth', 'paisley', 'grid',
            'polka dot', 'chevron', 'argyle', 'tartan', 'pinstripe'
        }
        
        self.material_terms = {
            'wood', 'leather', 'silk', 'cotton', 'wool', 'linen', 'metal',
            'glass', 'ceramic', 'plastic', 'rubber', 'stone', 'marble',
            'granite', 'velvet', 'satin', 'denim', 'corduroy', 'cashmere',
            'tweed', 'suede', 'fleece', 'canvas', 'polyester', 'nylon', 
            'ribbed', 'synthetic'
        }
        
        self.clothing_terms = {
            'shirt', 'pants', 'jacket', 'coat', 'dress', 'skirt', 'blouse',
            'sweater', 'cardigan', 'jeans', 'trousers', 'suit', 'blazer',
            'hoodie', 'sweatshirt', 'vest', 'underwear', 'socks', 'shoes',
            'boots', 'sneakers', 'sandals', 'hat', 'cap', 'gloves', 'scarf',
            'tie', 'belt', 'accessories', 'jewelry', 'watch', 'ring', 
            'necklace', 'bracelet', 'earrings', 'overcoat', 'dungarees',
            'neckerchief', 'trousers'
        }
        
        self.landscape_terms = {
            'mountain', 'valley', 'river', 'lake', 'ocean', 'sea', 'forest',
            'jungle', 'desert', 'beach', 'island', 'hill', 'cliff', 'canyon',
            'waterfall', 'glacier', 'meadow', 'field', 'farm', 'garden',
            'park', 'swamp', 'marsh', 'plains', 'dunes', 'plateau', 'tundra',
            'savanna', 'prairie', 'steppe', 'cave', 'volcano', 'geyser',
            'hot spring', 'coral reef', 'bay', 'peninsula', 'isthmus',
            'strait', 'sound', 'fjord', 'harbor', 'gulf', 'lagoon', 'sky',
            'cloud', 'sun', 'moon', 'star', 'rainbow', 'aurora', 'sunset',
            'sunrise', 'dawn', 'dusk', 'horizon', 'expanse', 'vista'
        }
        
        self.architectural_terms = {
            'building', 'house', 'apartment', 'skyscraper', 'tower', 'castle',
            'palace', 'temple', 'church', 'cathedral', 'mosque', 'synagogue',
            'bridge', 'dam', 'tunnel', 'road', 'street', 'avenue', 'highway',
            'path', 'trail', 'fence', 'wall', 'gate', 'door', 'window',
            'roof', 'chimney', 'arch', 'column', 'pillar', 'staircase',
            'elevator', 'escalator', 'fountain', 'statue', 'monument',
            'sculpture', 'garden', 'park', 'plaza', 'square', 'courtyard',
            'patio', 'terrace', 'balcony', 'porch', 'deck', 'shed', 'garage',
            'barn', 'silo', 'lighthouse', 'windmill', 'watermill', 'beacon'
        }
        
        # Combined vocabulary for faster lookups
        self.all_terms = self.color_terms.union(self.shape_terms).union(self.pattern_terms).union(
            self.material_terms).union(self.clothing_terms).union(self.landscape_terms).union(
            self.architectural_terms)
    
    def extract_colors(self, description: str) -> List[str]:
        """Extract color terms from the description."""
        description_lower = description.lower()
        found_colors = []
        
        for color in self.color_terms:
            if color in description_lower:
                found_colors.append(color)
        
        return found_colors
    
    def extract_shapes(self, description: str) -> List[str]:
        """Extract shape terms from the description."""
        description_lower = description.lower()
        found_shapes = []
        
        for shape in self.shape_terms:
            if shape in description_lower:
                found_shapes.append(shape)
        
        return found_shapes
    
    def extract_patterns(self, description: str) -> List[str]:
        """Extract pattern terms from the description."""
        description_lower = description.lower()
        found_patterns = []
        
        for pattern in self.pattern_terms:
            if pattern in description_lower:
                found_patterns.append(pattern)
        
        return found_patterns
    
    def extract_materials(self, description: str) -> List[str]:
        """Extract material terms from the description."""
        description_lower = description.lower()
        found_materials = []
        
        for material in self.material_terms:
            if material in description_lower:
                found_materials.append(material)
        
        return found_materials
    
    def extract_clothing(self, description: str) -> List[str]:
        """Extract clothing terms from the description."""
        description_lower = description.lower()
        found_clothing = []
        
        for clothing in self.clothing_terms:
            if clothing in description_lower:
                found_clothing.append(clothing)
        
        return found_clothing
    
    def extract_landscape(self, description: str) -> List[str]:
        """Extract landscape terms from the description."""
        description_lower = description.lower()
        found_landscape = []
        
        for landscape in self.landscape_terms:
            if landscape in description_lower:
                found_landscape.append(landscape)
        
        return found_landscape
    
    def extract_architecture(self, description: str) -> List[str]:
        """Extract architectural terms from the description."""
        description_lower = description.lower()
        found_architecture = []
        
        for architecture in self.architectural_terms:
            if architecture in description_lower:
                found_architecture.append(architecture)
        
        return found_architecture
    
    def extract_all_terms(self, description: str) -> Dict[str, List[str]]:
        """Extract all recognized terms from the description."""
        return {
            'colors': self.extract_colors(description),
            'shapes': self.extract_shapes(description),
            'patterns': self.extract_patterns(description),
            'materials': self.extract_materials(description),
            'clothing': self.extract_clothing(description),
            'landscape': self.extract_landscape(description),
            'architecture': self.extract_architecture(description)
        }
    
    def get_primary_category(self, description: str) -> Tuple[str, List[str]]:
        """Determine the primary category of the description."""
        extracted = self.extract_all_terms(description)
        
        # Find the category with the most terms
        max_count = 0
        primary_category = 'general'
        primary_terms = []
        
        for category, terms in extracted.items():
            if len(terms) > max_count:
                max_count = len(terms)
                primary_category = category
                primary_terms = terms
        
        return primary_category, primary_terms
