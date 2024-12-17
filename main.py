from pystray import Icon
from tray_manager import create_icon_image, create_tray_menu

def main():
    icon = Icon("BackupApp", create_icon_image(), menu=create_tray_menu())
    icon.run()

if __name__ == "__main__":
    main()
