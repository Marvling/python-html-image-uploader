# %%
from bs4 import BeautifulSoup
import sys
import os
import shutil
import ntpath

# Changing the working directory to script location
os.chdir(os.path.dirname(os.path.abspath(__file__)))


def check_locations(dir_local, dir_web,):

    # Setting the directories for the web and local folders
    list_dir_local = os.listdir(dir_local)
    list_dir_web = os.listdir(dir_web)

    # Finding the missing files
    files_missing = [i for i in list_dir_local if i not in list_dir_web]

    # Cheking if the directories are synced, generating a list for location of missing files
    if len(files_missing) != 0:
        dir_files_missing = [dir_local + "/" + i for i in files_missing]

        print('The missing files were:')
        print(*files_missing, sep='\n')
        print("\n")
        print('dir_files_missing was generated')
        print("\n")

        return dir_files_missing
    else:
        dir_files_missing = []
        print('The directories were synced')
        print('dir_files_missing is empty')
        print("\n")
        return dir_files_missing


def filename_from_path(path):
    head, tail = ntpath.split(path)
    return tail or ntpath.basename(head)


def move_missing(dir_local, dir_web, dir_files_missing):

    if len(dir_files_missing) != 0:

        dir_files_moved = []

        for i in dir_files_missing:
            # Move new files to dir_web
            shutil.copy2(i, dir_web)

            # Append new directories to dir_files_moved
            file_name = filename_from_path(i)
            file_dir = f"{dir_web}/{file_name}"
            dir_files_moved.append(file_dir)

        print("succesfully moved the following files")
        print(*dir_files_missing, sep='\n')
        print("\n")
        print("new file paths are")
        print(*dir_files_moved, sep='\n')
        print("\n")
        return dir_files_moved

    else:
        print('Missing files list was empty' + "\n" + "No files were moved")
        return

def generate_tags_to_insert(list_of_files_to_add, html_file):

    tags_to_insert = []

    if list_of_files_to_add != None:

        print(f"{len(list_of_files_to_add)} tags will be generated")

        for i in list_of_files_to_add:
            soup = BeautifulSoup(html_file, 'html.parser')
            # Preapare the tag to be inserted
            tag_new_a = soup.new_tag("a", attrs={
                    'class': 'column', 'href': i, 'data-lightbox': "20_10"})
            
            tag_new_img = soup.new_tag("img", attrs={
                    'class': 'column', 'src': i, 'alt': ""})
            
            tag_new_a.insert(1, tag_new_img)

            # Append the new tags to list
            tags_to_insert.append(tag_new_a)

        print(f"sucessfully generated {len(tags_to_insert)} tags")
        return tags_to_insert

    else:
        print('0 tags generated')
        return tags_to_insert

def generate_new_html(html_file, number_of_images_on_page, number_of_images_on_div, list_of_tags_to_add):
    
    # Finding the number of divs on the webpage
    number_of_divs = number_of_images_on_page / number_of_images_on_div
    number_of_divs = int(number_of_divs)

    # Creating a master list to itterate
    tags = list_of_tags_to_add


    # Finding the divs for insertion
    with open(html_file, "r") as file:
        soup = BeautifulSoup(file, 'html.parser')    

        while len(tags) != 0:
            # Find empty div
            for i in range(1, int(number_of_divs - (len(tags)/number_of_images_on_div)) +1):
                tag_checked = soup.find(id=f"row-{i}")

                # Set the div as tag_empty
                if len(tag_checked.contents) < 3:
                    tag_empty = tag_checked
            
                    # Insert the a tag into the empty tag
                    print("\n")
                    print(tag_empty)
                    tag_empty.insert(0,tags[-1])

                    # Remove the inserted tag from the master list
                    tags.pop()
    
    return soup

# Local directory
dir_local = "../../testdir"

# Web directory
dir_web = "Assets/Dailies"

# HTML file
html_file = "dailies.html"

images_page = 33
images_div = 3

dir_files_missing = check_locations(dir_local=dir_local, dir_web=dir_web)
dir_files_moved = move_missing(dir_local=dir_local, dir_web=dir_web, dir_files_missing=dir_files_missing)
tags_to_add = generate_tags_to_insert(dir_files_moved, html_file)

new_html = generate_new_html(html_file, images_page, images_div, tags_to_add)

print(new_html.prettify())
# %%