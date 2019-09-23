import bpy
from bpy.props import BoolProperty, FloatProperty, IntProperty, CollectionProperty, StringProperty
from bpy_extras.io_utils import ImportHelper

# UI menu properties
class PrettyImageProperties(bpy.types.PropertyGroup):
    alpha: BoolProperty(
        name="Transparency",
        description="Use alpha blend on image transform",
        default=True
        )
    scale: FloatProperty(
        name="Scale",
        description="Transform scale to apply to fitted image",
        default=1.0
        )
    length: IntProperty(
        name="Strip length",
        description="Frame duration of imported images",
        default=10
        )

class PrettyImagePanel (bpy.types.Panel):
    # Blender UI label, name, placement
    bl_label = "Pretty Image Loader"
    bl_idname = 'strip.pretty_image_loader'
    bl_space_type = 'SEQUENCE_EDITOR'
    bl_region_type = 'UI'
    def draw (self, context):
        row = self.layout.row()
        row.operator("strip.pretty_strip_add", text="Add Pretty Image")

class PrettyImageOperator (bpy.types.Operator):
    # Blender UI label, id and description
    bl_label = "Pretty Image Operator"
    bl_idname = 'strip.pretty_strip_add'
    bl_description = "Add a new image with alpha, transform strip and proper dimensions."
    # import settings
    filepath = StringProperty (name='File Path')
    files = CollectionProperty(name='File Names', type=bpy.types.OperatorFileListElement)
    directory = StringProperty(maxlen=1024, subtype='DIR_PATH',options={'HIDDEN'})
    filter_image = BoolProperty(default=True, options={'HIDDEN'})
    filter_folder = BoolProperty(default=True, options={'HIDDEN'})
    # image loading/formatting
    set_alpha = PrettyImageProperties.alpha
    img_scale = PrettyImageProperties.scale
    length = PrettyImageProperties.length

    def store_files (self, files):
        return [f.name for f in files]

    def execute (self, ctx):
        bpy.context.scene.sequence_editor_create()
        img_filenames = self.store_files(self.files)
        img_path = self.directory
        [print(f) for f in img_filenames]
        return {'FINISHED'}

    # TODO: show file manager when selected in pop-up menu - op keeps placing prev img

    def invoke (self, context, event):
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}

class PrettyImageHandler (bpy.types.Operator):
    bl_label = "Pretty Image Handler"
    bl_idname = 'strip.pretty_strip_handler'
    def execute (self, ctx):
        #bpy.ops.sequencer.pretty_strip_add('INVOKE_DEFAULT')
        print("Running image handler")
        return {'FINISHED'}

def menu_add(self, ctx):
    layout = self.layout
    layout.operator('strip.pretty_strip_handler', text="Pretty Strip")

def register():
    bpy.utils.register_class(PrettyImageProperties)
    bpy.utils.register_class(PrettyImagePanel)
    bpy.utils.register_class(PrettyImageOperator)
    
if __name__ == '__main__':
    register()
