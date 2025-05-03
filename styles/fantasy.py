from styles.base_style import BaseStyle

class FantasyStyle(BaseStyle):
    """
    Fantasy art style implementation
    """
    
    def __init__(self):
        super().__init__()
        self.name = "fantasy"
        self.positive_prompt = "fantasy art style, magical, mythical, epic scene, dramatic lighting, detailed fantasy illustration, dungeons and dragons style, high quality fantasy concept art"
        self.negative_prompt = "modern, urban, sci-fi, mundane, realistic photo, low quality, blurry"
        self.inference_steps = 55
        self.guidance_scale = 7.5
        self.img2img_strength = 0.70  # Good balance for fantasy transformation
    
    def get_prompt(self, content):
        """
        Enhanced prompt generation for fantasy style
        
        Args:
            content (str): The base content to apply the style to
            
        Returns:
            str: The combined prompt with fantasy-specific enhancements
        """
        prompt = f"{content}, {self.positive_prompt}"
        
        # Add character-specific fantasy elements
        if any(term in content.lower() for term in ["character", "person", "warrior", "mage", "wizard", "hero", "knight", "elf", "dwarf", "orc"]):
            prompt += ", fantasy character design, magical aura, mythical armor, enchanted weapons, heroic pose"
            
        # Add landscape-specific fantasy elements
        if any(term in content.lower() for term in ["landscape", "castle", "mountain", "forest", "kingdom", "realm"]):
            prompt += ", epic fantasy landscape, magical atmosphere, mystical light, otherworldly, fantasy environment"
            
        # Add creature-specific fantasy elements
        if any(term in content.lower() for term in ["dragon", "monster", "creature", "beast", "magical"]):
            prompt += ", mythical creature, fantasy beast design, magical aura, epic fantasy monster"
            
        return prompt