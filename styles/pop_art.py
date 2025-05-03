from styles.base_style import BaseStyle

class PopArtStyle(BaseStyle):
    """
    Pop Art style implementation
    """
    
    def __init__(self):
        super().__init__()
        self.name = "pop_art"
        self.positive_prompt = "pop art style, bold colors, halftone dots, Andy Warhol inspired, Roy Lichtenstein style, strong contrasts, flat graphic design elements"
        self.negative_prompt = "realistic, monochrome, subtle, detailed, painterly, organic, sketch, 3d render"
        self.inference_steps = 50
        self.guidance_scale = 8.0
        self.img2img_strength = 0.80  # Strong enough for the distinctive style
    
    def get_prompt(self, content):
        """
        Enhanced prompt generation for pop art style
        
        Args:
            content (str): The base content to apply the style to
            
        Returns:
            str: The combined prompt with pop art-specific enhancements
        """
        prompt = f"{content}, {self.positive_prompt}"
        
        # Add Warhol-specific pop art elements
        if any(term in content.lower() for term in ["portrait", "face", "celebrity", "icon", "repeated", "multiple"]):
            prompt += ", Andy Warhol style, repeated images, bright contrasting colors, screen printing effect, iconic portrait"
            
        # Add Lichtenstein-specific pop art elements
        if any(term in content.lower() for term in ["comic", "emotion", "speech", "thought", "action", "dramatic"]):
            prompt += ", Roy Lichtenstein style, ben-day dots, thick black outlines, primary colors, comic strip aesthetic, speech bubbles"
            
        # Add general mid-century pop art elements
        if any(term in content.lower() for term in ["object", "product", "commercial", "advertisement", "consumer"]):
            prompt += ", commercial pop art, consumer product aesthetic, advertising style, bold typography, graphic design elements"
            
        return prompt