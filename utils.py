"""
Author: Fabio Pöschko
Matr.Nr.: K11905017
Exercise 5
"""

import os, shutil

# i sometimes use this function to delete all elements in a folder, such that i keep my folders clean when doing
# some tests with different network architectures
def clear_folder(folder):
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))