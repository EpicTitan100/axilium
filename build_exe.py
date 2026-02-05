"""Build script for creating Axilium EXE."""

import PyInstaller.__main__
import os
import sys


def build_exe():
    """Build the Axilium executable."""
    # Get paths
    script_dir = os.path.dirname(os.path.abspath(__file__))
    main_script = os.path.join(script_dir, "run.py")
    icon_path = os.path.join(script_dir, "assets", "logo.ico")
    
    # PyInstaller arguments
    args = [
        main_script,
        "--name=Axilium",
        "--onefile",
        "--windowed",  # No console window
        "--clean",
        "--noconfirm",
        f"--distpath={os.path.join(script_dir, 'dist')}",
        f"--workpath={os.path.join(script_dir, 'build')}",
        "--add-data=data;data",  # Include data directory
        "--hidden-import=customtkinter",
        "--hidden-import=matplotlib",
        "--hidden-import=PIL",
        "--hidden-import=plyer",
        "--hidden-import=schedule",
    ]
    
    # Add icon if it exists
    if os.path.exists(icon_path):
        args.append(f"--icon={icon_path}")
    
    # Run PyInstaller
    PyInstaller.__main__.run(args)
    
    print("\n" + "="*50)
    print("Build complete!")
    print(f"Executable location: {os.path.join(script_dir, 'dist', 'Axilium.exe')}")
    print("="*50)


if __name__ == "__main__":
    build_exe()
