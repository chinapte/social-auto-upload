from pathlib import Path

from social_upload.conf import BASE_DIR

Path(BASE_DIR / "cookies").mkdir(exist_ok=True)