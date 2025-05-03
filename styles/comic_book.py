from styles.base_style import BaseStyle

class ComicBookStyle(BaseStyle):
    """
    Comic book art style implementation
    """
    
    def __init__(self):
        super().__init__()
        self.name = "comic_book"
        self.positive_prompt = "comic book style, bold lines, flat colors, comic panel, detailed comic art, vibrant, ink drawing with color, dynamic composition"
        self.negative_prompt = "realistic, 3d render, photography, watercolor, blurry, grainy, low contrast"
        self.inference_steps = 45
        self.guidance_scale = 7.8
        self.img2img_strength = 0.75  # Good balance for comic transformation
    
    def get_prompt(self, content):
        """
        Enhanced prompt generation for comic book style
        
        Args:
            content (str): The base content to apply the style to
            
        Returns:
            str: The combined prompt with comic-specific enhancements
        """
        prompt = f"{content}, {self.positive_prompt}"
        
        # Add superhero comic elements if appropriate
        if any(term in content.lower() for term in ["hero", "superhero", "villain", "fight", "action", "battle"]):
            prompt += ", superhero comic art style, action lines, dynamic poses, dramatic lighting"
            
        # Add narrative comic elements if appropriate
        if any(term in content.lower() for term in ["story", "narrative", "scene", "character"]):
            prompt += ", narrative comic panel, expressive characters, thought bubbles, iconic comic art"
            
        return prompt