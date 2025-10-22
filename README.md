# Image-Cartoonization-Project
This project implements an image cartoonization application using classical digital image processing techniques. The application converts regular photographs into cartoon-style sketches using edge detection, bilateral filtering, and color quantization.
## Features
- Convert images to cartoon-style sketches
- Interactive GUI with real-time parameter adjustments
- Multiple cartoonization parameters for customization
- Support for various image formats
- Before/after comparison view
- Save functionality for processed images

## Files Included
- `cartoonizer.py`: Core implementation of cartoonization techniques
- `cartoon_gui.py`: Graphical user interface for the application
- `optimize_parameters.py`: Script for testing and optimizing parameters
- `Project_Report.pdf`: Comprehensive project documentation
- `dataset/`: Sample images for testing
- `final_results/`: Cartoonized output images

## Requirements
- Python 3.x
- OpenCV
- NumPy
- Matplotlib
- Pillow
- Tkinter

## Installation
```bash
pip install opencv-python numpy matplotlib pillow
```

## Usage
To run the GUI application:
```bash
python cartoon_gui.py
```

To test cartoonization with optimized parameters:
```bash
python optimize_parameters.py
```

## Techniques Used
1. **Edge Detection**: Identifies boundaries in the image
2. **Bilateral Filtering**: Smooths the image while preserving edges
3. **Color Quantization**: Reduces the number of colors for a cartoon effect

## Project Structure
- Core cartoonization algorithm in `Cartoonizer` class
- GUI implementation in `CartoonGUI` class
- Parameter optimization in separate utility script
- Comprehensive documentation in project report

## Customization
The application allows adjustment of various parameters:
- Edge thickness
- Smoothing level
- Color smoothing
- Spatial smoothing
- Edge detection thresholds
- Number of color levels

## License
This project is created for educational purposes as part of a Digital Image Processing Lab Project.

## Author
Ubaid Ullah
