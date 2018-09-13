import bpy
from bpy.props import *
from bpy_extras.io_utils import ImportHelper
from .pretty_img import load_scale_img

# UI menu properties
PrettyImageProperties = {
    'alpha': BoolProperty(name="Transparency", description="Use alpha blend on image transform", default=True),
    'scale': FloatProperty(name="Scale", description="Transform scale to apply to fitted image", default=1.0),
    'length': IntProperty(name="Strip length", description="Frame duration of imported images", default=10)
}

class PrettyImagePanel (bpy.types.Panel):
    # Blender UI label, name, placement
    bl_label = "Pretty Image Loader"
    bl_idname = 'strip.pretty_image_loader'
    bl_space_type = 'SEQUENCE_EDITOR'
    bl_region_type = 'UI'
    def draw (self, context):

        # TODO do not show if inspecting a single strip
        sequencer = bpy.context.scene.sequence_editor
        #if sequencer.active_strip: return

        row = self.layout.row()
        row.operator("strip.add_pretty", text="Add Pretty Image")

class PrettyImageOperator (bpy.types.Operator):
    # Blender UI label, id and description
    bl_label = "Pretty Image Operator"
    bl_idname = 'strip.add_pretty'
    bl_description = "Add a new image with alpha, transform strip and proper dimensions."
    def execute (self, context):
        bpy.context.scene.sequence_editor_create()  # verify vse is valid in scene
        load_scale_img ("MY-ASDF-PATH.png")
        return {'FINISHED'}
    # import settings
    filepath = StringProperty (name='File Path')
    files = CollectionProperty(name='File Names', type=bpy.types.OperatorFileListElement)
    directory = StringProperty(maxlen=1024, subtype='DIR_PATH',options={'HIDDEN'})
    filter_image = BoolProperty(default=True, options={'HIDDEN'})
    filter_folder = BoolProperty(default=True, options={'HIDDEN'})
    # image loading/formatting
    set_alpha = PrettyImageProperties['alpha']
    img_scale = PrettyImageProperties['scale']
    length = PrettyImageProperties['length']

    def store_files (self, files):
        img_filenames = []
        for f in files:
            img_filenames.append (f.name)
        return img_filenames

    def execute (self, ctx):
        print("\n\nRestarting PRETTY IMG LOADER...")
        img_filenames = self.store_files(self.files)
        img_path = self.directory
        for filename in img_filenames:
            load_scale_img(filename, "{0}{1}".format(img_path, filename), scale=self.img_scale, length=self.length, alpha=self.set_alpha)
        return {'FINISHED'}

    def invoke (self, context, event):
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}
