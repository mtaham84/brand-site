from PIL import Image
from io import BytesIO
from django.core.files.base import ContentFile
import os


def optimize_image(image_field, max_width=1400, quality=80):
    if not image_field:
        return image_field

    img = Image.open(image_field)

    if img.mode != "RGB":
        img = img.convert("RGB")

    if img.width > max_width:
        ratio = max_width / img.width
        img = img.resize(
            (max_width, int(img.height * ratio)),
            Image.Resampling.LANCZOS
        )

    output = BytesIO()

    img.save(
        output,
        format="WEBP",
        quality=quality,
        optimize=True
    )

    filename = os.path.splitext(image_field.name)[0] + ".webp"

    return ContentFile(output.getvalue(), name=filename)