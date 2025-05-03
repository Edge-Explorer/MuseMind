from styles.ghibli import GhibliStyle
from styles.pixel_art import PixelArtStyle
from styles.realistic import RealisticStyle
from styles.anime import AnimeStyle
from styles.comic_book import ComicBookStyle
from styles.cyberpunk import CyberpunkStyle
from styles.enhance import EnhanceStyle
from styles.fantasy import FantasyStyle
from styles.impressionist import ImpressionistStyle
from styles.oil_painting import OilPaintingStyle
from styles.pop_art import PopArtStyle
from styles.steampunk import SteampunkStyle
from styles.watercolor import WatercolorStyle


def get_style(style_name):
    """
    Factory function to get the appropriate style instance based on name
    
    Args:
        style_name (str): Name of the style to get
        
    Returns:
        BaseStyle: Instance of the requested style class or None if not found
    """
    if not style_name:
        return None
        
    style_name = style_name.lower().strip()
    
    # Dictionary mapping style names to their respective classes
    styles = {
        "ghibli": GhibliStyle,
        "pixel_art": PixelArtStyle,
        "pixelart": PixelArtStyle,  # Alias
        "realistic": RealisticStyle,
        "anime": AnimeStyle,
        "comic_book": ComicBookStyle,
        "comic": ComicBookStyle,  # Alias
        "cyberpunk": CyberpunkStyle,
        "enhance": EnhanceStyle,
        "fantasy": FantasyStyle,
        "impressionist": ImpressionistStyle,
        "oil_painting": OilPaintingStyle,
        "oil": OilPaintingStyle,  # Alias
        "pop_art": PopArtStyle,
        "popart": PopArtStyle,  # Alias
        "steampunk": SteampunkStyle,
        "watercolor": WatercolorStyle
    }
    
    # Check for common misspellings of "ghibli"
    if ("gib" in style_name or "ghib" in style_name) and "li" in style_name:
        return GhibliStyle()
    
    # Add forgiving matching for other common misspellings
    if "water" in style_name and "color" in style_name:
        return WatercolorStyle()
    
    if "cyber" in style_name and ("punk" in style_name or "tech" in style_name):
        return CyberpunkStyle()
    
    if "steam" in style_name and "punk" in style_name:
        return SteampunkStyle()
        
    # Return the style instance if it exists, otherwise None
    return styles[style_name]() if style_name in styles else None