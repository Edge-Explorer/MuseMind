from styles.base_style import BaseStyle

class WatercolorStyle(BaseStyle):
    """
    Watercolor painting style implementation
    """
    
    def __init__(self):
        super().__init__()
        self.name = "watercolor"
        self.positive_prompt = "watercolor painting, wet on wet technique, flowing colors, soft edges, watercolor paper texture, beautiful watercolor art style"
        self.negative_prompt = "digital art, crisp edges, solid colors, detailed, anime, cartoon, 3d render, oil painting, acrylic"
        self.inference_steps = 55
        self.guidance_scale = 7.2
        self.img2img_strength = 0.80  # Strong enough for the distinctive watercolor look
    
    def get_prompt(self, content):
        """
        Enhanced prompt generation for watercolor style
        
        Args:
            content (str): The base content to apply the style to
            
        Returns:
            str: The combined prompt with watercolor-specific enhancements
        """
        prompt = f"{content}, {self.positive_prompt}"
        
        # Add landscape-specific watercolor elements
        if any(term in content.lower() for term in ["landscape", "nature", "mountain", "forest", "sea", "sky", "garden"]):
            prompt += ", fluid watercolor landscape, bleeding colors, loose brushwork, atmospheric watercolor scene, color gradients"
            
        # Add floral/botanical-specific watercolor elements
        if any(term in content.lower() for term in ["flower", "plant", "botanical", "garden", "floral", "leaf"]):
            prompt += ", botanical watercolor illustration, delicate brushwork, transparent layers, soft color washes"
            
        # Add portrait-specific watercolor elements
        if any(term in content.lower() for term in ["portrait", "person", "face", "figure", "people"]):
            prompt += ", impressionistic watercolor portrait, fluid brushstrokes, soft color transitions, minimalist details"
            
        return prompt