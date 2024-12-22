import os
from metadata_manager import MetadataManager
from tkinter import messagebox

class IntegrityChecker:
    def __init__(self, backup_directory):
        self.backup_directory = backup_directory

    def check_backup_integrity(self):
        """Проверяет целостность всех файлов резервной копии."""
        try:
            metadata = MetadataManager.load_metadata_for_integrity(self.backup_directory)
            if not metadata["files"]:
                messagebox.showwarning("Предупреждение", "Метаданные отсутствуют или повреждены.")
                return

            corrupted_files = []
            for relative_path, file_info in metadata["files"].items():
                file_path = os.path.join(self.backup_directory, relative_path)
                if not os.path.exists(file_path):
                    corrupted_files.append((relative_path, "Файл отсутствует"))
                    continue

                file_hash = MetadataManager.calculate_file_hash(file_path)
                if file_hash != file_info.get("hash"):
                    corrupted_files.append((relative_path, "Хеш не совпадает"))

            if not corrupted_files:
                messagebox.showinfo("Успех", "Целостность файлов не нарушена.")
            else:
                error_message = "Обнаружены повреждения:\n" + "\n".join(
                    [f"{file}: {reason}" for file, reason in corrupted_files]
                )
                messagebox.showerror("Ошибка целостности", error_message)
        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка при проверке целостности: {e}")
