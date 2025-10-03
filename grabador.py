import os
import time
from datetime import datetime

def main():
    print("🎯 MODO PRÁCTICA SEGURO")
    print("=======================")
    print("1. Este programa NO necesita instalaciones")
    print("2. Escribe en ESTA ventana")
    print("3. Presiona Enter 3 veces para terminar")
    print("4. Se creará automaticamente practica_segura.txt")
    print("=======================\n")
    
    texto_completo = ""
    linea_numero = 1
    
    print("EMPIEZA A ESCRIBIR (ojos cerrados):")
    print("------------------------------------")
    
    while True:
        try:
            # Mostrar número de línea
            print(f"Línea {linea_numero}: ", end="", flush=True)
            
            # Leer input
            linea = input()
            
            # Si presiona Enter vacío 3 veces, terminar
            if linea == "":
                vacios_consecutivos = texto_completo.count('\n\n\n')
                if vacios_consecutivos >= 2:
                    break
                texto_completo += "\n"
            else:
                texto_completo += linea + "\n"
                linea_numero += 1
                
        except KeyboardInterrupt:
            print("\n\n⚠️  Interrumpido por el usuario")
            break
    
    # Procesar resultado
    os.system('cls')
    print("🎯 RESULTADO FINAL")
    print("==================")
    print(texto_completo)
    print("==================")
    
    # Guardar SIEMPRE
    nombre_archivo = "practica_segura.txt"
    with open(nombre_archivo, 'w', encoding='utf-8') as f:
        f.write("=== PRÁCTICA DE MECANOGRAFÍA - MODO SEGURO ===\n")
        f.write(f"Fecha: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n")
        f.write(f"Total líneas: {linea_numero}\n")
        f.write("=" * 50 + "\n\n")
        f.write(texto_completo)
        f.write("\n" + "=" * 50 + "\n")
        f.write(f"Caracteres totales: {len(texto_completo)}\n")
    
    print(f"💾 ARCHIVO CREADO: {nombre_archivo}")
    print(f"📊 Caracteres: {len(texto_completo)}")
    print(f"📍 Ubicación: {os.path.abspath(nombre_archivo)}")
    
    # Abrir el archivo automáticamente
    try:
        os.startfile(nombre_archivo)
        print("📖 Archivo abierto automáticamente")
    except:
        print("⚠️  Abre manualmente el archivo")
    
    input("\nPresiona Enter para salir...")

if __name__ == "__main__":
    main()