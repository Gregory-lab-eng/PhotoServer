from pathlib import Path
import uuid


ALLOWED_EXTENSIONS = ['.png', '.jpg', '.jpeg', '.gif']
MAX_FILE_SIZE = 50 * 1024 * 1024


def is_allowed_file(filename: Path) -> bool:
    """Checking extensions"""
    ext = filename.suffix.lower()
    return ext in ALLOWED_EXTENSIONS


def get_unique_name(filename: Path) -> str:
    ext = filename.suffix.lower()
    unique_name = f"{uuid.uuid4().hex}{ext}"
    print(f"New file name {unique_name}")
    return unique_name