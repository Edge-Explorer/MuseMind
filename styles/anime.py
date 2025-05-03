from styles.base_style import BaseStyle

class AnimeStyle(BaseStyle):
    """
    Anime art style implementation
    """
    
    def __init__(self):
        super().__init__()
        self.name = "anime"
        self.positive_prompt = "anime style, detailed anime illustration, vibrant colors, clean lines, high quality anime art, anime aesthetic"
        self.negative_prompt = "low quality, blurry, distorted, deformed, disfigured, bad anatomy, western style, realistic, photo"
        self.inference_steps = 50
        self.guidance_scale = 7.5
        self.img2img_strength = 0.70  # Good balance for anime transformation
    
    def get_prompt(self, content):
        """
        Enhanced prompt generation for anime style
        
        Args:
            content (str): The base content to apply the style to
            
        Returns:
            str: The combined prompt with anime-specific enhancements
        """
        prompt = f"{content}, {self.positive_prompt}"
        
        # Add character-specific enhancements
        if any(term in content.lower() for term in ["person", "woman", "man", "girl", "boy", "character", "people"]):
            prompt += ", anime character design, expressive eyes, dynamic pose, detailed clothing"
            
        # Add scene-specific enhancements
        if any(term in content.lower() for term in ["landscape", "city", "background", "scene"]):
            prompt += ", detailed anime background art, beautiful scenery, dynamic lighting"
            
        return prompt