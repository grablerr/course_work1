import os
import shutil
from datetime import datetime
from tkinter import messagebox
from metadata_manager import MetadataManager

class BackupManager:
    def __init__(self, source_directory, target_directory, backup_type="full"):
        self.source_directory = source_directory
        self.target_directory = target_directory
        self.backup_type = backup_type

    def create_backup_folder(self):
        try:
            timestamp = datetime.now().strftime("%d-%m-%Y %H-%M")
            folder_name = f"Backup_{self.backup_type}_{timestamp}"
            backup_dir = os.path.join(self.target_directory, folder_name)
            os.makedirs(backup_dir, exist_ok=True)
            return backup_dir
        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка при создании папки: {e}")
            return None

    def copy_file(self, src, dest):
        try:
            os.makedirs(os.path.dirname(dest), exist_ok=True)
            shutil.copy2(src, dest)
        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка при копировании файла {src}: {e}")

    def full_backup(self):
        if not self.source_directory:
            messagebox.showerror("Ошибка", "Исходная директория не выбрана.")
            return
        if not self.target_directory:
            messagebox.showerror("Ошибка", "Целевая директория не выбрана.")
            return

        try:
            backup_dir = self.create_backup_folder()
            if not backup_dir:
                return
            metadata = {"last_full_backup": datetime.now().isoformat(), "files": {}}
            for root, _, files in os.walk(self.source_directory):
                for file in files:
                    src_path = os.path.join(root, file)
                    relative_path = os.path.relpath(src_path, self.source_directory)
                    dest_path = os.path.join(backup_dir, relative_path)
                    self.copy_file(src_path, dest_path)
                    metadata["files"][relative_path] = os.path.getmtime(src_path)
            MetadataManager.save_metadata(backup_dir, metadata)
            messagebox.showinfo("Успех", "Полное резервное копирование выполнено успешно.")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка при выполнении полного резервного копирования: {e}")

    def incremental_backup(self):
        if not self.source_directory:
            messagebox.showerror("Ошибка", "Исходная директория не выбрана.")
            return
        if not self.target_directory:
            messagebox.showerror("Ошибка", "Целевая директория не выбрана.")
            return

        try:
            backup_dir = self.create_backup_folder()
            if not backup_dir:
                return
            metadata = MetadataManager.load_metadata(self.target_directory)
            if not metadata["last_full_backup"]:
                messagebox.showwarning("Предупреждение", "Не найдено полное резервное копирование.")
                return
            for root, _, files in os.walk(self.source_directory):
                for file in files:
                    src_path = os.path.join(root, file)
                    relative_path = os.path.relpath(src_path, self.source_directory)
                    dest_path = os.path.join(backup_dir, relative_path)
                    file_mtime = os.path.getmtime(src_path)
                    if relative_path not in metadata["files"] or metadata["files"][relative_path] < file_mtime:
                        self.copy_file(src_path, dest_path)
                        metadata["files"][relative_path] = file_mtime
            metadata["last_diff_backup"] = datetime.now().isoformat()
            MetadataManager.save_metadata(self.target_directory, metadata)
            messagebox.showinfo("Успех", "Инкрементальное резервное копирование выполнено успешно.")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка при выполнении инкрементального резервного копирования: {e}")

    def differential_backup(self):
        if not self.source_directory:
            messagebox.showerror("Ошибка", "Исходная директория не выбрана.")
            return
        if not self.target_directory:
            messagebox.showerror("Ошибка", "Целевая директория не выбрана.")
            return

        try:
            backup_dir = self.create_backup_folder()
            if not backup_dir:
                return
            metadata = MetadataManager.load_metadata(self.target_directory)
            if not metadata["last_full_backup"]:
                messagebox.showwarning("Предупреждение", "Не найдено полное резервное копирование.")
                return
            full_backup_time = datetime.fromisoformat(metadata["last_full_backup"])
            for root, _, files in os.walk(self.source_directory):
                for file in files:
                    src_path = os.path.join(root, file)
                    relative_path = os.path.relpath(src_path, self.source_directory)
                    dest_path = os.path.join(backup_dir, relative_path)
                    file_mtime = os.path.getmtime(src_path)
                    if file_mtime > full_backup_time.timestamp():
                        self.copy_file(src_path, dest_path)
            metadata["last_diff_backup"] = datetime.now().isoformat()
            MetadataManager.save_metadata(self.target_directory, metadata)
            messagebox.showinfo("Успех", "Дифференциальное резервное копирование выполнено успешно.")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка при выполнении дифференциального резервного копирования: {e}")
