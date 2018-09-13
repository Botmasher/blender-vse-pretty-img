#!/usr/bin/env python
import bpy

def load_scale_img (name, path, scale=1.0, channel=1, length=10, alpha=True):

    scene = bpy.context.scene

    scene.sequence_editor_create()
    # create sequence editor

    strip = scene.sequence_editor.sequences.new_image(name=name, filepath=path, channel=channel, frame_start=scene.frame_current)

    def deselect_strips ():
        bpy.ops.sequencer.select_all(action='DESELECT')
        return

    # TODO set channel strip wisely - currently importing many causes interlaced stacking of transform and image strips

    deselect_strips()
    strip.select = True
    scene.sequence_editor.active_strip = strip

    bpy.ops.sequencer.effect_strip_add(type='TRANSFORM')
    transform_strip = scene.sequence_editor.active_strip
    transform_strip.use_uniform_scale = False

    # hack: update in viewport to read source img orig_width and orig_height
    # switch view and area
    area = bpy.context.area
    original_area = area.type
    area.type = 'SEQUENCE_EDITOR'
    original_view = area.spaces[0].view_type
    area.spaces[0].view_type = 'PREVIEW'
    # NOTE playhead steps alone are sufficient when user has visible VSE Preview
    frame_initial = scene.frame_current
    scene.frame_current = strip.frame_start
    bpy.ops.render.opengl(sequencer=True)
    # reset view and area
    area.spaces[0].view_type = original_view
    area.type = original_area
    # /hack

    # gather image data
    img = strip.elements[0]
    # store dimensions

    if not (img.orig_width and img.orig_height):
        print("pretty_img - Failed to rescale img with width or height of 0: {0}".format(img.filename))
        return

    img_res = {
        'w': img.orig_width,
        'h': img.orig_height
    }
    print("%s: %s" % (img.filename, "{0} x {1}".format(img_res['w'], img_res['h'])))

    # resize image
    # figure out how to resize just using input dimensions, the stretch applied, transform scale
    render_res = {'w': scene.render.resolution_x, 'h': scene.render.resolution_y}
    img_render_ratio = {'w': img_res['w'] / render_res['w'], 'h': img_res['h'] / render_res['h']}
    print("Image vs screen res ratio - w: {0:.0f}%, h: {1:.0f}%".format(img_render_ratio['w'] * 100, img_render_ratio['h'] * 100))

    bpy.ops.sequencer.refresh_all()

    scaled_img_h = scene.render.resolution_y    # 1.0 scale y == 100% render_res.h
    scaled_img_w = scene.render.resolution_x    # stretched value
    scaled_img_w_target = img_res['w'] / img_res['h'] * scaled_img_h  # final value we're after
    img_rescale_y = scaled_img_w_target / scaled_img_w  # what is that as a percentage of stretch?

    transform_strip.use_uniform_scale = False
    transform_strip.scale_start_y = scale                   # w
    transform_strip.scale_start_x = img_rescale_y * scale   # h

    # set strip opacity
    if alpha:
        transform_strip.blend_type = 'ALPHA_OVER'
        transform_strip.blend_alpha = 1.0
        strip.blend_type = 'ALPHA_OVER'
        strip.blend_alpha = 0.0

    # set strip length
    strip.frame_final_duration = length

    scene.frame_current = frame_initial

    deselect_strips()

    return strip
