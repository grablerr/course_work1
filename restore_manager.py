import os
import shutil
from datetime import datetime
from tkinter import messagebox
import re

class RestoreManager:
    def __init__(self, target_directory, restore_directory):
        """
        :param target_directory: Директория с резервными копиями
        :param restore_directory: Директория для восстановления
        """
        self.target_directory = target_directory
        self.restore_directory = restore_directory

    def auto_restore(self):
        """Автоматическое восстановление данных в зависимости от доступных резервных копий."""
        try:
            # Получаем резервные копии разных типов
            full_backups = self.get_backups("full")
            incremental_backups = self.get_backups("incremental")
            differential_backups = self.get_backups("differential")

            # Проверка наличия полного резервного копирования
            if not full_backups:
                messagebox.showwarning("Предупреждение",
                                       "Полные резервные копии не найдены.")
                return

            # Восстанавливаем из последнего полного резервного копирования
            latest_full_backup = full_backups[-1]
            self.copy_backup_files(latest_full_backup)
            full_date = self.extract_date_from_backup(latest_full_backup)

            # Применяем последнюю дифференциальную копию (если есть)
            if differential_backups:
                latest_diff_backup = differential_backups[-1]
                diff_date = self.extract_date_from_backup(latest_diff_backup)
                if diff_date > full_date:
                    self.copy_backup_files(latest_diff_backup)
                    full_date = diff_date  # ОБНОВЛЯЕМ ДАТУ после применения дифференциальной копии

            # Применяем все инкрементальные копии по порядку
            if incremental_backups:
                incremental_backups.sort(
                    key=self.extract_date_from_backup)  # Сортируем по дате

                for backup in incremental_backups:
                    incr_date = self.extract_date_from_backup(backup)
                    print(
                        f"Обработка инкрементальной копии: {backup}, Дата: {incr_date}")
                    if incr_date > full_date:  # Применяем только если новее последней даты
                        self.copy_backup_files(backup)
                        full_date = incr_date  # ОБНОВЛЯЕМ ДАТУ после каждой инкрементальной копии

            messagebox.showinfo("Успех",
                                "Автоматическое восстановление завершено.")
        except Exception as e:
            messagebox.showerror("Ошибка",
                                 f"Ошибка при автоматическом восстановлении данных: {e}")

    def get_backups(self, backup_type):
        """Получить список папок с резервными копиями определенного типа."""
        backups = []
        for folder in os.listdir(self.target_directory):
            folder_path = os.path.join(self.target_directory, folder)
            if os.path.isdir(folder_path) and backup_type in folder:
                backups.append(folder_path)
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

    def extract_date_from_backup(self, backup_path):
        """Извлекает дату из имени резервной копии."""
        match = re.search(r"(\d{2}-\d{2}-\d{4} \d{2}-\d{2})", backup_path)
        if match:
            return datetime.strptime(match.group(1), "%d-%m-%Y %H-%M")
        return datetime.min  # Если дата не найдена, возвращаем минимальное значение
