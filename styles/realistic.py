from styles.base_style import BaseStyle

class RealisticStyle(BaseStyle):
    """
    Photorealistic style implementation
    """
    
    def __init__(self):
        super().__init__()
        self.name = "realistic"
        self.positive_prompt = "photorealistic, highly detailed, professional photography, 8k, DSLR, perfect composition, masterpiece, photorealistic rendering"
        self.negative_prompt = "cartoon, anime, illustration, drawing, painting, crayon, sketch, disfigured, deformed, watermark, signature"
        self.inference_steps = 60  # Higher steps for more photorealistic details
        self.guidance_scale = 8.0
        self.img2img_strength = 0.60  # Lower strength to preserve more photographic details
        
    def get_prompt(self, content):
        """
        Enhanced prompt generation for realistic style
        
        Args:
            content (str): The base content to apply the style to
            
        Returns:
            str: The combined prompt with realistic-specific enhancements
        """
        prompt = f"{content}, {self.positive_prompt}"
        
        # Add photography-specific enhancements based on content
        if any(term in content.lower() for term in ["portrait", "person", "man", "woman", "people"]):
            prompt += ", portrait photography, bokeh, studio lighting, professional headshot"
        
        if any(term in content.lower() for term in ["landscape", "nature", "mountain", "ocean", "forest"]):
            prompt += ", nature photography, golden hour, dramatic lighting, high dynamic range"
            
        if any(term in content.lower() for term in ["city", "urban", "street", "building"]):
            prompt += ", urban photography, architectural photography, tilt-shift, dramatic perspective"
            
        return prompt