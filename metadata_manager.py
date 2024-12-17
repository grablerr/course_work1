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
            with open(metadata_file, "w", encoding="utf-8") as file:
                json.dump(metadata, file, indent=4, ensure_ascii=False)
        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка при сохранении метаданных: {e}")
