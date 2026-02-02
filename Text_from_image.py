#!/usr/bin/env python3

import cv2
import numpy as np
import pytesseract
import os
import sys
from pathlib import Path
from PIL import Image

# Check if Tesseract is installed locally
try:
    # For Windows, you need to set the tesseract path
    if os.name == 'nt':
        # Common installation paths for Tesseract on Windows
        tesseract_paths = [
            r'C:\Program Files\Tesseract-OCR\tesseract.exe',
            r'C:\Program Files (x86)\Tesseract-OCR\tesseract.exe',
            r'D:\CodeFile\intro-to-programming-1-python\numpy_exp1\tesseract\tesseract.exe'
        ]
        for path in tesseract_paths:
            if os.path.exists(path):
                pytesseract.pytesseract.tesseract_cmd = path
                break
        else:
            print("ERROR: Tesseract not found. Please install Tesseract OCR:")
            print("1. Download from: https://github.com/UB-Mannheim/tesseract/wiki")
            print("2. Add Tesseract to PATH or update the path in this script")
            sys.exit(1)
    
    # For Linux/Mac, tesseract should be in PATH if installed
    # Test if tesseract is accessible
    pytesseract.get_tesseract_version()
    
except Exception as e:
    print(f"Tesseract Error: {e}")
    print("\nPlease install Tesseract OCR:")
    print("Ubuntu/Debian: sudo apt-get install tesseract-ocr")
    print("Mac: brew install tesseract")
    print("Windows: Download installer from above link")
    sys.exit(1)


class TextExtractor:
    def __init__(self, image_folder="text_image"):
        """
        Initialize the text extractor with image folder path
        """
        self.image_folder = Path(image_folder)
        
        if not self.image_folder.exists():
            print(f"Error: Folder '{image_folder}' not found!")
            print(f"Current directory: {Path.cwd()}")
            print(f"Looking for: {self.image_folder.absolute()}")
            sys.exit(1)
    
    def preprocess_image(self, image_path):
        """
        Preprocess image to improve OCR accuracy
        """
        # Read image
        img = cv2.imread(str(image_path))
        if img is None:
            raise ValueError(f"Cannot read image: {image_path}")
        
        # Convert to grayscale
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
        # Apply thresholding to get binary image
        _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        
        # Denoise using median blur
        denoised = cv2.medianBlur(thresh, 3)
        
        # Optional: Dilate to make text thicker
        kernel = np.ones((1, 1), np.uint8)
        dilated = cv2.dilate(denoised, kernel, iterations=1)
        
        return dilated
    
    def extract_text(self, image_path, preprocess=True):
        """
        Extract text from a single image
        """
        try:
            if preprocess:
                # Use preprocessed image
                processed_img = self.preprocess_image(image_path)
                text = pytesseract.image_to_string(processed_img, lang='eng')
            else:
                # Use original image
                text = pytesseract.image_to_string(Image.open(image_path), lang='eng')
            
            return text.strip()
        
        except Exception as e:
            print(f"Error processing {image_path}: {e}")
            return ""
    
    def extract_all_text(self, output_file="extracted_text.txt"):
        """
        Extract text from all images in the folder
        """
        # Supported image formats
        image_extensions = {'.png', '.jpg', '.jpeg', '.bmp', '.tiff', '.tif', '.gif', '.webp'}
        
        # Find all image files
        image_files = []
        for ext in image_extensions:
            image_files.extend(self.image_folder.glob(f'*{ext}'))
            image_files.extend(self.image_folder.glob(f'*{ext.upper()}'))
        
        if not image_files:
            print(f"No images found in {self.image_folder}")
            return
        
        print(f"Found {len(image_files)} image(s)")
        print("-" * 50)
        
        all_text = []
        
        for img_file in image_files:
            print(f"Processing: {img_file.name}")
            
            # Try with preprocessing first
            text = self.extract_text(img_file, preprocess=True)
            
            if not text or len(text.strip()) < 3:
                # If preprocessing gives poor results, try without preprocessing
                print("  Preprocessing gave poor results, trying without preprocessing...")
                text = self.extract_text(img_file, preprocess=False)
            
            if text:
                all_text.append(f"\n{'='*60}\n")
                all_text.append(f"File: {img_file.name}\n")
                all_text.append(f"{'='*60}\n\n")
                all_text.append(text)
                all_text.append("\n")
                
                # Also print to console
                print(f"Extracted text from {img_file.name}:\n{text[:200]}...\n")
            else:
                print(f"No text found in {img_file.name}\n")
        
        # Save all extracted text to file
        if all_text:
            with open(output_file, 'w', encoding='utf-8') as f:
                f.writelines(all_text)
            print(f"\nAll extracted text saved to: {output_file}")
        
        return all_text
    
    def batch_process(self, output_dir="extracted_texts"):
        """
        Process each image separately and save individual text files
        """
        output_path = Path(output_dir)
        output_path.mkdir(exist_ok=True)
        
        image_extensions = {'.png', '.jpg', '.jpeg', '.bmp', '.tiff', '.tif', '.gif', '.webp'}
        image_files = []
        
        for ext in image_extensions:
            image_files.extend(self.image_folder.glob(f'*{ext}'))
            image_files.extend(self.image_folder.glob(f'*{ext.upper()}'))
        
        for img_file in image_files:
            print(f"Processing: {img_file.name}")
            
            # Try different preprocessing strategies
            text = self.extract_text(img_file, preprocess=True)
            
            if not text or len(text.strip()) < 3:
                text = self.extract_text(img_file, preprocess=False)
            
            # Save individual file
            output_file = output_path / f"{img_file.stem}.txt"
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(text)
            
            print(f"  Saved to: {output_file}")
        
        print(f"\nIndividual text files saved in: {output_dir}/")


