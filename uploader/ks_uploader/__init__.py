from pathlib import Path

from social_upload.conf import BASE_DIR

Path(BASE_DIR / "cookies" / "ks_uploader").mkdir(exist_ok=True)