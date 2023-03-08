# GitHub Repo Downloader
> This is a simple `Python` script that allows you to download the contents of any public GitHub repository in the form 
of a ZIP archive. You can either run the script from the command line or use the included `tkinter` GUI to enter the 
repository URL and choose a save location for the ZIP archive.
- - - -
## Usage

### Clone Repo:
```shell
git clone https://github.com/1994nikunj/GitHub-Repo-Downloader.git
```

### GUI
To use the GUI, simply run the script with no command-line arguments:
```shell
python main.py
```

This will open a tkinter window where you can enter the repository URL and choose a save location for the ZIP archive.

## Features
#### 1. Directory save navigation:
- The script includes the feature that allows users to select a local directory where they would like to  save the 
downloaded repository ZIP archive. This feature is accessible via the 'Browse...' button in the GUI or by  passing a 
directory path as an optional command-line argument when running the script.

#### 2. Progress Bar
  - The GUI version of the script includes a progress bar that shows the current download progress as a percentage of the 
  total file size. This allows you to track the download progress and estimate how long it will take to complete. The 
  progress bar updates in real-time as each file is downloaded, so you can see the progress as it happens.

## Requirements
This script requires Python 3 and the following modules:
- requests
- zipfile
- io
- tkinter

You can install these modules using pip:

Note that `tkinter` is included in the standard library for most Python installations and does not need to be installed 
separately. However, on some systems, you may need to install the separate `python3-tk` package to use tkinter.

## Inspiration
This project was inspired by the website https://download-directory.github.io/.