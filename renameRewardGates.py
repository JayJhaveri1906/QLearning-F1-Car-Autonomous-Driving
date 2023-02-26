# Renames the masks to be in sequential order
## credit to chatGpt with a bit modifications,, just gave it the following prompt xd:"
### write me a python script to rename multiple files by number in a folder
### based on the time they were created in sequential order.

import os

map = "Zandvoort"

folder_path = "assets/rewardGates/"+str(map)  # replace with your folder path
file_extension = ".png"  # replace with your file extension

# get list of files in folder
files = os.listdir(folder_path)

# filter files by extension
files = [f for f in files if f.endswith(file_extension)]

# sort files by creation time
files.sort(key=lambda x: -os.path.getctime(os.path.join(folder_path, x)))

# rename files sequentially
for i, f in enumerate(files):
    new_name = f"RG{i}{file_extension}"
    os.rename(os.path.join(folder_path, f), os.path.join(folder_path, new_name))