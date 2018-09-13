import bpy
import os
import inspect
from bpy.utils import register_class, unregister_class
from . import ui

bl_info = {
    "name": "Pretty Image Loader",
    "description": "Load prettier images with transparency and original image dimensions.",
    "author": "Joshua R",
    "version": (1, 0, 0),
    "blender": (2, 79, 0),
    "location": "Sequencer > Strip Properties",
    "tracker_url": "https://github.com/Botmasher/blender-vse-customizations/issues",
    "wiki_url": "",
    "support": "COMMUNITY",
    "category": "VSE"
}

def register_modules(modules, unregister=False):
    for module in modules:
        for member in inspect.getmembers(module, inspect.isclass):
            memberClass = member[1]
            try:
                registration = unregister_class(memberClass) if unregister else register_class(memberClass)
            except RuntimeError:
                print("Failed to load module member class {0}. Skipping for now.".format(memberClass))
    return

def register():
	register_modules([ui])

def unregister():
	register_modules(reversed([ui]), unregister=True)

if __name__ == '__main__':
    register()
