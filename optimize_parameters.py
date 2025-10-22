import cv2
import numpy as np
import os
import matplotlib.pyplot as plt
from cartoonizer import Cartoonizer

def optimize_parameters():
    """
    Test different parameter combinations to find optimal settings for cartoonization.
    """
    # Create cartoonizer instance
    cartoonizer = Cartoonizer()
    
    # Get list of images in dataset directory
    dataset_dir = 'dataset'
    image_files = [f for f in os.listdir(dataset_dir) if f.endswith(('.jpg', '.jpeg', '.png'))]
    
    # Create output directory
    output_dir = 'optimized_results'
    os.makedirs(output_dir, exist_ok=True)
    
    # Select a test image (using the first image in the dataset)
    test_image_path = os.path.join(dataset_dir, image_files[0])
    img = cv2.imread(test_image_path)
    
    # Parameter combinations to test
    bilateral_d_values = [5, 9, 13]
    bilateral_sigma_values = [50, 75, 100]
    edge_threshold_values = [(30, 100), (50, 150), (70, 200)]
    color_levels_values = [4, 8, 12]
    
    # Test different parameter combinations
    for d in bilateral_d_values:
        for sigma in bilateral_sigma_values:
            for edge_thresholds in edge_threshold_values:
                for color_levels in color_levels_values:
                    # Update parameters
                    cartoonizer.update_parameters(
                        bilateral_filter_d=d,
                        bilateral_sigma_color=sigma,
                        bilateral_sigma_space=sigma,
                        edge_threshold1=edge_thresholds[0],
                        edge_threshold2=edge_thresholds[1],
                        total_color_levels=color_levels
                    )
                    
                    # Apply cartoonization
                    cartoon = cartoonizer.cartoonize(img)
                    
                    # Save the result
                    param_str = f"d{d}_sigma{sigma}_edge{edge_thresholds[0]}_{edge_thresholds[1]}_colors{color_levels}"
                    output_path = os.path.join(output_dir, f"param_{param_str}.jpg")
                    cv2.imwrite(output_path, cartoon)
                    
                    print(f"Tested parameters: {param_str}")
    
    print("Parameter optimization completed. Results saved to 'optimized_results' directory.")

def test_all_images():
    """
    Test cartoonization on all images in the dataset with optimized parameters.
    """
    # Create cartoonizer instance with optimized parameters
    cartoonizer = Cartoonizer()
    cartoonizer.update_parameters(
        line_size=7,
        bilateral_filter_d=9,
        bilateral_sigma_color=75,
        bilateral_sigma_space=75,
        edge_threshold1=50,
        edge_threshold2=150,
        total_color_levels=8
    )
    
    # Get list of images in dataset directory
    dataset_dir = 'dataset'
    image_files = [f for f in os.listdir(dataset_dir) if f.endswith(('.jpg', '.jpeg', '.png'))]
    
    # Create output directory
    output_dir = 'final_results'
    os.makedirs(output_dir, exist_ok=True)
    
    # Process each image
    for image_file in image_files:
        # Read image
        image_path = os.path.join(dataset_dir, image_file)
        img = cv2.imread(image_path)
        
        # Apply cartoonization
        cartoon = cartoonizer.cartoonize(img)
        
        # Save the result
        output_path = os.path.join(output_dir, f"cartoon_{image_file}")
        cv2.imwrite(output_path, cartoon)
        
        # Create comparison image
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        cartoon_rgb = cv2.cvtColor(cartoon, cv2.COLOR_BGR2RGB)
        
        plt.figure(figsize=(12, 6))
        
        plt.subplot(1, 2, 1)
        plt.imshow(img_rgb)
        plt.title('Original Image')
        plt.axis('off')
        
        plt.subplot(1, 2, 2)
        plt.imshow(cartoon_rgb)
        plt.title('Cartoonized Image')
        plt.axis('off')
        
        plt.tight_layout()
        
        # Save the comparison
        comparison_path = os.path.join(output_dir, f"comparison_{image_file}")
        plt.savefig(comparison_path)
        plt.close()
        
        print(f"Processed {image_file} - Result saved to {output_path}")
    
    print("All images processed. Results saved to 'final_results' directory.")

if __name__ == "__main__":
    # Uncomment to run parameter optimization
    # optimize_parameters()
    
    # Test all images with optimized parameters
    test_all_images()
