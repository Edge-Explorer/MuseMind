import os
import random
from flask import Flask, request, jsonify, render_template, send_from_directory, redirect, url_for
from werkzeug.utils import secure_filename
from .generate import generate_image, apply_style_to_image  # Using updated functions
import time
import uuid

app = Flask(__name__)

# Configure upload settings
UPLOAD_FOLDER = 'uploads'
GENERATED_FOLDER = 'generated_images'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max upload size

# Create necessary folders
for folder in ["static", "templates", UPLOAD_FOLDER, GENERATED_FOLDER]:
    if not os.path.exists(folder):
        os.makedirs(folder)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/")
def index():
    """Serve a simple HTML interface for image generation"""
    return render_template("index.html")

@app.route("/generate", methods=["POST"])
def generate():
    """Generate an image from a text prompt"""
    data = request.get_json()
    prompt = data.get("prompt")
    width = int(data.get("width", 512))
    height = int(data.get("height", 512))
    style = data.get("style")  # Get the style parameter
    
    # Validate input parameters
    if not prompt:
        return jsonify({
            "success": False,
            "message": "Prompt is required"
        }), 400
        
    # Limit dimensions to reasonable values
    width = min(max(width, 256), 1024)
    height = min(max(height, 256), 1024)

    # Log the received prompt
    print(f"Prompt received: {prompt}")
    print(f"Dimensions: {width}x{height}")
    if style:
        print(f"Style: {style}")

    # Track generation time
    start_time = time.time()
    
    # Generate the image with the style parameter
    generated_image = generate_image(prompt, width, height, style)
    
    # Calculate generation time
    generation_time = time.time() - start_time
    print(f"Image generation took {generation_time:.2f} seconds")
    
    if generated_image:
        return jsonify({
            "success": True,
            "message": "Image generated successfully",
            "image": generated_image,
            "generation_time": f"{generation_time:.2f}"
        })
    else:
        return jsonify({
            "success": False,
            "message": "Error generating image"
        }), 500

@app.route('/upload', methods=['POST'])
def upload_file():
    # Check if the post request has the file part
    if 'file' not in request.files:
        return jsonify({
            "success": False,
            "message": "No file part"
        }), 400
    
    file = request.files['file']
    
    # If the user does not select a file, browser submits an empty file without filename
    if file.filename == '':
        return jsonify({
            "success": False,
            "message": "No selected file"
        }), 400
    
    if file and allowed_file(file.filename):
        # Generate unique filename to avoid collisions
        filename = str(uuid.uuid4()) + '_' + secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        # Return the uploaded file path for later use
        return jsonify({
            "success": True,
            "message": "File successfully uploaded",
            "filename": filename,
            "filepath": filepath
        })
    else:
        return jsonify({
            "success": False,
            "message": "File type not allowed. Please upload PNG, JPG, JPEG, or GIF files."
        }), 400

