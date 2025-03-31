import os
import subprocess
from datetime import datetime
from getpass import getpass

FOLDER_PATH = r'PATH'
OUTPUT_PATH = r'PATH'
SEVEN_ZIP_PATH = r'PATH'
OUTPUT_FILE_NAME = 'File.zip'

def git_sync(folder_path: str) -> None:
    """
    Syncs the specified folder with a local Git repository.
    """
    # Change to the specified directory
    os.chdir(folder_path)

    try:
        # Add all changes to the staging area
        subprocess.run(['git', 'add', '.'], check=True)

        now = str(datetime.now()).split('.')[0]

        # Commit the changes with a message
        subprocess.run(['git', 'commit', '-m', now], check=True)
    except subprocess.CalledProcessError as e:
        print(f'Looks like there was no changes to commit. Do you want to continue? (y/n): ')
        answer = input()
        if answer.lower() == 'y':
            print("Continuing...")
        else:
            print("Exiting...")
            quit()

def compress(folder_path: str, output_path: str) -> None:
    """
    Compresses and encrypts the specified folder into a zip file using 7zip.
    """
    # Checks if the output path exists, if not, asks the user wether to create it
    if not os.path.exists(output_path):
        create = input(f"The output path {output_path} does not exist. Do you want to create it? (y/n): ")
        if create.lower() == 'y':
            os.makedirs(output_path)
        else:
            print("Exiting...")
            quit()
    
    # Checks if the 7zip path exists
    if not os.path.exists(SEVEN_ZIP_PATH):
        print(f"The 7zip path {SEVEN_ZIP_PATH} does not exist. Please check the path, or if you don't have 7zip installed, please install it.")
        return
    
    # Get the password from the user
    password, confirm_password = '', ''
    while True:
        password = getpass("Enter the password to encrypt the zip file: ")
        confirm_password = getpass("Enter the password again to confirm: ")
        
        if password == confirm_password:
            break
        else:
            print("The passwords do not match. Please try again.")
    
    # Compress the folder using 7zip with password and AES-256 encryption
    subprocess.run([
        SEVEN_ZIP_PATH, 'a', '-tzip',  # Specify ZIP format
        '-p' + password,  # Set password
        '-mem=AES256',  # Use AES-256 encryption
        os.path.join(output_path, OUTPUT_FILE_NAME),  # Output ZIP file
        folder_path  # Folder to zip
        ], check=True)
    print(f"Folder {folder_path} compressed and encrypted successfully to {output_path}.")

if __name__ == "__main__":
    # Sync the folder with Git
    git_sync(FOLDER_PATH)

    # Compress the folder
    compress(FOLDER_PATH, OUTPUT_PATH)

    input("Press Enter to exit...")
