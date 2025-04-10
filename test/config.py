import os
import sys

if 'win' in sys.platform:  # Windows
    base_path = 'D:/Git/Application-Security'
    sys.path.append(base_path)
    sys.path.append(os.path.join(base_path, 'test'))
    sys.path.append(os.path.join(base_path, 'ftp'))