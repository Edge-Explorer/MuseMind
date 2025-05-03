from styles.base_style import BaseStyle

class ImpressionistStyle(BaseStyle):
    """
    Impressionist painting style implementation
    """
    
    def __init__(self):
        super().__init__()
        self.name = "impressionist"
        self.positive_prompt = "impressionist painting style, visible brushstrokes, emphasis on light, vibrant colors, Claude Monet style, en plein air, artistic masterpiece"
        self.negative_prompt = "detailed, sharp, realistic, digital art, 3d, anime, cartoon, smooth texture, photography"
        self.inference_steps = 55
        self.guidance_scale = 7.5
        self.img2img_strength = 0.80  # Strong enough to apply the distinctive brushwork
    
    def get_prompt(self, content):
        """
        Enhanced prompt generation for impressionist style
        
        Args:
            content (str): The base content to apply the style to
            
        Returns:
            str: The combined prompt with impressionist-specific enhancements
        """
        prompt = f"{content}, {self.positive_prompt}"
        
        # Add nature-specific impressionist elements
        if any(term in content.lower() for term in ["landscape", "garden", "water", "lake", "river", "sea", "field", "nature"]):
            prompt += ", impressionist landscape, natural light effects, en plein air painting, vibrant natural colors, Monet-like water reflections"
            
        # Add urban-specific impressionist elements
        if any(term in content.lower() for term in ["city", "street", "building", "urban", "cafe", "paris"]):
            prompt += ", impressionist cityscape, atmospheric perspective, Parisian impressionism, cafe scenes, urban light effects"
            
        # Add figure-specific impressionist elements
        if any(term in content.lower() for term in ["person", "people", "figure", "portrait", "woman", "man"]):
            prompt += ", impressionist figure painting, soft edges, loose brushwork, emphasis on light and atmosphere over detail"
            
        return prompt