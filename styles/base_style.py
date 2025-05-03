class BaseStyle:
    """
    Base class for all art styles to inherit from.
    Defines the common interface and default values.
    """
    
    def __init__(self):
        self.name = "base"  # Override in subclasses
        self.positive_prompt = ""  # Override in subclasses
        self.negative_prompt = "low quality, blurry, distorted, deformed, disfigured, bad anatomy, ugly, amateur"
        self.inference_steps = 50
        self.guidance_scale = 7.5
        self.img2img_strength = 0.75
        
    def get_prompt(self, content):
        """
        Generate the full prompt by combining the content with style-specific positive prompt
        
        Args:
            content (str): The base content to apply the style to
            
        Returns:
            str: The combined prompt
        """
        return f"{content}, {self.positive_prompt}"
    
    def get_style_info(self):
        """
        Return a dictionary with all the style parameters
        
        Returns:
            dict: Style parameters
        """
        return {
            "name": self.name,
            "positive": self.positive_prompt,
            "negative": self.negative_prompt,
            "inference_steps": self.inference_steps,
            "guidance_scale": self.guidance_scale,
            "img2img_strength": self.img2img_strength
        }
    
    def adjust_for_img2img(self, content):
        """
        Make any style-specific adjustments for img2img processing
        
        Args:
            content (str): The base content description
            
        Returns:
            dict: Adjusted parameters including prompt
        """
        # Default implementation - can be overridden in subclasses
        return {
            "prompt": self.get_prompt(content),
            "negative_prompt": self.negative_prompt,
            "inference_steps": self.inference_steps,
            "guidance_scale": self.guidance_scale,
            "strength": self.img2img_strength
        }
        
    def detect_content_type(self, content):
        """
        Helper method to detect content types in the prompt.
        Used by subclasses to apply specific enhancements.
        
        Args:
            content (str): The base content to analyze
            
        Returns:
            dict: Dictionary of detected content types
        """
        content_lower = content.lower()
        
        return {
            # Characters/people
            "has_person": any(term in content_lower for term in ["person", "character", "man", "woman", "people", "face", "portrait", "figure", "boy", "girl", "child"]),
            
            # Landscapes/nature
            "has_landscape": any(term in content_lower for term in ["landscape", "nature", "mountain", "forest", "sky", "clouds", "sea", "ocean", "lake", "river", "field", "garden"]),
            
            # Urban/city
            "has_urban": any(term in content_lower for term in ["city", "urban", "street", "building", "architecture", "skyline", "town"]),
            
            # Technology/machines
            "has_tech": any(term in content_lower for term in ["tech", "technology", "computer", "machine", "robot", "device", "mechanical", "electronic", "vehicle"]),
            
            # Still life/objects
            "has_object": any(term in content_lower for term in ["still life", "object", "fruit", "flower", "book", "food", "item", "product"]),
            
            # Action/narrative
            "has_action": any(term in content_lower for term in ["action", "battle", "fight", "movement", "dynamic", "story", "narrative", "scene"])
        }