#!/usr/bin/env python3
"""
Setup script for ISDIP Python implementation
"""
import subprocess
import sys
import os

def install_requirements():
    """Install required packages"""
    requirements = [
        "numpy",
        "opencv-python", 
        "scikit-image",
        "Pillow"
    ]
    
    for package in requirements:
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])
            print(f"✓ Installed {package}")
        except subprocess.CalledProcessError:
            print(f"✗ Failed to install {package}")

def create_directories():
    """Create necessary directories"""
    dirs = ["../saliencymap", "../superpixels"]
    for d in dirs:
        os.makedirs(d, exist_ok=True)
        print(f"✓ Created directory {d}")

if __name__ == "__main__":
    print("Setting up ISDIP Python environment...")
    install_requirements()
    create_directories()
    print("Setup complete!")