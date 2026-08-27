import bpy
from bpy.props import (StringProperty, PointerProperty, IntProperty, BoolProperty, EnumProperty)                    
from bpy.types import (PropertyGroup, Operator)

import os

from . import anim

import subprocess

working_dir = dirname = os.path.dirname(os.path.abspath(__file__))
print(working_dir)
# ================================

class SimpleAssistProperties(PropertyGroup):
    # Simple Export Anim
    start_frame: IntProperty(
        name = "Start Frame",
        default = 1,
        min = 1
    ) # type: ignore
    end_frame: IntProperty(
        name = "End Frame",
        default = 50,
        min = 5
    ) # type: ignore
    data_list: EnumProperty(
        name = "Data List",
        default = '0',
        items = (
            ('0', "Default", "Export usually used bones in FFXIV animations"), # value, dropdown-value, tiptool
            ('1', "Upper", "Export only upper body"),
            ('2', "Arm", "Export only right arm"),
            ('3', "All", "Export all bones")
        )
    ) # type: ignore
    output_dir: StringProperty(
        name = "",
        default = working_dir + "/tmp/",
        maxlen = 1024,
        subtype = "DIR_PATH"
    ) # type: ignore
    race_list: EnumProperty(
        name = "Bone List",
        default = working_dir + '/template/race/c0101.sklb',
        items = (
                (working_dir + '/template/race/c0101.sklb', "Midlander M", "C0101"), # value, dropdown-value, tiptool
                (working_dir + '/template/race/c0201.sklb', "Midlander F", "C0201"),
                (working_dir + '/template/race/c0301.sklb', "Highlander M", "C0301"),
                (working_dir + '/template/race/c0401.sklb', "Highlander F", "C0401"),
                (working_dir + '/template/race/c0501.sklb', "Elezen M", "C0501"),
                (working_dir + '/template/race/c0601.sklb', "Elezen F", "C0601"),
                (working_dir + '/template/race/c0701.sklb', "Miqote M", "C0701"),
                (working_dir + '/template/race/c0801.sklb', "Miqote F", "C0801"),
                (working_dir + '/template/race/c0901.sklb', "Roegadyn M", "C0901"),
                (working_dir + '/template/race/c1001.sklb', "Roegadyn F", "C1001"),
                (working_dir + '/template/race/c1101.sklb', "Lalafell M", "C1101"),
                (working_dir + '/template/race/c1201.sklb', "Lalafell F", "C1201"),
                (working_dir + '/template/race/c1301.sklb', "Aura M", "C1301"),
                (working_dir + '/template/race/c1401.sklb', "Aura F", "C1401"),
                (working_dir + '/template/race/c1501.sklb', "Hrothgar M", "C1501"),
                (working_dir + '/template/race/c1601.sklb', "Hrothgar F", "C1601"),
                (working_dir + '/template/race/c1701.sklb', "Viera M", "C1701"),
                (working_dir + '/template/race/c1801.sklb', "Viera F", "C1801")
        )
    ) # type: ignore

    # Simple Import Anim
    import_path: StringProperty(
        name = "",
        default = working_dir + '/template/motion/motion.gltf',
        maxlen = 1024,
        subtype = "FILE_PATH"
    ) # type: ignore

class SimpleAssistPanelImportAnim(bpy.types.Panel):
    bl_idname = "BA_PT_Import_Anim"
    bl_label = "Import Animation"
    bl_category = "SimpleAssist"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        state = scene.b_assist_props

        col = layout.column()
        col.label(text="Input GLTF File")
        col.prop(state, "import_path")

        layout.operator(SimpleAssistImportAnim.bl_idname, text="Import", icon="PLAY")

        layout.operator(SimpleAssistImportMesh.bl_idname, text="Import Mannequin", icon="MESH_DATA")

