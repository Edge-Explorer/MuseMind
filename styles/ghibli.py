from .base_style import BaseStyle

class GhibliStyle(BaseStyle):
    """
    Studio Ghibli style - creates images in the distinctive artistic style
    of Studio Ghibli animation films, characterized by painterly 
    backgrounds, expressive characters, and whimsical elements.
    """
    
    def __init__(self):
        super().__init__()
        self.name = "ghibli"
        self.positive_prompt = "Studio Ghibli anime style, Miyazaki style, pastel colors, soft lighting, detailed backgrounds, hand-drawn animation style, whimsical, painterly, detailed traditional animation, background art by Kazuo Oga, character design by Hayao Miyazaki"
        self.negative_prompt = "3D, CGI, photorealistic, hyper-detailed, low quality, blurry, distorted, deformed, disfigured, bad anatomy, disproportionate, unnatural colors, oversaturated, high contrast"
        self.inference_steps = 55
        self.guidance_scale = 8.0
        self.img2img_strength = 0.60  # Lower strength to preserve more of the original image structure
        
        # Ghibli film specific parameters
        self.film_style = None
        
    def adjust_for_img2img(self, content):
        """
        Make Ghibli-specific adjustments for img2img processing
        
        Args:
            content (str): The base content description
            
        Returns:
            dict: Adjusted parameters including prompt
        """
        params = super().adjust_for_img2img(content)
        
        # Detect content types
        content_types = self.detect_content_type(content)
        
        # Add character-specific elements
        if content_types["has_person"]:
            params["prompt"] += ", iconic Ghibli character design, expressive eyes, simple facial features, naturalistic proportions"
            
        # Add landscape-specific elements
        if content_types["has_landscape"]:
            params["prompt"] += ", Ghibli background art, atmospheric perspective, detailed natural elements, dynamic clouds, painterly landscapes"
            params["inference_steps"] = 60  # More steps for detailed landscapes
            
        # Add specific elements for urban scenes
        if content_types["has_urban"]:
            params["prompt"] += ", detailed Ghibli city background, European-inspired architecture, quaint town design"
            
        # Additional film-specific styling if set
        if self.film_style:
            params["prompt"] += f", {self.film_style}"
            
        return params
    
    def apply_film_style(self, film):
        """
        Apply a specific Ghibli film's art style
        
        Args:
            film (str): Film reference (e.g. 'spirited_away', 'totoro', 'mononoke')
        """
        film = film.lower().replace(' ', '_')
        
        film_styles = {
            'spirited_away': "Spirited Away art style, warm fantasy lighting, otherworldly architecture, mystical bathhouse setting, water elements, Japanese folklore elements",
            'totoro': "My Neighbor Totoro art style, lush forest scenery, rural Japanese countryside, soft natural lighting, summer atmosphere, magical forest creatures",
            'mononoke': "Princess Mononoke art style, ancient forest, Japanese mythology, spiritual forest elements, nature spirits, dramatic lighting, detailed texture",
            'howls_moving_castle': "Howl's Moving Castle art style, steampunk elements, European fantasy architecture, magical mechanisms, soft fantasy lighting",
            'kiki': "Kiki's Delivery Service art style, European coastal town, flying scenes, cozy atmosphere, warm lighting, gentle colors",
            'castle_in_the_sky': "Castle in the Sky art style, floating islands, ancient technology, dramatic sky perspectives, adventure atmosphere",
            'porco_rosso': "Porco Rosso art style, Mediterranean setting, vintage airplanes, 1920s setting, blue ocean, rocky islands",
            'nausicaa': "Nausicaa art style, post-apocalyptic landscape, toxic jungle, fantasy creatures, dramatic skies, insect designs",
            'ponyo': "Ponyo art style, vibrant underwater scenes, seaside imagery, childlike wonder, flowing water effects, playful character design"
        }
        
        # Set film-specific style if found, otherwise use a generic enhancement
        if film in film_styles:
            self.film_style = film_styles[film]
            
            # Adjust other parameters based on film style
            if film == 'spirited_away' or film == 'howls_moving_castle':
                self.guidance_scale = 8.5
            elif film == 'totoro' or film == 'kiki':
                self.guidance_scale = 7.5
                self.img2img_strength = 0.55  # More subtle transformation
            elif film == 'mononoke' or film == 'nausicaa':
                self.guidance_scale = 9.0  # Stronger guidance for more dramatic styles
                self.img2img_strength = 0.65
            elif film == 'ponyo':
                self.guidance_scale = 7.0
                self.img2img_strength = 0.55
                self.inference_steps = 60  # More steps for water effects
        else:
            # Generic enhancement for unrecognized film
            self.film_style = "classic Studio Ghibli animation style, Miyazaki-directed film"
    
    def apply_scene_type(self, scene_type):
        """
        Optimize the style for a specific type of scene
        
        Args:
            scene_type (str): Type of scene ('landscape', 'character', 'action', etc)
        """
        scene_type = scene_type.lower().strip()
        
        scene_enhancements = {
            'landscape': {
                'prompt': "expansive Ghibli landscape, atmospheric perspective, detailed natural elements, painterly style, dramatic sky, Kazuo Oga background art style",
                'steps': 60,
                'strength': 0.65,
                'guidance': 8.5
            },
            'character': {
                'prompt': "Ghibli character design, expressive face, simple features, emotional expression, gentle lighting, character close-up, Studio Ghibli character sheet",
                'steps': 50,
                'strength': 0.55,
                'guidance': 7.5
            },
            'action': {
                'prompt': "dynamic Ghibli animation scene, movement lines, action pose, dramatic moment, Studio Ghibli action sequence",
                'steps': 55,
                'strength': 0.70,
                'guidance': 8.0
            },
            'interior': {
                'prompt': "detailed Ghibli interior design, cozy atmosphere, lived-in space, soft lighting, attention to small details",
                'steps': 55,
                'strength': 0.60,
                'guidance': 7.5
            },
            'fantasy': {
                'prompt': "magical Ghibli fantasy elements, whimsical creatures, fantasy landscape, otherworldly setting, magical atmosphere",
                'steps': 60,
                'strength': 0.70,
                'guidance': 8.5
            },
            'flying': {
                'prompt': "Ghibli flying scene, soaring through clouds, aerial perspective, wind effects, sense of freedom, sky adventure",
                'steps': 55,
                'strength': 0.65,
                'guidance': 8.0
            }
        }
        
        if scene_type in scene_enhancements:
            enhancement = scene_enhancements[scene_type]
            self.positive_prompt += f", {enhancement['prompt']}"
            self.inference_steps = enhancement['steps']
            self.img2img_strength = enhancement['strength']
            self.guidance_scale = enhancement['guidance']