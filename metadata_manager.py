import hashlib
import os
import json
from tkinter import messagebox

class MetadataManager:
    @staticmethod
    def get_metadata_file(target_dir):
        return os.path.join(target_dir, "backup_metadata.json")

    @staticmethod
    def load_metadata(target_dir):
        try:
            metadata_file = MetadataManager.get_metadata_file(target_dir)
            if os.path.exists(metadata_file):
                with open(metadata_file, "r", encoding="utf-8") as file:
                    return json.load(file)
            return {"last_full_backup": None, "last_diff_backup": None, "files": {}}
        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка при загрузке метаданных: {e}")
            return {"last_full_backup": None, "last_diff_backup": None, "files": {}}

    @staticmethod
    def save_metadata(target_dir, metadata):
        try:
            metadata_file = MetadataManager.get_metadata_file(target_dir)
            temp_metadata_file = metadata_file + ".tmp"
            # Сохраняем в временный файл
            with open(temp_metadata_file, "w", encoding="utf-8") as temp_file:
                json.dump(metadata, temp_file, indent=4, ensure_ascii=False)
            # Заменяем временный файл на основной
            os.replace(temp_metadata_file, metadata_file)
        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка при сохранении метаданных: {e}")

    @staticmethod
    def calculate_file_hash(file_path):
        """Рассчитывает SHA-256 хеш файла."""
        sha256_hash = hashlib.sha256()
        try:
            with open(file_path, "rb") as file:
                for byte_block in iter(lambda: file.read(4096), b""):
                    sha256_hash.update(byte_block)
            return sha256_hash.hexdigest()
        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка при расчете хеша файла {file_path}: {e}")
            return None
