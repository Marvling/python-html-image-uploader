# %%
from bs4 import BeautifulSoup
import sys
import os
import shutil

# Changing the working directory to script location
os.chdir(os.path.dirname(os.path.abspath(__file__)))


def check_locations(dir_local, dir_web, to_be_added=[]):

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

        return dir_files_missing
    else:
        dir_files_missing = []
        print('The directories were synced')
        print('dir_files_missing is empty')
        return dir_files_missing

def move_missing (dir_files_missing, dir_web):

    if len(dir_files_missing) != 0:
        
        # Move new files to dir_web
        for i in dir_files_missing:
            shutil.copy2(i, dir_web)

        print("succesfully moved the following files")
        print(*dir_files_missing, sep='\n')
    else:
        print('Missing files list was empty' + "\n" + "No files were moved")
        return
        
def generate_new_html (html_file):
    
    # Finding the divs for insertion
    with open("dailies_21_01.html", "r") as file:
            soup = BeautifulSoup(file, 'html.parser')

            # Find empty div
            for i in range(1, 12):
                tag_checked = soup.find(id=f"row-{i}")
                print("tag_checked = " + str(tag_checked))
                print("\n")
            
                if len(tag_checked.contents) < 3:
                    tag_empty = tag_checked

                    print("tag_empty = " + str(tag_empty))

# Local directory
dir_local = "../../testdir"
# Web directory
dir_web = "Assets/Dailies"
# List of directories of the files in the local directory that aren't in the web directory
dir_files_missing = []

dir_files_missing = check_locations(dir_local=dir_local, dir_web=dir_web)
move_missing(dir_files_missing=dir_files_missing, dir_web=dir_web)


# %%


# %%

# Insert the missing files in the empty tag
with open("dailies_21_01.html", "r") as file:
    soup = BeautifulSoup(file, 'html.parser')

    tag_existing = soup.find(id="row-1")
    print(len(tag_existing.contents))

    tag_new_a = soup.new_tag("a", attrs={
        'class': 'column', 'href': 'Assets/Dailies/20_10_29.jpg', 'data-lightbox': "20_10"})

    tag_new_img = soup.new_tag("img", attrs={
        'class': 'column', 'src': 'Assets/Dailies/20_10_29.jpg', 'alt': ""})

    # Insert the img into a
    tag_new_a.insert(1, tag_new_img)

    # Insert the img into the row
    tag_existing.insert(0, tag_new_a)
    print(len(tag_existing.contents))

# %%