def main():
    """
    Main function to run the text extraction
    """
    print("=" * 60)
    print("LOCAL TEXT EXTRACTION FROM IMAGES")
    print("=" * 60)
    print("This tool extracts text from images using Tesseract OCR")
    print("No internet connection required!\n")
    
    # Initialize extractor
    extractor = TextExtractor("text_image")
    
    # Ask user for processing mode
    print("Select processing mode:")
    print("1. Extract all text to single file")
    print("2. Process each image separately")
    print("3. Extract text from specific image")
    
    try:
        choice = input("\nEnter choice (1-3): ").strip()
        
        if choice == "1":
            output_name = input("Enter output filename [default: extracted_text.txt]: ").strip()
            if not output_name:
                output_name = "extracted_text.txt"
            extractor.extract_all_text(output_file=output_name)
        
        elif choice == "2":
            extractor.batch_process()
        
        elif choice == "3":
            # List available images
            image_extensions = {'.png', '.jpg', '.jpeg', '.bmp', '.tiff', '.tif', '.gif', '.webp'}
            images = []
            for ext in image_extensions:
                images.extend(Path("text_image").glob(f"*{ext}"))
                images.extend(Path("text_image").glob(f"*{ext.upper()}"))
            
            if not images:
                print("No images found in text_image folder!")
                return
            
            print("\nAvailable images:")
            for i, img in enumerate(images, 1):
                print(f"{i}. {img.name}")
            
            try:
                img_choice = int(input("\nSelect image number: ")) - 1
                if 0 <= img_choice < len(images):
                    text = extractor.extract_text(images[img_choice], preprocess=True)
                    if not text:
                        text = extractor.extract_text(images[img_choice], preprocess=False)
                    
                    print(f"\n{'='*60}")
                    print(f"Extracted Text from {images[img_choice].name}:")
                    print(f"{'='*60}\n")
                    print(text)
                    
                    # Save to file
                    save = input("\nSave to file? (y/n): ").lower().strip()
                    if save == 'y':
                        filename = f"extracted_{images[img_choice].stem}.txt"
                        with open(filename, 'w', encoding='utf-8') as f:
                            f.write(text)
                        print(f"Text saved to {filename}")
                else:
                    print("Invalid selection!")
            except ValueError:
                print("Please enter a valid number!")
        
        else:
            print("Invalid choice. Using default mode (single file)...")
            extractor.extract_all_text()
    
    except KeyboardInterrupt:
        print("\n\nProcess interrupted by user.")
    except Exception as e:
        print(f"\nError: {e}")
    
    print("\n" + "=" * 60)
    print("Text extraction complete!")
    print("=" * 60)


if __name__ == "__main__":
    main()