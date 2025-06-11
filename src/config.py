import os
# This file contains the configuration for the task manager, including the data file path.
DATA_FILE = os.environ.get("DATA_FILE", "tasks.json")
