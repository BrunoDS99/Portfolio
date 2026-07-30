# Watermarker Desktop Application

A desktop application built with **Python**, **Tkinter**, and **Pillow** that allows users to quickly add text or logo watermarks to images through a simple graphical interface.

This project was developed as part of my Python portfolio to demonstrate GUI development, image processing, project organization, and clean application structure.

---

## Features

* 🖼️ Open PNG and JPEG images
* ✍️ Add custom text watermarks
* 🖼️ Add logo watermarks
* 🎚️ Adjust watermark opacity
* 📏 Resize logo watermark
* 📍 Choose watermark position

  * Top Left
  * Top Right
  * Bottom Left
  * Bottom Right
* 👀 Live preview of the watermarked image
* 💾 Save the final image to any location

---

## Technologies

* Python 3
* Tkinter
* Pillow (PIL)

---

## Project Structure

```text
Project 4 - Watermarker/
│
├── assets/
│   ├── photo.jpg
│   ├── logo.png
│   └── ...
│
├── src/
│   ├── config.py
│   ├── gui.py
│   ├── image_utils.py
│   ├── watermark.py
│   └── window_config.py
│
├── tests/
│
├── app.py
├── requirements.txt
└── README.md
```

---

## Installation

Clone the repository:

```bash
git clone <repository-url>
```

Navigate into the project:

```bash
cd "Project 4 - Watermarker"
```

Create a virtual environment:

```bash
python -m venv .venv
```

Activate the virtual environment:

**Windows**

```bash
.venv\Scripts\activate
```

**macOS / Linux**

```bash
source .venv/bin/activate
```

Install the dependencies:

```bash
pip install -r requirements.txt
```

Run the application:

```bash
python app.py
```

---

## How to Use

1. Click **Open Image** and choose an image.
2. Select either **Text** or **Logo** watermark mode.
3. If using a logo, click **Upload Logo** and choose a PNG image.
4. Adjust the watermark settings:

   * Text
   * Font size
   * Opacity
   * Logo scale
   * Position
5. Click **Apply Watermark**.
6. Preview the result.
7. Click **Save Image** and choose where to save the finished image.

---

## Future Improvements

Potential enhancements include:

* Drag-and-drop image loading
* Batch watermarking
* Custom fonts
* Logo rotation
* Theme support (Light/Dark mode)
* Image zoom and pan
* Additional export formats

---

## Learning Objectives

This project demonstrates:

* Object-oriented programming
* Tkinter GUI development
* Image manipulation with Pillow
* File handling
* Project organization
* Modular application design
* Event-driven programming

---

## License

This project is intended for educational and portfolio purposes.
