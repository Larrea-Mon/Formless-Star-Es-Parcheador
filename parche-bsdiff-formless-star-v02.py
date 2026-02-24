import sys
import os
import hashlib
import bsdiff4

# config
PATCH_FILE_EXE = "parche-exe.bsdiff"
PATCH_FILE_RPG = "parche-rpg.bsdiff"

TARGET_EXE = "Formless Star.exe"
TARGET_RPG = "Formless Star.rpg"

EXPECTED_MD5_EXE = 'f147ad7a179b30e0efefe791657d98d3'  
EXPECTED_MD5_RPG = '9356294b3008bde688a8b860ea77cc99'

def resource_path(relative_name: str) -> str:
    base = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base, relative_name)

def md5_of_file(path):
    h = hashlib.md5()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()

def main():
    patch_exe_path = resource_path(PATCH_FILE_EXE)
    patch_rpg_path = resource_path(PATCH_FILE_RPG)

    if not os.path.isfile(patch_exe_path):
        print(f"Error: No se encontró el parche {PATCH_FILE_EXE}")
        print(f"Buscado en: {patch_exe_path}")
        input("Presiona Enter para salir.")
        sys.exit(1)

    if not os.path.isfile(patch_rpg_path):
        print(f"Error: No se encontró el parche {PATCH_FILE_RPG}")
        print(f"Buscado en: {patch_rpg_path}")
        input("Presiona Enter para salir.")
        sys.exit(1)

    # Paso 1 localizar los archivos del juego (estos sí van en la carpeta actual del usuario)
    if not os.path.isfile(TARGET_EXE):
        print(f"Error: No se encontró el archivo {TARGET_EXE}")
        input(f"Coloca este parcheador en la misma carpeta que {TARGET_EXE} y vuelve a ejecutarlo. Presiona Enter para salir.")
        sys.exit(1)

    if not os.path.isfile(TARGET_RPG):
        print(f"Error: No se encontró el archivo {TARGET_RPG}")
        input(f"Coloca este parcheador en la misma carpeta que {TARGET_RPG} y vuelve a ejecutarlo. Presiona Enter para salir.")
        sys.exit(1)

    # Paso 2 verificar los archivos
    print(f"Verificando integridad de {TARGET_EXE}...")
    exe_hash = md5_of_file(TARGET_EXE)
    #print(f"MD5: {exe_hash}")
    if exe_hash != EXPECTED_MD5_EXE:
        print(f"Error: El archivo {TARGET_EXE} no coincide con el esperado. Asegúrate de tener la versión correcta del juego.")
        input("Presiona Enter para salir.")
        sys.exit(1)  # you were missing exit here

    print(f"Verificando integridad de {TARGET_RPG}...")
    rpg_hash = md5_of_file(TARGET_RPG)
    #print(f"MD5: {rpg_hash}")
    if rpg_hash != EXPECTED_MD5_RPG:
        print(f"Error: El archivo {TARGET_RPG} no coincide con el esperado. Asegúrate de tener la versión correcta del juego.")
        input("Presiona Enter para salir.")
        sys.exit(1)

    # Paso 3 aplicar el bsdiff
    try:
        bsdiff4.file_patch_inplace(TARGET_EXE, patch_exe_path)
        bsdiff4.file_patch_inplace(TARGET_RPG, patch_rpg_path)
    except Exception as e:
        print(f"Error al aplicar el parche: {e}")
        input("Presiona Enter para salir.")
        sys.exit(1)

    print("Parche aplicado exitosamente.")
    input("Presiona Enter para salir.")

if __name__ == "__main__":
    main()