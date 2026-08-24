import bpy

from . import helper

def export(startFrame, endFrame, out_bin_file):
    arm_ob = helper.detect_armature()
    bpy.context.view_layer.objects.active = arm_ob
    bpy.context.active_object.select_set(state=True)

    numOriginalFrames = endFrame - startFrame
    duration = float(numOriginalFrames) * 0.0345

    tracks = {}
    for bone in arm_ob.data.bones:
        if bone.name == "n_root":
            continue

        tracks[bone.name] = []

    numTracks = len(tracks)

    current_frame = 0
    for current_frame in range(numOriginalFrames + 1):
        #current_time = current_frame * 0.0333333333333333
        bpy.context.scene.frame_set(current_frame + startFrame)

        for pose_bone in arm_ob.pose.bones:
            if pose_bone.name not in tracks:
                continue
            bone = pose_bone.bone
            
            if pose_bone.parent:
                m = pose_bone.parent.matrix.inverted() @ pose_bone.matrix
            else:
                m = pose_bone.matrix

            location, rotation, scale = m.decompose()
            t = helper.Transform()
            t.translation = location
            t.rotation = rotation
            t.scale = scale
            tracks[pose_bone.name].append(t)

    with open(out_bin_file, 'wb') as file:
        helper.write_int(file, numOriginalFrames)
        helper.write_int(file, numTracks)
        helper.write_float(file, duration)
        
        for track_name in tracks:
            helper.write_cstring(file, track_name)
            
        for current_frame in range(numOriginalFrames + 1):
            for track_name in tracks:
                transform = tracks[track_name][current_frame]
                transform.write(file)