import io
import os
import time
import tkinter as tk
from tkinter import messagebox, filedialog, ttk
import zipfile

import requests
from tqdm import tqdm


class GitHubRepoDownloader(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.master.geometry("400x355")  # set the size of the window
        self.master.resizable(False, False)  # prevent the window from being resized
        self.master.title("GitHub Repo Downloader")  # set the title of the window
        self.pack(fill="both", expand=True)  # fill the entire window
        self.create_widgets()

    def create_widgets(self):
        self.url_label = tk.Label(self, text="Enter the URL of a GitHub repository:")
        self.url_label.pack(pady=(20, 0))

        self.url_entry = tk.Entry(self, width=60)
        self.url_entry.pack(ipady=10, pady=(0, 10))

        self.download_dir_label = tk.Label(self, text="Please select the directory to save the downloaded contents:")
        self.download_dir_label.pack(pady=(10, 0))

        self.download_dir_entry = tk.Entry(self, width=60)
        self.download_dir_entry.pack(ipady=10, pady=(0, 5))

        self.browse_button = tk.Button(self, text="Browse...", command=self.browse_for_directory, width=51)
        self.browse_button.pack()

        self.cwd_button = tk.Button(self, text="Set download location to current working directory",
                                    command=self.set_download_dir_to_cwd, width=51)
        self.cwd_button.pack(pady=(10, 0))

        self.progress_label = tk.Label(self, text="")
        self.progress_label.pack()

        self.progress_bar = ttk.Progressbar(self, orient="horizontal", length=365, mode="determinate")
        self.progress_bar.pack()

        self.download_button = tk.Button(self, text="Download", command=self.download_repository, width=51)
        self.download_button.pack(ipady=20, pady=10)

    def browse_for_directory(self):
        directory = tk.filedialog.askdirectory()
        if directory:
            self.directory = directory

    def download_directory(self, url, progress_bar=None):
        # Construct the URL for the GitHub API request
        api_url = url.replace("github.com", "api.github.com/repos") + "/contents"

        # Send a GET request to the GitHub API to get a list of all files and directories
        response = requests.get(api_url)

        # Check if the request was successful
        if response.status_code == 200:
            # Create a new ZIP archive in memory
            zip_file = io.BytesIO()

            # Create a ZipFile object for the new archive
            with zipfile.ZipFile(zip_file, "w") as zip_archive:
                # Iterate over each file and directory in the repository
                for item in tqdm(response.json(), desc='Downloading', unit='file', leave=False,
                                 disable=not progress_bar):

                    if progress_bar:
                        progress_bar.step(1)
                        self.update()

                    # Check if the item is a file
                    if item["type"] == "file":
                        # Get the URL for the raw file content
                        file_url = item["download_url"]

                        # Send a GET request to the file URL to download the file content
                        file_response = requests.get(file_url)

                        # Add the file content to the ZIP archive
                        zip_archive.writestr(item["path"], file_response.content)

                    # Check if the item is a directory
                    elif item["type"] == "dir":
                        # Get the URL for the contents of the directory
                        dir_url = item["url"]

                        # Call the function recursively to download the contents of the directory
                        self.download_directory(dir_url, progress_bar=progress_bar)

            # Seek to the beginning of the ZIP archive
            zip_file.seek(0)

            # Return the ZIP archive as a bytes object
            return zip_file.read()

        # Raise an exception if the request was not successful
        else:
            raise Exception("Failed to download directory: " + str(response.status_code))

    def set_download_dir_to_cwd(self):
        self.download_dir_entry.delete(0, tk.END)
        self.download_dir_entry.insert(0, os.getcwd())

    def download_repository(self):
        url = self.url_entry.get()
        try:
            self.progress_label.config(text="Downloading repository...")
            self.progress_bar.config(maximum=100, value=0)
            self.progress_bar.pack()
            data = self.download_directory(url, progress_bar=self.progress_bar)

        except Exception as e:
            tk.messagebox.showerror("Error", str(e))
            return

        finally:
            self.progress_label.config(text="")
            self.progress_bar.stop()
            self.progress_bar.pack_forget()
            if self.progress_bar['value'] < self.progress_bar['maximum']:
                # if the progress bar is not at maximum value, delay for 1 second
                time.sleep(0.5)

        filename = url.split("/")[-1] + ".zip"
        filepath = os.path.join(self.download_dir_entry.get(), filename)

        with open(filepath, "wb") as f:
            f.write(data)

        tk.messagebox.showinfo("Success", "The repository has been downloaded and saved to " + filepath)


if __name__ == "__main__":
    root = tk.Tk()
    app = GitHubRepoDownloader(master=root)
    app.mainloop()
