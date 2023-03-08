import io
import tkinter as tk
import tkinter.filedialog
import zipfile

import requests
from tqdm import tqdm


class GitHubRepoDownloader(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        self.url_label = tk.Label(self, text="Enter the URL of a GitHub repository:")
        self.url_label.pack()

        self.url_entry = tk.Entry(self, width=50)
        self.url_entry.pack()

        self.browse_button = tk.Button(self, text="Browse...", command=self.browse_for_directory)
        self.browse_button.pack()

        self.download_button = tk.Button(self, text="Download", command=self.download_repository)
        self.download_button.pack()

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

    def download_repository(self):
        url = self.url_entry.get()
        try:
            data = self.download_directory(url)
        except Exception as e:
            tk.messagebox.showerror("Error", str(e))
            return

        filename = url.split("/")[-1] + ".zip"
        if hasattr(self, "directory"):
            filepath = self.directory + "/" + filename
        else:
            filepath = tkinter.filedialog.asksaveasfilename(defaultextension=".zip", initialfile=filename)
            if not filepath:
                return

        with open(filepath, "wb") as f:
            f.write(data)

        tk.messagebox.showinfo("Success", "The repository has been downloaded and saved to " + filepath)


if __name__ == "__main__":
    root = tk.Tk()
    app = GitHubRepoDownloader(master=root)
    app.mainloop()
