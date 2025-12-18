import bpy
from bpy.props import (StringProperty, PointerProperty, IntProperty, BoolProperty, EnumProperty)                    
from bpy.types import (PropertyGroup, Operator)

import os

from . import anim

import subprocess

# ================================

class BlenderAssistProperties(PropertyGroup):
    # Quick Export Anim
    start_frame: IntProperty(
        name = "Start Frame",
        default = 1,
        min = 1
    )
    end_frame: IntProperty(
        name = "End Frame",
        default = 50,
        min = 5
    )
    compress_anim: BoolProperty(
        name = "Compress animation data",
        default = True
    )
    output_dir: StringProperty(
        name = "",
        default = "./tmp/",
        maxlen = 1024,
        subtype = "DIR_PATH"
    )
    bones_list: EnumProperty(
        name = "Bones",
        default = './template/bones/full.pap',
        items = (
              ('./template/bones/full.pap', "Full Body", "Every bone in a normal animation"),
              ('./template/bones/upper.sklb', "Upper Body", "Only j_sebo and children"),
              )
    )
    race_list: EnumProperty(
        name = "Race",
        default = './template/race/c0101.sklb',
        items = (
              ('./template/race/c0101.sklb', "Midlander M", "C0101"), # value, dropdown-value, tiptool
              ('./template/race/c0801.sklb', "Miqote F", "C0801"),
              )
    )

    # Quick Import Anim
    import_path: StringProperty(
        name = "",
        default = "./template/motion/motion.gltf",
        maxlen = 1024,
        subtype = "FILE_PATH"
    )

class BlenderAssistPanelQuickImportAnim(bpy.types.Panel):
    bl_idname = "BA_PT_Quick_Import_Anim"
    bl_label = "Quick Import Animation"
    bl_category = "BlenderAssist"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        state = scene.b_assist_props

        col = layout.column()
        col.label(text="VFXEditor Exported GLTF File")
        col.prop(state, "import_path")

        layout.operator(BlenderAssistQuickImportAnim.bl_idname, text="Import", icon="PLAY")

class BlenderAssistQuickImportAnim(Operator):
    bl_idname = "b_assist_props.blender_assist_quick_import_anim"
    bl_label = "Blender Assist Operator Quick Import Animation"

    def execute(self, context):
        scene = context.scene
        state = scene.b_assist_props

        import_path = state.import_path

        bpy.ops.import_scene.gltf(filepath=import_path, disable_bone_shape=True, guess_original_bind_pose=False)

        ob = context.object
        ad = ob.animation_data
        ad.nla_tracks.remove(ad.nla_tracks.active)

        for fcurve in ad.action.fcurves:
            for keyframe_point in fcurve.keyframe_points:
                keyframe_point.co.x *= 1.25
        for fcurve in ad.action.fcurves:
            for keyframe_point in fcurve.keyframe_points:
                keyframe_point.co.x += 1

        dummy = ob.children[0]
        bpy.data.objects.remove(dummy)
        
        return {'FINISHED'}
    
# ================================

class BlenderAssistQuickExportAnim(Operator):
    bl_idname = "b_assist_props.blender_assist_quick_export_anim"
    bl_label = "Blender Assist Operator Quick Export Animation"

    def execute(self, context):
        scene = context.scene
        state = scene.b_assist_props

        output_dir = state.output_dir
        anim_in = state.bones_list
        skl_in = state.race_list

        anim_idx = "0"
        check_original_bound = "1"

        compress_anim = "0"
        if state.compress_anim:
            compress_anim = "1"

        dirname = os.path.dirname(os.path.abspath(__file__))
        
        basename = os.path.basename(output_dir)
        basename, _ = os.path.splitext(basename)
        anim_bin_file = dirname + '/tmp/' + basename + '.bin'

        print("Starting exporting to bin: " + anim_bin_file)
        anim.export(
            state.start_frame,
            state.end_frame,
            anim_bin_file
        )

        print("Finished exporting to bin")
        command = dirname + '/bin/blenderassist.exe'
        print(command + " " + str(anim_idx) + " " + anim_bin_file + " " + skl_in + " " + anim_in + " -> " + output_dir)
        print(check_original_bound, compress_anim)
        subprocess.run([command, 'quick_pack_anim', str(anim_idx), anim_bin_file, skl_in, anim_in, output_dir, check_original_bound, compress_anim])

        return {'FINISHED'}
        
class BlenderAssistPanelQuickExportAnim(bpy.types.Panel):
    bl_idname = "BA_PT_Quick_Export_Anim"
    bl_label = "Quick Export Animation"
    bl_category = "BlenderAssist"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        state = scene.b_assist_props

        if context.object != None and context.object.type == 'ARMATURE':
            split = layout.row().split(factor=0.25)
            split.label(text="Target")
            split.label(text=context.object.name, icon='ARMATURE_DATA')

            col = layout.column()
            col.label(text="Output Directory")
            col.prop(state, "output_dir", text="")

            box = layout.box()
            row = box.row(align=True)
            row.prop(state, "start_frame")
            row.prop(state, "end_frame")     

            box.prop(state, "race_list")
            box.prop(state, "bones_list")
            box.prop(state, "compress_anim")

            layout.operator(BlenderAssistQuickExportAnim.bl_idname, text="Export", icon="PLAY")
        else:
            layout.label(text='No armature selected', icon='ERROR') 
    
# ================================
        
classes = (
    BlenderAssistProperties,

    BlenderAssistPanelQuickImportAnim,
    BlenderAssistQuickImportAnim,
    BlenderAssistPanelQuickExportAnim,
    BlenderAssistQuickExportAnim,
)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.Scene.b_assist_props = PointerProperty(type=BlenderAssistProperties)


def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)  
    del bpy.types.Scene.b_assist_props


if __name__ == "__main__":
    register()
