import os
import sys


app_path = os.path.dirname(os.path.dirname(__file__))
print(app_path)

sys.path.append(app_path)