class SimpleAssistImportAnim(Operator):
    """Import animation from .gltf file exported by VFXEditor PAP Editor"""
    bl_idname = "b_assist_props.blender_assist_import_anim"
    bl_label = "Blender Assist Operator Import Animation"

    def execute(self, context):
        scene = context.scene
        state = scene.b_assist_props

        import_path = state.import_path

        bpy.ops.import_scene.gltf(filepath=import_path, disable_bone_shape=True, guess_original_bind_pose=False)

        ob = context.object
        ad = ob.animation_data
        ad.nla_tracks.remove(ad.nla_tracks.active)

        if(ad.action.fcurves[0].keyframe_points[1].co.x != 1):
            print("Frame 2 was " + str(ad.action.fcurves[0].keyframe_points[1].co.x) + " and got adjusted to 1")
            multiplier = 1 / ad.action.fcurves[0].keyframe_points[1].co.x
            for fcurve in ad.action.fcurves:
                for keyframe_point in fcurve.keyframe_points:
                    keyframe_point.co.x = round(keyframe_point.co.x * multiplier)
        for fcurve in ad.action.fcurves:
            for keyframe_point in fcurve.keyframe_points:
                keyframe_point.co.x += 1

        dummy = ob.children[0]
        bpy.data.objects.remove(dummy)

        return {'FINISHED'}
    
class SimpleAssistImportMesh(Operator):
    """Import a default Midlander M mesh"""
    bl_idname = "b_assist_props.blender_assist_import_mesh"
    bl_label = "Blender Assist Operator Import Mesh"

    def execute(self, context):
        import_path = working_dir + '/template/mesh/c0101.glb'

        bpy.ops.import_scene.gltf(filepath=import_path, disable_bone_shape=True, guess_original_bind_pose=False)
        
        return {'FINISHED'}

# ================================

class SimpleAssistPanelEdit(bpy.types.Panel):
    bl_idname = "BA_PT_Edit"
    bl_label = "Edit"
    bl_category = "SimpleAssist"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"

    def draw(self, context):
        layout = self.layout
        if context.object != None and context.object.type == 'ARMATURE':

            split = layout.row().split()
            split.operator(SimpleAssistEditConstraint.bl_idname, text="Constraint", icon="CONSTRAINT")
            split.operator(SimpleAssistEditTail.bl_idname, text="Tail Constraints", icon="CON_FOLLOWTRACK")
        else:
            layout.label(text='No armature selected', icon='ERROR') 

class SimpleAssistEditConstraint(Operator):
    """Add constraints to relevant joints"""
    bl_idname = "b_assist_props.blender_assist_edit_constraint"
    bl_label = "Blender Assist Operator Edit Constraint"

    def execute(self, context):
        anim.curatePose(context.object)

        return {'FINISHED'}

class SimpleAssistEditTail(Operator):
    """Add constraints to tail bones"""
    bl_idname = "b_assist_props.blender_assist_edit_tail"
    bl_label = "Blender Assist Operator Edit Tail"

    def execute(self, context):
        anim.tailTrack(context.object)

        return {'FINISHED'}
        
# ================================

class SimpleAssistExportAnim(Operator):
    """Export animation to .hkx to the indicated directory(anim.hkx) using the output bone list specified\n
Cannot be used to retarget\nTo retarget, import an animation using desired skeleton and change its NLA tracks as necessary"""
    bl_idname = "b_assist_props.blender_assist_export_anim"
    bl_label = "Blender Assist Operator Export Animation"

    def execute(self, context):
        scene = context.scene
        state = scene.b_assist_props

        output_dir = state.output_dir
        anim_in = working_dir + '/template/bones/full.pap'
        skl_in = state.race_list

        anim_idx = "0"
        check_original_bound = "1"
        compress_anim = "0"

        match state.data_list:
            case '1': 
                anim_in = working_dir + '/template/bones/upper.pap'
            case '2':
                anim_in = working_dir + '/template/bones/arm.pap'
            case '3':
                check_original_bound = "0"

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
        
class SimpleAssistPanelExportAnim(bpy.types.Panel):
    bl_idname = "BA_PT_Export_Anim"
    bl_label = "Export Animation"
    bl_category = "SimpleAssist"
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

            grid = box.grid_flow(columns=1, align=True)
            grid.prop(state, "race_list")
            grid.prop(state, "data_list")

            layout.operator(SimpleAssistExportAnim.bl_idname, text="Export", icon="PLAY")
        else:
            layout.label(text='No armature selected', icon='ERROR') 
    
# ================================
        
classes = (
    SimpleAssistProperties,

    SimpleAssistPanelImportAnim,
    SimpleAssistImportAnim,
    SimpleAssistImportMesh,
    SimpleAssistPanelEdit,
    SimpleAssistEditConstraint,
    SimpleAssistEditTail,
    SimpleAssistPanelExportAnim,
    SimpleAssistExportAnim,
)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.Scene.b_assist_props = PointerProperty(type=SimpleAssistProperties)


def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)  
    del bpy.types.Scene.b_assist_props


if __name__ == "__main__":
    register()
