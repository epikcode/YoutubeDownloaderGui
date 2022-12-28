import tkinter as tk
from tkinter import ttk
import tkinter.filedialog as fd
import youtube_dl
import ctypes
import os
import sys

def isAdmin():
    try:
        # Checks if user is admin
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

window = tk.Tk()
window.title("YouTube Downloader")
window.geometry("500x500")

def downloadVideo():
    # Gets the url
    url = urlEntry.get()

    # Gets the metadata for the video
    ydlOpts = {'simulate': True}
    with youtube_dl.YoutubeDL(ydlOpts) as ydl:
        info = ydl.extract_info(url, download=False)

    # Gets the title
    title = info['title']

    # Generetes a valid filename
    filename = youtube_dl.utils.sanitize_filename(title)

    # Destination path + filename + .mp4
    destination = os.path.join(destinationEntry.get(), filename + ".mp4")

    # Downloads the video
    ydlOpts = {
        'outtmpl': destination,
        'progress_hooks': [progressHook]
    }
    with youtube_dl.YoutubeDL(ydlOpts) as ydl:
        ydl.download([url])

    # Shows a message when the download is complete
    messageLabel['text'] = "Download complete!"

    # Exit button
    finishedButton = tk.Button(text="Finished", command=sys.exit)

    finishedButton.pack()

def progressHook(d):
    if d['status'] == 'downloading':
        # Calculate the percentage complete
        percentComplete = d['downloaded_bytes'] / d['total_bytes'] * 100

        # Update the progress bar
        progressBar['value'] = percentComplete

        # Update the estimated time label
        eta = d['eta']
        minutes, seconds = divmod(int(eta), 60)
        estimatedTimeLabel['text'] = f"{minutes}:{seconds:02d}"
    elif d['status'] == 'finished':
        # Update the progress bar
        progressBar['value'] = 100

        # Show a message when the download is complete
        messageLabel['text'] = "Download complete!"

def browse():
    # Asks user for file directory
    folder = fd.askdirectory()

    # Clear the destination entry widget
    destinationEntry.delete(0, tk.END)

    # Insert the selected folder into the destination entry widget
    destinationEntry.insert(0, folder)

urlLabel = tk.Label(text="Enter the URL of the YouTube video:")
urlEntry = tk.Entry(width=50)
destinationLabel = tk.Label(text="Destination folder:")
destinationEntry = tk.Entry(width=50)
browseButton = tk.Button(text="Browse", command=browse)
downloadButton = tk.Button(text="Download", command=downloadVideo)
progressBar = tk.ttk.Progressbar(
    orient="horizontal", length=400, mode="determinate")
estimatedTimeLabel = tk.Label(text="")
messageLabel = tk.Label(text="")

# Place the widgets in the window
urlLabel.pack()
urlEntry.pack()
destinationLabel.pack()
destinationEntry.pack()
browseButton.pack()
downloadButton.pack()
progressBar.pack()
estimatedTimeLabel.pack()
messageLabel.pack()

def main():
    if isAdmin():
        # Program is running with administrator privileges
        window.mainloop()
    else:
        # Program is not running with administrator privileges
        ctypes.windll.shell32.ShellExecuteW(
            None, "runas", sys.executable, " ".join(sys.argv), None, 1)


if __name__ == "__main__":
    main()
