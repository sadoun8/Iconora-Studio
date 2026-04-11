import importlib
import os
import sys

class PluginManager:
    """Plugin manager for Iconora Studio 3.0."""

    def __init__(self, plugins_dir="plugins"):
        self.plugins_dir = plugins_dir
        self.plugins = {}
        self.loaded_modules = {}

        # Add plugins directory to sys.path
        if self.plugins_dir not in sys.path:
            sys.path.append(self.plugins_dir)

        # Create plugins directory if it doesn't exist
        if not os.path.exists(self.plugins_dir):
            os.makedirs(self.plugins_dir)

    def load_all_plugins(self):
        """Loads all available plugins from the plugins directory."""
        if not os.path.exists(self.plugins_dir): return
        
        for file in os.listdir(self.plugins_dir):
            if file.endswith(".py") and file != "__init__.py":
                plugin_name = file[:-3]
                try:
                    module = importlib.import_module(plugin_name)
                    # Check if the plugin has an 'apply' function
                    if hasattr(module, "apply"):
                        self.plugins[plugin_name] = module
                        self.loaded_modules[plugin_name] = module
                        print(f"Loaded plugin: {plugin_name}")
                    else:
                        print(f"Skipping plugin: {plugin_name} (No 'apply' function found)")
                except Exception as e:
                    print(f"Failed to load plugin {plugin_name}: {e}")

    def apply_plugin(self, name, image, *args, **kwargs):
        """Applies a specific plugin to the given image."""
        if name in self.plugins:
            return self.plugins[name].apply(image, *args, **kwargs)
        else:
            print(f"Plugin {name} not found or not loaded")
            return image

    def list_plugins(self):
        """Returns a list of loaded plugin names."""
        return list(self.plugins.keys())
