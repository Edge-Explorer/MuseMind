from styles.base_style import BaseStyle

class CyberpunkStyle(BaseStyle):
    """
    Cyberpunk art style implementation
    """
    
    def __init__(self):
        super().__init__()
        self.name = "cyberpunk"
        self.positive_prompt = "cyberpunk style, neon lights, futuristic city, high tech low life, cybernetic, rain, night time, digital art, science fiction, vibrant colors"
        self.negative_prompt = "daylight, natural, rural, vintage, historical, low tech, grainy, blurry"
        self.inference_steps = 50
        self.guidance_scale = 8.0
        self.img2img_strength = 0.75  # Good balance for cyberpunk transformation
    
    def get_prompt(self, content):
        """
        Enhanced prompt generation for cyberpunk style
        
        Args:
            content (str): The base content to apply the style to
            
        Returns:
            str: The combined prompt with cyberpunk-specific enhancements
        """
        prompt = f"{content}, {self.positive_prompt}"
        
        # Add character-specific cyberpunk elements
        if any(term in content.lower() for term in ["person", "character", "man", "woman", "people"]):
            prompt += ", cybernetic implants, neon-lit face, urban outfit, tech-enhanced, holographic interface"
            
        # Add cityscape-specific cyberpunk elements
        if any(term in content.lower() for term in ["city", "urban", "street", "skyline", "building"]):
            prompt += ", towering skyscrapers, neon advertisements, holographic billboards, flying vehicles, smog, rain-slicked streets"
            
        # Add technology-specific cyberpunk elements
        if any(term in content.lower() for term in ["tech", "computer", "machine", "robot", "cyber", "vehicle"]):
            prompt += ", advanced technology, glowing interfaces, holographic displays, futuristic design"
            
        return prompt