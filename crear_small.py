from pathlib import Path
from PIL import Image

CARPETA = Path("app/static/img")
MAX_SIZE = 64

ESCUDOS = [
    "san_jose_sf.webp",
    "salvador_sf.webp",
    "parquesol_sf1.webp",
    "pucela_sf.webp",
    "galvan_sf.webp",
    "cplv_sf.webp",
    "aliados_sf.webp",
    "vall_sala_sf.webp",
    "aula_sf.webp",
    "cbc_sf.webp",
    "pucela_basket_sf.webp",
    "reco_fs.webp",
    "valla_voley_sf.webp",
    "vrac_sf.webp",
]

creadas = 0

for nombre in ESCUDOS:
    archivo = CARPETA / nombre

    if not archivo.exists():
        print(f"NO ENCONTRADO: {nombre}")
        continue

    nombre_small = archivo.with_name(
        f"{archivo.stem}-small.webp"
    )

    try:
        with Image.open(archivo) as img:
            img = img.convert("RGBA")

            img.thumbnail(
                (MAX_SIZE, MAX_SIZE),
                Image.Resampling.LANCZOS
            )

            img.save(
                nombre_small,
                "WEBP",
                quality=90,
                method=6
            )

            print(
                f"OK: {nombre} -> {nombre_small.name} "
                f"({img.width}x{img.height})"
            )

            creadas += 1

    except Exception as e:
        print(f"ERROR: {nombre}: {e}")

print()
print(f"Versiones small creadas: {creadas}")
