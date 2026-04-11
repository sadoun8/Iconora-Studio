import xml.etree.ElementTree as ET
import os

class SVGEditor:
    """Professional SVG Editor for Iconora Studio 3.0."""

    def __init__(self):
        self.tree = None
        self.root = None
        self.current_path = None

    def load(self, path):
        """Loads an SVG file from the given path."""
        if not os.path.exists(path):
            raise FileNotFoundError(f"SVG file not found at: {path}")
        
        self.current_path = path
        try:
            self.tree = ET.parse(path)
            self.root = self.tree.getroot()
            return True
        except ET.ParseError as e:
            print(f"Failed to parse SVG: {e}")
            return False

    def change_color(self, old_color, new_color):
        """Replaces an old color with a new one across all elements."""
        if not self.root: return
        
        for elem in self.root.iter():
            # Check fill/stroke attributes
            for attr in ["fill", "stroke"]:
                if elem.attrib.get(attr) == old_color:
                    elem.attrib[attr] = new_color
            
            # Check style attribute
            style = elem.attrib.get("style", "")
            if old_color in style:
                elem.attrib["style"] = style.replace(old_color, new_color)

    def set_stroke_width(self, width):
        """Updates the stroke width for all applicable elements."""
        if not self.root: return
        for elem in self.root.iter():
            if "stroke" in elem.attrib or "stroke-width" in elem.attrib:
                elem.attrib["stroke-width"] = str(width)

    def save(self, path=None):
        """Saves the modified SVG to a file."""
        if not self.tree: return
        save_path = path or self.current_path
        if not save_path:
            raise ValueError("No save path provided")
            
        self.tree.write(save_path, encoding="utf-8", xml_declaration=True)
        return save_path

    def get_xml_string(self):
        """Returns the current SVG as a string."""
        if not self.tree: return ""
        return ET.tostring(self.root, encoding="unicode")
