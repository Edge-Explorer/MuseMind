from styles.base_style import BaseStyle

class EnhanceStyle(BaseStyle):
    """
    Image enhancement style implementation (not truly a style, 
    but more of an image quality enhancement operation)
    """
    
    def __init__(self):
        super().__init__()
        self.name = "enhance"
        self.positive_prompt = "high quality, enhanced details, professional photo, perfect lighting, vibrant colors, sharp focus, 8K resolution"
        self.negative_prompt = "low quality, blurry, noise, compression artifacts, distorted, grainy, pixelated, overexposed, underexposed"
        self.inference_steps = 60  # Higher for better quality
        self.guidance_scale = 7.5
        self.img2img_strength = 0.60  # Lower to keep more original details
    
    def adjust_for_img2img(self, content):
        """
        For enhance mode, we'll use a special flag to indicate direct enhancement
        without using the diffusion model (for faster processing)
        
        Args:
            content (str): The base content description
            
        Returns:
            dict: Parameters with a special direct_enhance flag
        """
        return {
            "prompt": self.get_prompt(content),
            "negative_prompt": self.negative_prompt,
            "inference_steps": self.inference_steps,
            "guidance_scale": self.guidance_scale,
            "strength": self.img2img_strength,
            "direct_enhance": True  # Special flag for direct enhancement
        }