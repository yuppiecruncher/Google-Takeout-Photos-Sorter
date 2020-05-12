import os, glob
import os.path
import shutil
import itertools, sys
from spinner import Spinner

parent_directory = input(
    "Enter the directory to copy from (Usually 'Google Photos'), or ctrl-c to quit without changes:"
)
if os.path.exists(parent_directory):
    print("Found your directory and the following subfolders:")

    """
    Generate a list of folders in the parent directory and print a list of the subfolders for the user.
    """
    sub_folders = [
        sF
        for sF in os.listdir(parent_directory)
        if os.path.isdir(os.path.join(parent_directory, sF))
    ]

    for folder in sub_folders:
        print(folder)

    new_parent_directory = input("Please enter a folder name for your moved files:\n")

    """
    Added spinning cursor because moving large amounts of images can take a while.
    """

    with Spinner("Moving images to '%s'... this could take a few minutes" % new_parent_directory):
        sub_folder_list = []
        images_count = 0
        file_ext = ('*.jpg', "*.JPG")

        for folder in sub_folders:
            #  get all the file types in the tuple
            images = []
            for ext in file_ext:
                images.extend(glob.iglob(os.path.join(parent_directory + "/" + folder, ext)))
            """
            For each folder name in sub_folders, split will split the string at the second occurence of "-" and [:2] will
            retrieve the first two elements in the list and finally "-".join() will rejoin the two elements with a "-"
            For custom named album folders, it skips the splits and joins and just uses the name of the folder.
            """
            if "-" in folder:
                folder_name = "-".join(folder.split("-", 2)[:2])
            else:
                folder_name = folder
            new_sub_folder = os.path.join(new_parent_directory, folder_name)
            if not os.path.exists(new_sub_folder):
                os.makedirs(new_sub_folder)
                sub_folder_list += [folder_name]
            for image in images:
                if os.path.isfile(image):
                    shutil.copy2(image, new_sub_folder)
                    images_count += 1
        print("\nCreated new folders in: '%s'" % new_parent_directory)

        for new_folders in sub_folder_list:
            print("'%s'" % new_folders)

        print("Whew! All done. Copied %s images total into the new folders." % images_count)

else:
    print("I couldn't find that directory. Please try again.")
