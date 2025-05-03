from styles.base_style import BaseStyle

class SteampunkStyle(BaseStyle):
    """
    Steampunk art style implementation
    """
    
    def __init__(self):
        super().__init__()
        self.name = "steampunk"
        self.positive_prompt = "steampunk style, Victorian era, brass, copper, gears, steam-powered machinery, industrial revolution aesthetic, ornate details, vintage"
        self.negative_prompt = "modern, digital, minimalist, futuristic, plastic, electronic, contemporary"
        self.inference_steps = 50
        self.guidance_scale = 7.6
        self.img2img_strength = 0.70  # Good balance for steampunk transformation
    
    def get_prompt(self, content):
        """
        Enhanced prompt generation for steampunk style
        
        Args:
            content (str): The base content to apply the style to
            
        Returns:
            str: The combined prompt with steampunk-specific enhancements
        """
        prompt = f"{content}, {self.positive_prompt}"
        
        # Add character-specific steampunk elements
        if any(term in content.lower() for term in ["person", "character", "man", "woman", "portrait"]):
            prompt += ", Victorian clothing, brass goggles, mechanical prosthetics, gears, leather accents, pocket watch"
            
        # Add machine-specific steampunk elements
        if any(term in content.lower() for term in ["machine", "vehicle", "device", "invention", "airship", "engine"]):
            prompt += ", intricate brass machinery, steam-powered technology, exposed gears and pipes, ornate Victorian engineering"
            
        # Add environment-specific steampunk elements
        if any(term in content.lower() for term in ["city", "building", "interior", "factory", "workshop", "laboratory"]):
            prompt += ", industrial Victorian architecture, brass fixtures, steam pipes, clockwork mechanisms, gas lamps, ornate metalwork"
            
        return prompt