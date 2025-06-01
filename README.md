# MuseMind 🎨🧠

MuseMind is a Flask-based backend application that enables AI-driven image generation and style transfer using Stable Diffusion 1.5. It supports prompt-based image synthesis, custom style transfer via uploaded images, and pre-defined artistic styles, leveraging PyTorch and Diffusers for optimized generation.

---

## ⚙️ Features

* 🖼️ **Prompt-Based Image Generation**: Generate images from textual prompts using Stable Diffusion 1.5.
* 🎨 **Style Transfer**: Apply artistic styles to images, including custom styles via uploaded images.
* ⚡ **Optimized Performance**: Utilizes PyTorch and Diffusers for efficient image generation.
* 🧩 **Modular Design**: Easily extendable for additional features or integration with other applications.

---

## 🧠 Tech Stack

* **Backend**: Python (Flask)
* **Machine Learning**: PyTorch, Diffusers, Stable Diffusion 1.5
* **Image Processing**: OpenCV, PIL

---

## 📁 Modules

* `generate_image.py` – Handles image generation and style transfer logic.
* `requirements.txt` – Lists all Python dependencies.
* `styles/` – Contains pre-defined artistic styles.
* `output.png` – Sample output image.

---

## 🧪 Input

* **Text Prompts**: Describe the desired image to generate.
* **Style Images**: Upload images to extract and apply their artistic style.([Gist][1])

---

## 🚀 Goal

To provide a backend service capable of generating and transforming images through AI, facilitating creative applications such as art generation, design prototyping, and more.


