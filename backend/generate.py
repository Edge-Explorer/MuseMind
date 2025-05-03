import os
import torch
from diffusers import StableDiffusionPipeline, DPMSolverMultistepScheduler, StableDiffusionImg2ImgPipeline
import base64
from io import BytesIO
from PIL import Image, ImageEnhance, ImageFilter, ImageOps
import time
import re
import numpy as np
from styles import get_style

# Global variables to keep models in memory
TEXT_TO_IMAGE_PIPELINE = None
IMG_TO_IMG_PIPELINE = None

# Function to initialize pipelines only once
def initialize_pipeline(pipeline_type="text2img", device=None):
    """
    Initialize and return the requested pipeline type.
    Reuses existing pipeline if already loaded.
    
    Args:
        pipeline_type (str): "text2img" or "img2img"
        device (str): Device to use, defaults to auto-detection
        
    Returns:
        Pipeline object
    """
    global TEXT_TO_IMAGE_PIPELINE, IMG_TO_IMG_PIPELINE
    
    # Auto-detect device if not specified
    if device is None:
        device = "cuda" if torch.cuda.is_available() else "cpu"
    
    torch_dtype = torch.float16 if device == "cuda" else torch.float32
    model_path = "./model/stable-diffusion-v1-5"
    
    if pipeline_type == "text2img" and TEXT_TO_IMAGE_PIPELINE is None:
        print(f"Initializing text-to-image pipeline on {device}...")
        TEXT_TO_IMAGE_PIPELINE = StableDiffusionPipeline.from_pretrained(
            model_path,
            torch_dtype=torch_dtype,
            safety_checker=None,
        )
        TEXT_TO_IMAGE_PIPELINE.scheduler = DPMSolverMultistepScheduler.from_config(
            TEXT_TO_IMAGE_PIPELINE.scheduler.config,
            use_karras_sigmas=True,  # Better quality sigmas
            algorithm_type="dpmsolver++",  # Better algorithm
        )
        TEXT_TO_IMAGE_PIPELINE = TEXT_TO_IMAGE_PIPELINE.to(device)
        TEXT_TO_IMAGE_PIPELINE.enable_attention_slicing()
        
        # Enable model offloading if on CUDA to save VRAM
        if device == "cuda":
            TEXT_TO_IMAGE_PIPELINE.enable_model_cpu_offload()
        
        return TEXT_TO_IMAGE_PIPELINE
        
    elif pipeline_type == "img2img" and IMG_TO_IMG_PIPELINE is None:
        print(f"Initializing image-to-image pipeline on {device}...")
        IMG_TO_IMG_PIPELINE = StableDiffusionImg2ImgPipeline.from_pretrained(
            model_path,
            torch_dtype=torch_dtype,
            safety_checker=None,
        )
        # Use the same improved scheduler
        IMG_TO_IMG_PIPELINE.scheduler = DPMSolverMultistepScheduler.from_config(
            IMG_TO_IMG_PIPELINE.scheduler.config,
            use_karras_sigmas=True,
            algorithm_type="dpmsolver++",
        )
        IMG_TO_IMG_PIPELINE = IMG_TO_IMG_PIPELINE.to(device)
        IMG_TO_IMG_PIPELINE.enable_attention_slicing()
        
        # Enable model offloading if on CUDA to save VRAM
        if device == "cuda":
            IMG_TO_IMG_PIPELINE.enable_model_cpu_offload()
            
        return IMG_TO_IMG_PIPELINE
    
    # Return existing pipeline
    return TEXT_TO_IMAGE_PIPELINE if pipeline_type == "text2img" else IMG_TO_IMG_PIPELINE

