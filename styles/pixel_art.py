from .base_style import BaseStyle

class PixelArtStyle(BaseStyle):
    """
    Pixel Art style - creates retro game-like pixel graphics
    with limited color palette and pixelated appearance.
    """
    
    def __init__(self):
        super().__init__()
        self.name = "pixel_art"
        self.positive_prompt = "pixel art style, 8-bit, 16-bit, retro game graphics, pixelated, limited color palette, video game art, pixel art masterpiece, sharp pixel edges, blocky, retro game aesthetic, crisp pixels"
        self.negative_prompt = "smooth, blurry, detailed, realistic, 3d, high resolution, photography, oil painting, gradient colors, anti-aliasing, dithering"
        self.inference_steps = 30  # Reduced steps for more defined pixel blocks
        self.guidance_scale = 10.0  # Higher guidance for stronger style adherence
        self.img2img_strength = 0.85  # Higher strength for pixel art conversion
        
        # Pixel art specific parameters
        self.pixel_size = 8  # Default pixel size
        self.color_count = 24  # Default color count
        
    def adjust_for_img2img(self, content):
        """
        Make pixel art specific adjustments for img2img processing
        
        Args:
            content (str): The base content description
            
        Returns:
            dict: Adjusted parameters including prompt
        """
        params = super().adjust_for_img2img(content)
        
        # Detect content types
        content_types = self.detect_content_type(content)
        
        # Customize prompt based on content
        if content_types["has_person"]:
            params["prompt"] += ", pixel sprite character, 16-bit character design"
            
        if content_types["has_landscape"]:
            params["prompt"] += ", pixel art background, retro game environment"
            
        if content_types["has_tech"]:
            params["prompt"] += ", sci-fi pixel art, tech sprites, 16-bit technology"
            
        if content_types["has_urban"]:
            params["prompt"] += ", pixel city, retro game city background"
        
        # For action scenes, use more dynamic pixel art style
        if content_types["has_action"]:
            params["prompt"] += ", dynamic pixel art scene, retro game action sequence"
            params["strength"] = 0.9  # Higher strength for action scenes
            
        return params
    
    def set_pixel_size(self, size):
        """
        Set the pixel size for rendering
        
        Args:
            size (int): Pixel size (higher = more pixelated)
        """
        self.pixel_size = max(2, min(32, size))  # Clamp between 2 and 32
        
    def set_color_count(self, count):
        """
        Set the color count for the reduced color palette
        
        Args:
            count (int): Number of colors (lower = more retro look)
        """
        self.color_count = max(8, min(64, count))  # Clamp between 8 and 64
        
    def match_game_era(self, era):
        """
        Configure style parameters to match specific gaming era
        
        Args:
            era (str): Gaming era ('8bit', '16bit', '32bit', etc.)
        """
        era = era.lower().replace('-', '').replace('_', '')
        
        if era == '8bit' or era == 'nes':
            self.pixel_size = 16
            self.color_count = 16
            self.positive_prompt = "8-bit NES style pixel art, limited NES color palette, low resolution pixel graphics, simple pixel shapes, NES game aesthetic, 8-bit sprites"
            
        elif era == '16bit' or era == 'snes' or era == 'genesis':
            self.pixel_size = 8
            self.color_count = 32
            self.positive_prompt = "16-bit SNES style pixel art, SNES color palette, detailed pixel graphics, 16-bit sprite design, SNES game aesthetic"
            
        elif era == '32bit' or era == 'ps1':
            self.pixel_size = 4
            self.color_count = 64
            self.positive_prompt = "32-bit PlayStation era pixel art, higher color depth, pixel art with detailed shading, PS1 aesthetic, more colorful pixel graphics"
        
    def apply_game_style(self, game_style):
        """
        Apply a specific game's art style
        
        Args:
            game_style (str): Game style reference (e.g. 'zelda', 'mario', 'metroid')
        """
        game_style = game_style.lower().strip()
        
        style_map = {
            'zelda': "Legend of Zelda pixel art style, top-down pixel graphics, Zelda-like sprites, fantasy pixel art, Hyrule-inspired pixel landscapes",
            'mario': "Super Mario pixel art style, vibrant pixel colors, platformer game sprites, Mario-inspired character design, mushroom kingdom pixel art",
            'metroid': "Metroid-style pixel art, sci-fi pixel environments, space pixel art, dark atmosphere, Metroid-inspired alien pixel designs",
            'pokemon': "Pokemon-style pixel art, monster catching game aesthetic, Pokemon-inspired creature design, RPG overworld pixel style",
            'final_fantasy': "Final Fantasy pixel RPG style, JRPG pixel art, detailed character sprites, fantasy pixel environments, classic RPG UI elements",
            'sonic': "Sonic the Hedgehog pixel style, fast-moving character design, Genesis-era sprites, vibrant colorful pixel backgrounds, Sonic-inspired level design",
            'castlevania': "Castlevania pixel art style, gothic horror pixel graphics, detailed architecture, dramatic lighting in pixel form, horror game pixel aesthetic",
            'megaman': "Mega Man pixel art style, robot character design, sci-fi action platformer sprites, Mega Man-inspired enemy designs, tech pixel art"
        }
        
        if game_style in style_map:
            self.positive_prompt = style_map[game_style]
            
            # Adjust other parameters based on game style
            if game_style == 'zelda' or game_style == 'pokemon':
                self.pixel_size = 8
                self.color_count = 32
            elif game_style == 'mario' or game_style == 'sonic':
                self.pixel_size = 8
                self.color_count = 48
            elif game_style == 'metroid' or game_style == 'castlevania':
                self.pixel_size = 6
                self.color_count = 32
            elif game_style == 'megaman':
                self.pixel_size = 6
                self.color_count = 24
            elif game_style == 'final_fantasy':
                self.pixel_size = 8
                self.color_count = 64