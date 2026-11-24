"""Development helpers for the esign module."""

from io import BytesIO

from django.utils import timezone
from PIL import Image, ImageDraw


def example_stamp_data(file, user, group) -> dict:
    """Example visible stamp (`data` of `SignatureBackend.stamp`).

    Draws a round stamp with the group name. A host app returns the stamp
    image of the municipality instead, e.g. from its configuration.
    """
    size = 300
    image = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)
    color = (30, 110, 60, 255)
    draw.ellipse((10, 10, size - 10, size - 10), outline=color, width=12)
    draw.ellipse((40, 40, size - 40, size - 40), outline=color, width=4)
    draw.text(
        (size / 2, size / 2),
        group or "Alexandria",
        fill=color,
        anchor="mm",
        font_size=36,
    )

    output = BytesIO()
    image.save(output, format="PNG")
    return {
        "image": output.getvalue(),
        "text": timezone.localdate().strftime("%d.%m.%Y"),
    }
