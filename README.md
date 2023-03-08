# GitHub Repo Downloader
> The GitHub Repo Downloader is a `Python` GUI application designed to make it easy to download entire GitHub repositories
> as ZIP archives. The application utilizes the `GitHub API` to fetch the contents of the repository and download them to
> a specified location on the user's computer. The application is built using the Python standard library, as well as
> the `tkinter` library for the GUI and the `requests` library for handling HTTP requests.
- - - -
## Feature List:
- Simple and intuitive GUI for entering the URL of the GitHub repository and selecting the download location.
- Option to browse for and select the download location using a file dialog.
- Option to set the download location to the current working directory with a single click.
- Progress bar that shows the download progress and estimated time remaining.
- Ability to download entire repositories, including all files and directories, in a single ZIP archive.
- Option to cancel the download at any time.
- Error handling for invalid URLs, network errors, and other exceptions that may occur during the download process.
- Success message upon completion of the download process.

## Sample Screenshots
![screenshot_1.png](Assets%2Fscreenshot_1.png)
![screenshot_2.png](Assets%2Fscreenshot_2.png)
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