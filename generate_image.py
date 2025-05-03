from diffusers import StableDiffusionPipeline
import torch

# Load the model from your local path
model_path = "./model/stable-diffusion-v1-5"

pipe = StableDiffusionPipeline.from_pretrained(
    model_path,
    torch_dtype=torch.float32,  # Using CPU
    safety_checker=None,        # Optional: Disable safety checker
)

pipe.to("cpu")  # Force CPU mode

# Your first prompt
prompt = "a magical forest with glowing mushrooms and fireflies, fantasy art"
image = pipe(prompt).images[0]

# Save the result
image.save("output.png")
print("Image saved as output.png")
