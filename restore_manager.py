import os
import shutil
from tkinter import messagebox


class RestoreManager:
    def __init__(self, target_directory, restore_directory):
        """
        :param target_directory: Директория с резервными копиями
        :param restore_directory: Директория для восстановления
        """
        self.target_directory = target_directory
        self.restore_directory = restore_directory

    def restore_from_full_backup(self):
        """Восстановление из последнего полного резервного копирования."""
        try:
            backups = self.get_backups("full")
            if not backups:
                messagebox.showwarning("Предупреждение", "Полные резервные копии не найдены.")
                return
            latest_full_backup = backups[-1]  # Последний по времени
            self.copy_backup_files(latest_full_backup)
            messagebox.showinfo("Успех", "Восстановление из полного резервного копирования завершено.")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка при восстановлении из полного резервного копирования: {e}")

    def restore_from_incremental_backup(self):
        """Восстановление из полного и всех инкрементальных копий."""
        try:
            full_backups = self.get_backups("full")
            if not full_backups:
                messagebox.showwarning("Предупреждение", "Полные резервные копии не найдены.")
                return
            latest_full_backup = full_backups[-1]
            self.copy_backup_files(latest_full_backup)

            incremental_backups = self.get_backups("incremental")
            for backup in incremental_backups:
                self.copy_backup_files(backup)

            messagebox.showinfo("Успех", "Восстановление из инкрементальных резервных копий завершено.")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка при восстановлении из инкрементальных резервных копий: {e}")

    def restore_from_differential_backup(self):
        """Восстановление из полного и последнего дифференциального копирования."""
        try:
            full_backups = self.get_backups("full")
            if not full_backups:
                messagebox.showwarning("Предупреждение", "Полные резервные копии не найдены.")
                return
            latest_full_backup = full_backups[-1]
            self.copy_backup_files(latest_full_backup)

            differential_backups = self.get_backups("differential")
            if differential_backups:
                latest_diff_backup = differential_backups[-1]
                self.copy_backup_files(latest_diff_backup)

            messagebox.showinfo("Успех", "Восстановление из дифференциального резервного копирования завершено.")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка при восстановлении из дифференциальных резервных копий: {e}")

    def get_backups(self, backup_type):
        """Получить список папок с резервными копиями определенного типа."""
        backups = []
        for folder in os.listdir(self.target_directory):
            if os.path.isdir(os.path.join(self.target_directory, folder)) and backup_type in folder:
                backups.append(os.path.join(self.target_directory, folder))
        backups.sort()
        return backups

    def copy_backup_files(self, backup_folder):
        """Копирование файлов из резервной копии в директорию восстановления."""
        for root, _, files in os.walk(backup_folder):
            for file in files:
                if file == "backup_metadata.json":  # Пропуск файла метаданных
                    continue
                src_path = os.path.join(root, file)
                relative_path = os.path.relpath(src_path, backup_folder)
                dest_path = os.path.join(self.restore_directory, relative_path)
                os.makedirs(os.path.dirname(dest_path), exist_ok=True)
                shutil.copy2(src_path, dest_path)
