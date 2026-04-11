"""
Iconora Studio - Phase 2: SVG Converter
Converts raster images to vector SVG format with advanced tracing.
"""

import os
from pathlib import Path
from PIL import Image, ImageFilter, ImageOps
import base64
from io import BytesIO

try:
    from skimage import measure
    import numpy as np
    HAS_SKIMAGE = True
except ImportError:
    HAS_SKIMAGE = False
    print("Warning: scikit-image or numpy not found. SVG tracing will be disabled.")

class SVGConverter:
    """Convert raster images to vector SVG formats"""

    def __init__(self, image_path):
        """Initialize with image path"""
        self.image_path = image_path
        self.image = None
        self.load_image()

    def load_image(self):
        """Load image and prepare for processing"""
        try:
            self.image = Image.open(self.image_path)
            if self.image.mode != 'RGBA':
                self.image = self.image.convert('RGBA')
            return True
        except Exception as e:
            raise Exception(f"Failed to load image: {str(e)}")

    def convert_to_svg(self, output_path, embed_image=False, trace=True, threshold=128, 
                       simplify=False, tolerance=1.5, fill_color="black", bg_transparent=True):
        """Perform conversion with optimized tracing for crisp vectors"""
        try:
            import svgwrite
            width, height = self.image.size
            dwg = svgwrite.Drawing(output_path, size=(width, height), profile='tiny')

            if not bg_transparent and not trace:
                # If background is not transparent and we are only embedding, 
                # we might want to add a white background rect first
                dwg.add(dwg.rect(insert=(0, 0), size=(width, height), fill="white"))

            if trace:
                if HAS_SKIMAGE:
                    # PRE-PROCESSING for crisp tracing
                    # 1. Convert to Grayscale
                    gray = self.image.convert('L')

                    # 2. Add slight blur to reduce noise
                    gray = gray.filter(ImageFilter.GaussianBlur(0.5))

                    # 3. Apply threshold manually
                    gray = gray.point(lambda p: 255 if p > threshold else 0)

                    img_array = np.array(gray)

                    # Find contours
                    contours = measure.find_contours(img_array, 0.5)

                    if not contours and not embed_image:
                        embed_image = True

                    # Draw paths
                    for contour in contours:
                        if simplify:
                            contour = measure.approximate_polygon(contour, tolerance)

                        # Simplified path generation
                        path_data = "M"
                        for i, point in enumerate(contour):
                            y, x = point
                            if i == 0:
                                path_data += f" {x},{y}"
                            else:
                                path_data += f" L {x},{y}"
                        path_data += " Z"
                        dwg.add(dwg.path(d=path_data, fill=fill_color, stroke="none"))
                else:
                    if not embed_image:
                        raise Exception("Tracing requires scikit-image and numpy. Please use 'Embed' option.")

            if embed_image:
                # Get base64 representation
                buffered = BytesIO()
                
                # If not bg_transparent, we might want to paste onto white first if it has alpha
                export_img = self.image
                if not bg_transparent and self.image.mode == 'RGBA':
                    export_img = Image.new("RGB", self.image.size, (255, 255, 255))
                    export_img.paste(self.image, mask=self.image.getchannel('A'))

                # Save to buffer
                fmt = "PNG" if bg_transparent else "JPEG"
                export_img.save(buffered, format=fmt)
                img_str = base64.b64encode(buffered.getvalue()).decode()

                dwg.add(dwg.image(
                    href=f"data:image/{fmt.lower()};base64,{img_str}",
                    insert=(0, 0),
                    size=(width, height)
                ))

            dwg.save()
            return output_path

        except Exception as e:
            raise Exception(f"SVG Conversion failed: {str(e)}")
