from PIL import Image, ImageDraw, ImageFont

class Layer:
    """Base Layer class for the design engine."""

    def __init__(self, type, obj, x=0, y=0, width=100, height=100, opacity=1.0, rotation=0):
        self.type = type
        self.obj = obj # PIL Image, text string, or shape info
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.opacity = opacity
        self.rotation = rotation
        self.visible = True
        self.locked = False

    def render(self, canvas_img):
        """Renders the layer onto the given PIL Image canvas."""
        if not self.visible: return canvas_img
        
        # Implementation of layer rendering based on type
        # Text, Icon, Shape, Image layers
        # Using PIL.Image.alpha_composite
        pass

class LayerManager:
    """Manages multiple design layers with Z-index support."""

    def __init__(self):
        self.layers = []
        self.active_layer = None

    def add_layer(self, layer):
        """Adds a new layer to the top of the stack."""
        self.layers.append(layer)
        self.active_layer = layer

    def move_layer(self, index, x, y):
        """Updates the position of a specific layer."""
        if 0 <= index < len(self.layers):
            self.layers[index].x = x
            self.layers[index].y = y

    def remove_layer(self, index):
        """Removes a layer from the stack."""
        if 0 <= index < len(self.layers):
            del self.layers[index]

    def render_all(self, width, height):
        """Renders all layers into a final composition image."""
        base = Image.new("RGBA", (width, height), (255, 255, 255, 0))
        for layer in self.layers:
            base = layer.render(base)
        return base
