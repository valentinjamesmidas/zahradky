"""Convert Blender catalog renders to small WebP cards. Requires Pillow."""
from pathlib import Path
from PIL import Image
ROOT=Path(__file__).resolve().parents[1]
out=ROOT/'public/images/options';out.mkdir(parents=True,exist_ok=True)
for p in (ROOT/'work/catalog-renders').glob('*.png'):
    Image.open(p).save(out/(p.stem+'.webp'),quality=82,method=6)
print('WebP catalog updated.')