@app.route('/apply_style', methods=['POST'])
def apply_style():
    data = request.get_json()
    filename = data.get('filename')  # This might be None if user is just using a prompt
    style = data.get('style')
    instructions = data.get('instructions')  # Get optional instructions
    prompt = data.get('prompt')  # Get optional prompt for additional guidance
    width = int(data.get("width", 512))
    height = int(data.get("height", 512))
    
    # If both filename and prompt are missing, we can't proceed
    if not filename and not prompt:
        return jsonify({
            "success": False,
            "message": "Either filename or prompt is required"
        }), 400
    
    # If prompt is provided but no filename, use the generate_image function directly
    if prompt and not filename:
        # Limit dimensions to reasonable values
        width = min(max(width, 256), 1024)
        height = min(max(height, 256), 1024)
        
        # Track generation time
        start_time = time.time()
        
        # Use generate_image instead of applying style to an existing image
        generated_image = generate_image(prompt, width, height, style)
        
        # Calculate generation time
        generation_time = time.time() - start_time
        print(f"Image generation took {generation_time:.2f} seconds")
        
        if generated_image:
            return jsonify({
                "success": True,
                "message": "Image generated successfully",
                "image": generated_image,
                "generation_time": f"{generation_time:.2f}"
            })
        else:
            return jsonify({
                "success": False,
                "message": "Error generating image"
            }), 500
    
    # If we have a filename, proceed with style application to an uploaded image
    if filename:
        # Full path to the uploaded image with improved path handling
        image_path = os.path.normpath(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        print(f"Looking for file: {filename}")
        print(f"Full path: {image_path}")
        print(f"File exists: {os.path.exists(image_path)}")
        
        # Check if file exists
        if not os.path.exists(image_path):
            # List files in the upload directory to debug
            files_in_dir = os.listdir(app.config['UPLOAD_FOLDER'])
            print(f"Files in upload directory: {files_in_dir}")
            return jsonify({
                "success": False,
                "message": f"File not found: {filename}"
            }), 404
        
        # Track processing time
        start_time = time.time()
        
        # Apply style to the uploaded image (pass instructions and prompt if provided)
        result = apply_style_to_image(image_path, style, instructions, prompt)
        
        # Calculate processing time
        processing_time = time.time() - start_time
        print(f"Style application took {processing_time:.2f} seconds")
        
        if result:
            return jsonify({
                "success": True,
                "message": "Style applied successfully",
                "image": result,
                "generation_time": f"{processing_time:.2f}"
            })
        else:
            return jsonify({
                "success": False,
                "message": "Error applying style to image"
            }), 500

@app.route("/generated_images/<path:filename>")
def serve_image(filename):
    """Serve generated images"""
    return send_from_directory(GENERATED_FOLDER, filename)

@app.route("/uploads/<path:filename>")
def serve_upload(filename):
    """Serve uploaded images"""
    return send_from_directory(UPLOAD_FOLDER, filename)

# List all uploaded files
@app.route("/uploads")
def list_uploads():
    """List all uploaded files"""
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
        
    files = []
    for filename in os.listdir(UPLOAD_FOLDER):
        if allowed_file(filename):
            file_path = os.path.join(UPLOAD_FOLDER, filename)
            file_info = {
                "filename": filename,
                "path": f"/uploads/{filename}",
                "size": os.path.getsize(file_path),
                "modified": os.path.getmtime(file_path)
            }
            files.append(file_info)
    
    # Sort files by modified time (newest first)
    files.sort(key=lambda x: x["modified"], reverse=True)
    
    return jsonify({
        "success": True,
        "files": files
    })

# Random image generation route
@app.route("/random_image", methods=["POST"])
def random_image():
    """Generate a random image based on predefined prompts"""
    data = request.get_json() or {}
    width = int(data.get("width", 512))
    height = int(data.get("height", 512))
    
    # Limit dimensions to reasonable values
    width = min(max(width, 256), 1024)
    height = min(max(height, 256), 1024)
    
    # Predefined list of prompts for random generation
    prompts = [
        "A peaceful mountain landscape at sunset",
        "A futuristic cyberpunk city at night with neon lights",
        "An underwater scene with colorful coral reef and fish",
        "A fantasy castle in the clouds",
        "A cozy cottage in a forest clearing",
        "A tropical beach paradise with palm trees",
        "A space station orbiting a distant planet",
        "An ancient temple hidden in the jungle",
        "A steampunk airship floating in the sky",
        "A winter wonderland with snow-covered trees",
        "A magical fairy garden with glowing mushrooms",
        "A medieval village market scene",
        "A desert oasis with camels and palm trees",
        "A rustic farm with fields of wheat at golden hour",
        "A bustling city street in the rain"
    ]
    
    # Predefined list of styles for random selection
    styles = [
        "realistic", "anime", "ghibli", "oil_painting", 
        "watercolor", "pixel_art", "cyberpunk", "fantasy"
    ]
    
    # Randomly select a prompt and style
    prompt = random.choice(prompts)
    style = random.choice(styles)
    
    print(f"Random prompt: {prompt}")
    print(f"Random style: {style}")
    print(f"Dimensions: {width}x{height}")
    
    # Track generation time
    start_time = time.time()
    
    # Generate the image
    generated_image = generate_image(prompt, width, height, style)
    
    # Calculate generation time
    generation_time = time.time() - start_time
    print(f"Random image generation took {generation_time:.2f} seconds")
    
    if generated_image:
        return jsonify({
            "success": True,
            "message": "Random image generated successfully",
            "image": generated_image,
            "prompt": prompt,
            "style": style,
            "generation_time": f"{generation_time:.2f}"
        })
    else:
        return jsonify({
            "success": False,
            "message": "Error generating random image"
        }), 500

if __name__ == "__main__":
    print("Starting AI Image Generator server...")
    app.run(debug=True, host='0.0.0.0', port=5000)