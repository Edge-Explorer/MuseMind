from styles.base_style import BaseStyle

class OilPaintingStyle(BaseStyle):
    """
    Oil painting art style implementation
    """
    
    def __init__(self):
        super().__init__()
        self.name = "oil_painting"
        self.positive_prompt = "oil painting, detailed brushwork, textured canvas, rich colors, artistic, masterpiece oil painting style, professional art"
        self.negative_prompt = "digital art, smooth, flat colors, cartoon, anime, 3d render, blurry, grainy, photography, photo"
        self.inference_steps = 55
        self.guidance_scale = 7.5
        self.img2img_strength = 0.80  # Strong enough to apply the distinctive brushwork
    
    def get_prompt(self, content):
        """
        Enhanced prompt generation for oil painting style
        
        Args:
            content (str): The base content to apply the style to
            
        Returns:
            str: The combined prompt with oil painting-specific enhancements
        """
        prompt = f"{content}, {self.positive_prompt}"
        
        # Add portrait-specific oil painting elements
        if any(term in content.lower() for term in ["portrait", "person", "man", "woman", "face", "figure"]):
            prompt += ", traditional oil portrait, dramatic lighting, chiaroscuro, rich skin tones, realistic portrait painting"
            
        # Add landscape-specific oil painting elements
        if any(term in content.lower() for term in ["landscape", "nature", "mountain", "sea", "forest", "sky"]):
            prompt += ", landscape oil painting, atmospheric perspective, rich natural colors, detailed foliage, classical composition"
            
        # Add still life-specific oil painting elements
        if any(term in content.lower() for term in ["still life", "fruit", "flower", "object", "food", "book", "table"]):
            prompt += ", still life oil painting, rich textures, detailed objects, dramatic lighting, realistic textures"
            
        return prompt