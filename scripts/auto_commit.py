import random
from datetime import datetime

file_path = "assets/example.py"  # Update to your target file

with open(file_path, "a") as f:
    random_line = f"# Auto-commit: {random.randint(1000, 9999)} at {datetime.now()}"
    f.write(f"\n{random_line}")
