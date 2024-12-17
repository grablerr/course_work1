from tkinter import filedialog, messagebox
from pystray import Icon, MenuItem, Menu
from PIL import Image, ImageDraw
from backup_manager import BackupManager
from restore_manager import RestoreManager
# Глобальные переменные
source_directory = None
target_directory = None
backup_type = "full"

def select_directory(title):
    try:
        root = filedialog.Tk()
        root.withdraw()
        directory = filedialog.askdirectory(title=title)
        root.destroy()
        return directory
    except Exception as e:
        messagebox.showerror("Ошибка", f"Не удалось выбрать директорию: {e}")
        return None

def create_icon_image():
    try:
        return Image.open("img.jpg")
    except FileNotFoundError:
        img = Image.new("RGB", (64, 64), color=(255, 255, 255))
        draw = ImageDraw.Draw(img)
        draw.text((10, 20), "BKP", fill=(0, 0, 0))  # Простой текст "BKP"
        return img

def set_source_directory(icon, item):
    global source_directory
    selected_dir = select_directory("Выбор исходной директории")
    if selected_dir:
        source_directory = selected_dir
        messagebox.showinfo("Успех", f"Исходная директория установлена: {source_directory}")

def set_target_directory(icon, item):
    global target_directory
    selected_dir = select_directory("Выбор целевой директории")
    if selected_dir:
        target_directory = selected_dir
        messagebox.showinfo("Успех", f"Целевая директория установлена: {target_directory}")

def set_backup_type_full(icon, item):
    global backup_type
    backup_type = "full"
    messagebox.showinfo("Успех", "Метод резервного копирования: Полное")

def set_backup_type_incremental(icon, item):
    global backup_type
    backup_type = "incremental"
    messagebox.showinfo("Успех", "Метод резервного копирования: Инкрементальное")

def set_backup_type_differential(icon, item):
    global backup_type
    backup_type = "differential"
    messagebox.showinfo("Успех", "Метод резервного копирования: Дифференциальное")

def force_backup(icon, item):
    global source_directory, target_directory, backup_type
    backup_manager = BackupManager(source_directory, target_directory, backup_type)
    if backup_type == "full":
        backup_manager.full_backup()
    elif backup_type == "incremental":
        backup_manager.incremental_backup()
    elif backup_type == "differential":
        backup_manager.differential_backup()

def restore_full_backup(icon, item):
    target_dir = select_directory("Выбор директории с резервными копиями")
    restore_dir = select_directory("Выбор директории для восстановления")
    if target_dir and restore_dir:
        manager = RestoreManager(target_dir, restore_dir)
        manager.restore_from_full_backup()

def restore_incremental_backup(icon, item):
    target_dir = select_directory("Выбор директории с резервными копиями")
    restore_dir = select_directory("Выбор директории для восстановления")
    if target_dir and restore_dir:
        manager = RestoreManager(target_dir, restore_dir)
        manager.restore_from_incremental_backup()

def restore_differential_backup(icon, item):
    target_dir = select_directory("Выбор директории с резервными копиями")
    restore_dir = select_directory("Выбор директории для восстановления")
    if target_dir and restore_dir:
        manager = RestoreManager(target_dir, restore_dir)
        manager.restore_from_differential_backup()


def quit_app(icon, item):
    icon.stop()

def create_tray_menu():
    return Menu(
        MenuItem("Выбор исходной директории", set_source_directory),
        MenuItem("Выбор целевой директории", set_target_directory),
        MenuItem("Выбор метода копирования", Menu(
            MenuItem("Полное", set_backup_type_full),
            MenuItem("Инкрементальное", set_backup_type_incremental),
            MenuItem("Дифференциальное", set_backup_type_differential)
        )),
        MenuItem("Принудительное копирование", force_backup),
        MenuItem("Восстановление данных", Menu(
            MenuItem("Полное восстановление", restore_full_backup),
            MenuItem("Инкрементальное восстановление", restore_incremental_backup),
            MenuItem("Дифференциальное восстановление", restore_differential_backup)
        )),
        MenuItem("Выход", quit_app)
    )

