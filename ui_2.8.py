import bpy
from bpy_extras.io_utils import ImportHelper

# UI menu properties
class PrettyImageProperties(bpy.types.PropertyGroup):
    alpha : bpy.props.BoolProperty(
        name="Transparency",
        description="Use alpha blend on image transform",
        default=True
        )
    scale : bpy.props.FloatProperty(
        name="Scale",
        description="Transform scale to apply to fitted image",
        default=1.0
        )
    length : bpy.props.IntProperty(
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
    bl_category = 'Strip'
    
    def draw (self, context):
        row = self.layout.row()
        row.operator("strip.pretty_strip_add", text="Add Pretty Image")

class PrettyImageOperator (bpy.types.Operator):
    # Blender UI label, id and description
    bl_label = "Pretty Image Operator"
    bl_idname = 'strip.pretty_strip_add'
    bl_description = "Add a new image with alpha, transform strip and proper dimensions."
    # import settings
    filepath = bpy.props.StringProperty (name='File Path')
    files = bpy.props.CollectionProperty(name='File Names', type=bpy.types.OperatorFileListElement)
    directory = bpy.props.StringProperty(maxlen=1024, subtype='DIR_PATH',options={'HIDDEN'})
    filter_image = bpy.props.BoolProperty(default=True, options={'HIDDEN'})
    filter_folder = bpy.props.BoolProperty(default=True, options={'HIDDEN'})
    # image loading/formatting
    set_alpha = PrettyImageProperties.alpha
    img_scale = PrettyImageProperties.scale
    length = PrettyImageProperties.length

    def store_files (self, files):
        return [f.name for f in files]

    def execute (self, context):
        context.scene.sequence_editor_create()
        img_filenames = self.store_files(self.files)
        [print(f) for f in img_filenames]
        return {'FINISHED'}

    # TODO: show file manager when selected in pop-up menu - op keeps placing prev img

    def invoke (self, context, event):
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}

class PrettyImageHandler (bpy.types.Operator):
    bl_label = "Pretty Image Handler"
    bl_idname = 'strip.pretty_strip_handler'
    
    def execute (self, context):
        #bpy.ops.sequencer.pretty_strip_add('INVOKE_DEFAULT')
        print("Running image handler")
        return {'FINISHED'}

def menu_add(self, ctx):
    layout = self.layout
    layout.operator('strip.pretty_strip_handler', text="Pretty Strip")

ui_classes = [
    PrettyImageProperties,
    PrettyImagePanel,
    PrettyImageOperator
]

def register():
    for ui_class in ui_classes:
        bpy.utils.register_class(ui_class)
    bpy.types.SEQUENCER_MT_add.append(menu_add)
    bpy.types.ImageSequence.pretty_image = bpy.props.PointerProperty(
        type=PrettyImageProperties,
        description=""
        )

def unregister():
    for ui_class in reversed(ui_classes):
        bpy.utils.unregister_class(ui_class) 
    del bpy.types.ImageSequence.pretty_image

if __name__ == '__main__':
    register()
