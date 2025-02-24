# Run this file to install all necessary libraries for main.py

from subprocess import check_call
from sys import executable

packages = [
    "ultralytics",
    "pillow",
    "opencv-python"
]

def install_packages(packages):
    for package in packages:
        print(f"Instalando {package}...")
        check_call([executable, "-m", "pip", "install", package])

if __name__ == "__main__":
    install_packages(packages)