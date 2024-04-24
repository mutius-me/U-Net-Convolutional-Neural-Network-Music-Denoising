import os

def rename_files_and_dirs(root_dir):
    # Walk through all directories and files in root_dir
    for root, dirs, files in os.walk(root_dir, topdown=False):
        # Rename files containing '_mixed'
        for file in files:
            if '_mixed' in file:
                new_file = file.replace('_mixed', '')
                old_path = os.path.join(root, file)
                new_path = os.path.join(root, new_file)
                os.rename(old_path, new_path)
                print(f'Renamed {old_path} to {new_path}')

        # Rename directories containing '_mixed'
        for dir in dirs:
            if '_mixed' in dir:
                new_dir = dir.replace('_mixed', '')
                old_path = os.path.join(root, dir)
                new_path = os.path.join(root, new_dir)
                os.rename(old_path, new_path)
                print(f'Renamed {old_path} to {new_path}')

# Specify the directory you want to clean up
root_directory = '/Users/Leo/Developer/Local/senior-project/dataset/iteration-1/data/mixed/spectrogram-256-frames'
rename_files_and_dirs(root_directory)