# Enhanced pixelation for better pixel art quality
def pixelate_image(image, pixel_size=8):
    """
    Apply true pixel art effect with enhanced quality
    
    Args:
        image (PIL.Image): Input image
        pixel_size (int): Size of the pixels (higher = more pixelated)
        
    Returns:
        PIL.Image: Pixelated image with improved quality
    """
    # Get original size
    width, height = image.size
    
    # For better quality pixel art, first enhance the contrast slightly
    enhancer = ImageEnhance.Contrast(image)
    image = enhancer.enhance(1.2)
    
    # Resize down to create pixel effect - use BICUBIC for initial downsampling
    # for better detail preservation
    small_width = max(width // pixel_size, 1)
    small_height = max(height // pixel_size, 1)
    small_image = image.resize((small_width, small_height), Image.BICUBIC)
    
    # Resize back up creating visible pixels - NEAREST for crisp pixel edges
    pixelated_image = small_image.resize((width, height), Image.NEAREST)
    
    return pixelated_image

# Improved color reduction with better palette generation
def reduce_colors(image, num_colors=16):
    """
    Reduce the number of colors with enhanced palette selection
    
    Args:
        image (PIL.Image): Input image
        num_colors (int): Number of colors to reduce to
        
    Returns:
        PIL.Image: Image with optimized color palette
    """
    if image.mode != 'RGB':
        image = image.convert('RGB')
    
    # Use better dithering method for higher quality color reduction
    reduced_img = image.quantize(colors=num_colors, method=2, dither=Image.FLOYDSTEINBERG)
    
    # Convert back to RGB for further processing
    return reduced_img.convert('RGB')

# Comprehensive image enhancement function for better quality
def enhance_image_quality(image, enhancement_level=1.2, sharpness=1.3, contrast=1.2, saturation=1.3):
    """
    Enhanced image quality with more control over individual parameters
    
    Args:
        image (PIL.Image): Input image
        enhancement_level (float): Overall level multiplier
        sharpness (float): Sharpness enhancement level
        contrast (float): Contrast enhancement level
        saturation (float): Color saturation level
        
    Returns:
        PIL.Image: Enhanced image
    """
    # Convert to RGB if not already
    if image.mode != 'RGB':
        image = image.convert('RGB')
    
    # Apply sharpness enhancement
    enhancer = ImageEnhance.Sharpness(image)
    image = enhancer.enhance(sharpness * enhancement_level)
    
    # Apply contrast enhancement
    enhancer = ImageEnhance.Contrast(image)
    image = enhancer.enhance(contrast * enhancement_level)
    
    # Apply color enhancement
    enhancer = ImageEnhance.Color(image)
    image = enhancer.enhance(saturation * enhancement_level)
    
    # Apply brightness enhancement (slightly)
    enhancer = ImageEnhance.Brightness(image)
    image = enhancer.enhance(1.05)
    
    # Apply subtle unsharp mask filter for edge enhancement
    if enhancement_level > 1.1:
        image = image.filter(ImageFilter.UnsharpMask(radius=1.5, percent=150, threshold=3))
    
    return image

# Optimized function to generate image from prompt with improved quality
def generate_image(prompt: str, width: int = 512, height: int = 512, style: str = None):
    """
    Generate an image based on the provided prompt and style with enhanced quality.
    
    Args:
        prompt (str): The text prompt describing the image to generate
        width (int): Width of the output image (default: 512)
        height (int): Height of the output image (default: 512)
        style (str): Optional style to apply (e.g., "ghibli", "anime", "realistic")
        
    Returns:
        str: Base64 encoded string of the generated image
    """
    # Check if CUDA is available for GPU acceleration
    device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"Using device: {device}")
    
    # Get or initialize the pipeline
    pipe = initialize_pipeline("text2img", device)
    
    # Get style object if a style name is provided
    style_obj = get_style(style)
    
    # Apply specific style to the prompt if provided
    styled_prompt = prompt
    # Improved negative prompt with more specific terms for better quality
    negative_prompt = "low quality, blurry, distorted, deformed, disfigured, bad anatomy, ugly, amateur, watermark, signature, text, cropped, low resolution, draft"
    
    # Higher quality defaults for inference
    inference_steps = 40 if device == "cuda" else 30  # More steps for better quality
    guidance_scale = 8.0  # Slightly higher guidance scale
    
    if style_obj:
        # Use the style object to format the prompt and get parameters
        styled_prompt = style_obj.get_prompt(prompt)
        negative_prompt = style_obj.negative_prompt
        inference_steps = max(style_obj.inference_steps, inference_steps)  # Use the higher value
        guidance_scale = style_obj.guidance_scale
        
        print(f"Using style: {style_obj.name}")
        print(f"Using styled prompt: {styled_prompt}")
    
    # Generate the image with improved parameters
    try:
        print(f"Generating with: steps={inference_steps}, guidance={guidance_scale}, dimensions={width}x{height}")
        
        # Set seed for reproducibility but allow for variation
        generator = torch.Generator(device=device).manual_seed(int(time.time()) % 10000)
        
        # Better dimension handling for CPU
        if device == "cpu":
            # Scale down dimensions for CPU processing, but maintain at least 640px
            max_cpu_dim = 640  # Higher quality CPU generation
            scale_factor = min(1.0, max_cpu_dim / max(width, height))
            gen_width = int(width * scale_factor)
            gen_height = int(height * scale_factor)
            print(f"Adjusted dimensions for CPU: {gen_width}x{gen_height}")
        else:
            gen_width, gen_height = width, height
        
        result = pipe(
            prompt=styled_prompt,
            negative_prompt=negative_prompt,
            width=gen_width,
            height=gen_height,
            num_inference_steps=inference_steps,
            guidance_scale=guidance_scale,
            generator=generator
        )

        # Check if result contains the 'images' attribute
        if not hasattr(result, "images") or not result.images:
            print("Error: No images generated.")
            return None
            
        image = result.images[0]  # Get the generated image
        
        # Resize back to requested dimensions if we scaled down
        if device == "cpu" and (gen_width != width or gen_height != height):
            image = image.resize((width, height), Image.LANCZOS)
        
        # Apply style-specific post-processing
        if style == "pixel_art" or (style_obj and style_obj.name == "pixel_art"):
            # Apply optimized pixel art processing
            image = pixelate_image(image, pixel_size=10)  # Less pixelation for better detail
            image = reduce_colors(image, num_colors=32)  # More colors for better detail
            image = enhance_image_quality(image, enhancement_level=1.4, contrast=1.3, saturation=1.4)
        else:
            # Apply enhanced image quality for all other styles
            image = enhance_image_quality(image, enhancement_level=1.3, sharpness=1.4, contrast=1.25, saturation=1.3)

        # Specify the output folder and filename
        output_folder = "generated_images"
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

        # Generate a safe filename based on the prompt and timestamp
        timestamp = int(time.time())
        safe_prompt = "".join(c if c.isalnum() or c in [' ', '_'] else '_' for c in prompt[:20])
        output_path = os.path.join(output_folder, f"{safe_prompt}_{timestamp}.png")
        
        # Save with higher quality
        image.save(output_path, quality=95, optimize=True)

        # Convert the image to base64 to send as a response
        buffered = BytesIO()
        image.save(buffered, format="PNG", quality=95, optimize=True)
        img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")

        print(f"Image successfully saved to {output_path}")
        return img_str
        
    except Exception as e:
        print(f"Error generating image: {str(e)}")
        import traceback
        traceback.print_exc()
        return None

# Improved function to resize image based on hardware capabilities
def resize_for_processing(image, device="cpu"):
    """
    Resize image to dimensions appropriate for the hardware with better quality preservation
    
    Args:
        image (PIL.Image): Input image
        device (str): "cuda" or "cpu"
    
    Returns:
        PIL.Image: Possibly resized image
        float: Scale factor used (for scaling back later)
    """
    width, height = image.size
    # Higher maximum sizes for better quality
    max_size = 1024 if device == "cuda" else 768
    
    # If image is larger than max_size in either dimension, resize
    if width > max_size or height > max_size:
        scale_factor = min(max_size / width, max_size / height)
        new_width = int(width * scale_factor)
        new_height = int(height * scale_factor)
        # Use LANCZOS for best quality downsampling
        return image.resize((new_width, new_height), Image.LANCZOS), scale_factor
    
    # No resize needed
    return image, 1.0

# Optimized style application function with improved quality
def apply_style_to_image(image_path: str, style: str = None, instructions: str = None, prompt: str = None):
    """
    Apply a specific style to an uploaded image with enhanced quality.
    
    Args:
        image_path (str): Path to the uploaded image
        style (str): Style to apply (e.g., "ghibli", "anime", "realistic")
        instructions (str): Additional instructions for image processing
        prompt (str): Additional prompt to guide the style transfer
        
    Returns:
        str: Base64 encoded string of the styled image
    """
    # Check if CUDA is available for GPU acceleration
    device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"Using device: {device}")
    print(f"Applying style: {style}")
    
    try:
        # Check if the file exists
        if not os.path.isfile(image_path):
            print(f"Error: Image file not found: {image_path}")
            return None
        
        # Load the uploaded image
        init_image = Image.open(image_path).convert("RGB")
        
        # Print image details for debugging
        print(f"Original image size: {init_image.width}x{init_image.height}")
        
        # Pre-enhance the image slightly before processing for better results
        init_image = ImageEnhance.Contrast(init_image).enhance(1.15)
        init_image = ImageEnhance.Sharpness(init_image).enhance(1.15)
        
        # Resize image for processing if needed, with better quality preservation
        init_image, scale_factor = resize_for_processing(init_image, device)
        print(f"Processing at size: {init_image.width}x{init_image.height}")
        
        # Get style object if a style name is provided
        style_obj = get_style(style)
        
        # Special handling for pixel art style - purely PIL operations for better performance
        if style == "pixel_art" or (style_obj and style_obj.name == "pixel_art"):
            print("Applying pixel art style with specialized processing")
            
            # Start with enhancing the source image
            enhanced_image = enhance_image_quality(init_image, enhancement_level=1.3, 
                                                 contrast=1.3, saturation=1.4)
            
            # Apply improved pixel art transformation
            # First sharpen details
            enhanced_image = enhanced_image.filter(ImageFilter.SHARPEN)
            
            # Then pixelate with better parameters
            pixelated_image = pixelate_image(enhanced_image, pixel_size=10)
            
            # Use better color reduction with dithering for smoother transitions
            final_image = reduce_colors(pixelated_image, num_colors=32)
            
            # Final touch-ups
            final_image = enhance_image_quality(final_image, enhancement_level=1.4,
                                               contrast=1.3, saturation=1.4)
            
        else:
            # Only load the img2img pipeline if we need it
            img2img_pipeline = initialize_pipeline("img2img", device)
            
            # Improved parameters for img2img
            styled_prompt = prompt if prompt else "This image"
            negative_prompt = "low quality, blurry, distorted, deformed, disfigured, bad anatomy, ugly, watermark, signature, text"
            # Higher steps for better quality
            inference_steps = 40 if device == "cuda" else 30
            guidance_scale = 8.0
            strength = 0.70  # Higher strength for more transformation
            
            # Get parameters from style object if available
            if style_obj:
                if prompt:
                    styled_prompt = style_obj.get_prompt(prompt)
                else:
                    styled_prompt = style_obj.get_prompt("This image")
                    
                negative_prompt = style_obj.negative_prompt
                inference_steps = max(style_obj.inference_steps, inference_steps)
                guidance_scale = style_obj.guidance_scale
                strength = style_obj.img2img_strength
                
            # Additional instructions if provided
            if instructions:
                styled_prompt += f", {instructions}"
                
            print(f"Using img2img with prompt: {styled_prompt}")
            print(f"Using negative prompt: {negative_prompt}")
            print(f"Using inference steps: {inference_steps}")
            print(f"Using strength: {strength}")
            
            # Apply img2img transformation with enhanced parameters
            result = img2img_pipeline(
                prompt=styled_prompt,
                negative_prompt=negative_prompt,
                image=init_image,
                strength=strength,
                guidance_scale=guidance_scale,
                num_inference_steps=inference_steps,
                generator=torch.Generator(device=device).manual_seed(int(time.time()) % 10000)
            )
            
            final_image = result.images[0]
            
            # Apply enhanced post-processing
            final_image = enhance_image_quality(
                final_image, 
                enhancement_level=1.3, 
                sharpness=1.4, 
                contrast=1.25, 
                saturation=1.3
            )
        
        # Scale back to original size if we resized earlier, with high quality
        if scale_factor < 1.0:
            original_width, original_height = Image.open(image_path).size
            final_image = final_image.resize((original_width, original_height), Image.LANCZOS)
        
        # Save the result with higher quality settings
        output_folder = "generated_images"
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)
            
        # Generate a safe filename
        timestamp = int(time.time())
        style_name = style if style else "styled"
        output_path = os.path.join(output_folder, f"{style_name}_image_{timestamp}.png")
        final_image.save(output_path, quality=95, optimize=True)
        
        # Convert to base64 for response
        buffered = BytesIO()
        final_image.save(buffered, format="PNG", quality=95, optimize=True)
        img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")
        
        print(f"Styled image saved to {output_path}")
        
        # Clear GPU memory if available
        if device == "cuda":
            torch.cuda.empty_cache()
            
        return img_str
        
    except Exception as e:
        print(f"Error applying style to image: {str(e)}")
        import traceback
        traceback.print_exc()
        return None