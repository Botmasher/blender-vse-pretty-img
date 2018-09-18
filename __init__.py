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

def register():
    bpy.types.SEQUENCER_MT_add.append(ui.menu_add)
    register_class(ui.PrettyImageOperator)
    register_class(ui.PrettyImageHandler)

def unregister():
    unregister_class(ui.PrettyImageHandler)
    unregister_class(ui.PrettyImageOperator)
    bpy.types.SEQUENCER_MT_add.remove(ui.menu_add)

if __name__ == '__main__':
    register()
