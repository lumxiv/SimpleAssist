import bpy

from . import helper

class Rotation:
    def __init__(self, min, max):
        self.min = min
        self.max = max

class XYZ:
    def __init__(self, X: Rotation, Y: Rotation, Z: Rotation):
        self.X = X
        self.Y = Y
        self.Z = Z

def limitRot(object, name, xyz: XYZ):
    bone = object.pose.bones[object.pose.bones.find(name)]
    bone.use_ik_limit_x = True
    bone.use_ik_limit_y = True
    bone.use_ik_limit_z = True
    bone.ik_max_x = xyz.X.max
    bone.ik_min_x = xyz.X.min
    bone.ik_max_y = xyz.Y.max
    bone.ik_min_y = xyz.Y.min
    bone.ik_max_z = xyz.Z.max
    bone.ik_min_z = xyz.Z.min

def tailTrack(object):
    dampedTrackCn(object, "n_sippo_a", "n_sippo_b", .2)
    dampedTrackCn(object, "n_sippo_b", "n_sippo_c", .4)
    dampedTrackCn(object, "n_sippo_c", "n_sippo_d", .6)
    dampedTrackCn(object, "n_sippo_d", "n_sippo_e", .8)

def dampedTrackObjCn(object, source, target, influence):
    pose = object.pose
    name = "Simple Damped Track Obj"
    if pose.bones[pose.bones.find(source)].constraints.find(name) != -1:
        return
    
    cn = pose.bones[pose.bones.find(source)].constraints.new(type="DAMPED_TRACK")
    cn.name = name
    cn.target = bpy.data.objects.get(target)
    cn.influence = influence
    cn.track_axis = "TRACK_X"

def dampedTrackCn(object, source, target, influence):
    pose = object.pose
    name = "Simple Damped Track"
    if pose.bones[pose.bones.find(source)].constraints.find(name) != -1:
        return
    
    cn = pose.bones[pose.bones.find(source)].constraints.new(type="DAMPED_TRACK")
    cn.name = name
    cn.target = object
    cn.subtarget = target
    cn.influence = influence
    cn.track_axis = "TRACK_X"

def copyTransformCn(object, target, subtarget, influence):
    name = "Simple Copy Transform"
    if object.constraints.find(name) != -1:
        return
    
    cn = object.constraints.new(type="COPY_TRANSFORMS")
    cn.name = name
    cn.target = target
    cn.subtarget = subtarget
    cn.influence = influence
    cn.mix_mode = "BEFORE_FULL"

def curatePose(object):
    lockIKXY(object, "j_ude_b_r")
    lockIKXY(object, "j_asi_b_r")
    lockIKXY(object, "j_asi_c_r")
    lockIKXY(object, "j_ude_b_l")
    lockIKXY(object, "j_asi_b_l")
    lockIKXY(object, "j_asi_c_l")
    wristCn(object, "n_hte_r", "j_te_r")
    shoulderCn(object, "n_hkata_r", "j_ude_a_r")
    elbowCn(object, "n_hhiji_r", "j_ude_a_r")
    wristCn(object, "n_hte_l", "j_te_l")
    shoulderCn(object, "n_hkata_l", "j_ude_a_l")
    elbowCn(object, "n_hhiji_l", "j_ude_a_l")
    muteChannels(object, "n_hte_r")
    muteChannels(object, "n_hkata_r")
    muteChannels(object, "n_hhiji_r")
    muteChannels(object, "n_hte_l")
    muteChannels(object, "n_hkata_l")
    muteChannels(object, "n_hhiji_l")

    muteChannels(object, "n_root")
    limitRot(object, "n_root", XYZ(Rotation(0,0),Rotation(0,0),Rotation(0,0)))
    #limitRot(object, "n_hara", XYZ(Rotation(0,0),Rotation(0,0),Rotation(0,0)))

    limitRot(object, "j_te_r", XYZ(Rotation(-1.5708,1.5708),Rotation(-1.5708,1.5708),Rotation(-1.309,1.309)))
    limitRot(object, "j_sako_r", XYZ(Rotation(-0.261799,0.261799),Rotation(-0.261799,0.261799),Rotation(-0.261799,0.610865)))
    limitRot(object, "j_ude_a_r", XYZ(Rotation(-1.5708,1.5708),Rotation(-1.5708,1.5708),Rotation(-1.5708,1.5708)))
    limitRot(object, "j_ude_b_r", XYZ(Rotation(0,0),Rotation(0,0),Rotation(-2.61799,0)))
    limitRot(object, "j_asi_a_r", XYZ(Rotation(-0.785398,0.785398),Rotation(-0.436332,0.785398),Rotation(-2.44346,0.785398)))
    limitRot(object, "j_asi_b_r", XYZ(Rotation(0,0),Rotation(0,0),Rotation(0,1.309)))
    limitRot(object, "j_asi_c_r", XYZ(Rotation(0,0),Rotation(0,0),Rotation(0,1.309)))
    limitRot(object, "j_asi_d_r", XYZ(Rotation(-0.523599,0.523599),Rotation(-0.523599,0.523599),Rotation(-0.785398,-0.785398)))

    limitRot(object, "j_te_l", XYZ(Rotation(-1.5708,1.5708),Rotation(-1.5708,1.5708),Rotation(-1.309,1.309)))
    limitRot(object, "j_sako_l", XYZ(Rotation(-0.261799,0.261799),Rotation(-0.261799,0.261799),Rotation(-0.261799,0.610865)))
    limitRot(object, "j_ude_a_l", XYZ(Rotation(-1.5708,1.5708),Rotation(-1.5708,1.5708),Rotation(-1.5708,1.5708)))
    limitRot(object, "j_ude_b_l", XYZ(Rotation(0,0),Rotation(0,0),Rotation(-2.61799,0)))
    limitRot(object, "j_asi_a_l", XYZ(Rotation(-0.785398,0.785398),Rotation(-0.436332,0.785398),Rotation(-2.44346,0.785398)))
    limitRot(object, "j_asi_b_l", XYZ(Rotation(0,0),Rotation(0,0),Rotation(0,1.309)))
    limitRot(object, "j_asi_c_l", XYZ(Rotation(0,0),Rotation(0,0),Rotation(0,1.309)))
    limitRot(object, "j_asi_d_l", XYZ(Rotation(-0.523599,0.523599),Rotation(-0.523599,0.523599),Rotation(-0.785398,-0.785398)))

    #sebo and kosi can be used as rotation substitute to n_hara, better not add these all the time
    #limitRot(object, "j_kosi", XYZ(Rotation(-0.349066,0.349066),Rotation(-0.349066,0.349066),Rotation(-0.349066,0.349066)))
    #limitRot(object, "j_sebo_a", XYZ(Rotation(-0.349066,0.349066),Rotation(-0.349066,0.349066),Rotation(-0.349066,0.349066)))

    limitRot(object, "j_sebo_b", XYZ(Rotation(-0.349066,0.349066),Rotation(-0.349066,0.349066),Rotation(-0.349066,0.349066)))
    limitRot(object, "j_sebo_c", XYZ(Rotation(-0.349066,0.349066),Rotation(-0.349066,0.349066),Rotation(-0.349066,0.349066)))

def muteChannels(object, name):
    ad = object.animation_data
    if hasattr(ad, 'action'):
        for fcurve in ad.action.fcurves:
            if fcurve.data_path.startswith('pose.bones["' + name + '"]'):
                fcurve.mute = True

    for pbone in object.pose.bones:
        if(pbone.name == name):
            pbone.rotation_quaternion = (1.0, 0.0, 0.0, 0.0)
            pbone.rotation_euler = (0.0, 0.0, 0.0)
            pbone.location = (0.0, 0.0, 0.0)
            pbone.scale = (1.0, 1.0, 1.0)

def wristCn(object, source, target):
    pose = object.pose
    name = "Simple Copy Rotation"
    if pose.bones[pose.bones.find(source)].constraints.find(name) != -1:
        return

    cn = pose.bones[pose.bones.find(source)].constraints.new(type="COPY_ROTATION")
    cn.name = name
    cn.target = object
    cn.subtarget = target
    cn.use_y = False
    cn.use_z = False
    cn.influence = 0.5
    cn.owner_space = "LOCAL"
    cn.target_space = "LOCAL"

def shoulderCn(object, source, target):
    pose = object.pose
    name = "Simple Copy Rotation"
    if pose.bones[pose.bones.find(source)].constraints.find(name) != -1:
        return
    
    cn = pose.bones[pose.bones.find(source)].constraints.new(type="COPY_ROTATION")
    cn.name = name
    cn.target = object
    cn.subtarget = target
    cn.invert_x = True
    cn.use_y = False
    cn.use_z = False
    cn.influence = 0.5
    cn.owner_space = "LOCAL"
    cn.target_space = "LOCAL"

def elbowCn(object, source, target):
    pose = object.pose
    name = "Simple Locked Track"
    if pose.bones[pose.bones.find(source)].constraints.find(name) != -1:
        return

    cn = pose.bones[pose.bones.find(source)].constraints.new(type="LOCKED_TRACK")
    cn.name = name
    cn.target = object
    cn.subtarget = target
    cn.track_axis = "TRACK_NEGATIVE_X"
    cn.lock_axis = "LOCK_Z"
    cn.influence = 0.5

def lockIKXY(object, name):
    pose = object.pose
    pose.bones[pose.bones.find(name)].lock_ik_x = True
    pose.bones[pose.bones.find(name)].lock_ik_y = True

def addFakeBone(context, name, parent, offset):
    if bpy.data.objects.get(name) != None:
        return
    
    armature = context.object
    bpy.ops.object.mode_set(mode='OBJECT')
    bpy.ops.object.select_all(action='DESELECT')
    bpy.ops.object.add()
    ob = context.object
    ob.name = name
    ob.parent = armature
    ob.location = offset
    ob.empty_display_size = .05
    ob.empty_display_type = "SPHERE"
    ob.hide_viewport = True
    copyTransformCn(ob, armature, parent, 1)
    bpy.ops.object.select_all(action='DESELECT')
    armature.select_set(True)
    bpy.context.view_layer.objects.active = armature

def addSkirtBones(context):
    offsetFw = -.20
    offsetSi = .14
    offsetBk = .22
    addFakeBone(context, "j_sk_f_a_dt_r", "j_asi_b_r", (0, offsetFw, 0))
    addFakeBone(context, "j_sk_s_a_dt_r", "j_asi_b_r", (0, 0, -offsetSi))
    addFakeBone(context, "j_sk_b_a_dt_r", "j_asi_b_r", (0, offsetBk, 0))
    addFakeBone(context, "j_sk_f_a_dt_l", "j_asi_b_l", (0, offsetFw, 0))
    addFakeBone(context, "j_sk_s_a_dt_l", "j_asi_b_l", (0, 0, offsetSi))
    addFakeBone(context, "j_sk_b_a_dt_l", "j_asi_b_l", (0, offsetBk, 0))

    addFakeBone(context, "j_sk_f_b_dt_r", "j_asi_c_r", (0, offsetFw, 0))
    addFakeBone(context, "j_sk_s_b_dt_r", "j_asi_c_r", (0, 0, -offsetSi))
    addFakeBone(context, "j_sk_b_b_dt_r", "j_asi_d_r", (0, offsetBk, 0))
    addFakeBone(context, "j_sk_f_b_dt_l", "j_asi_c_l", (0, offsetFw, 0))
    addFakeBone(context, "j_sk_s_b_dt_l", "j_asi_c_l", (0, 0, offsetSi))
    addFakeBone(context, "j_sk_b_b_dt_l", "j_asi_d_l", (0, offsetBk, 0))

    addFakeBone(context, "j_sk_f_c_dt_r", "j_asi_c_r", (0, offsetFw, 0))
    addFakeBone(context, "j_sk_s_c_dt_r", "j_asi_d_r", (0, 0, -offsetSi))
    addFakeBone(context, "j_sk_b_c_dt_r", "j_asi_d_r", (0, offsetBk, 0))
    addFakeBone(context, "j_sk_f_c_dt_l", "j_asi_c_l", (0, offsetFw, 0))
    addFakeBone(context, "j_sk_s_c_dt_l", "j_asi_d_l", (0, 0, offsetSi))
    addFakeBone(context, "j_sk_b_c_dt_l", "j_asi_d_l", (0, offsetBk, 0))

def skirtCn(object):
    dampedTrackObjCn(object, "j_sk_f_a_r", "j_sk_f_a_dt_r", 1)
    dampedTrackObjCn(object, "j_sk_s_a_r", "j_sk_s_a_dt_r", 1)
    dampedTrackObjCn(object, "j_sk_b_a_r", "j_sk_b_a_dt_r", 1)
    dampedTrackObjCn(object, "j_sk_f_a_l", "j_sk_f_a_dt_l", 1)
    dampedTrackObjCn(object, "j_sk_s_a_l", "j_sk_s_a_dt_l", 1)
    dampedTrackObjCn(object, "j_sk_b_a_l", "j_sk_b_a_dt_l", 1)

    dampedTrackObjCn(object, "j_sk_f_b_r", "j_sk_f_b_dt_r", .5)
    dampedTrackObjCn(object, "j_sk_s_b_r", "j_sk_s_b_dt_r", .5)
    dampedTrackObjCn(object, "j_sk_b_b_r", "j_sk_b_b_dt_r", .5)
    dampedTrackObjCn(object, "j_sk_f_b_l", "j_sk_f_b_dt_l", .5)
    dampedTrackObjCn(object, "j_sk_s_b_l", "j_sk_s_b_dt_l", .5)
    dampedTrackObjCn(object, "j_sk_b_b_l", "j_sk_b_b_dt_l", .5)

    dampedTrackObjCn(object, "j_sk_f_c_r", "j_sk_f_c_dt_r", .5)
    dampedTrackObjCn(object, "j_sk_s_c_r", "j_sk_s_c_dt_r", .5)
    dampedTrackObjCn(object, "j_sk_b_c_r", "j_sk_b_c_dt_r", 1)
    dampedTrackObjCn(object, "j_sk_f_c_l", "j_sk_f_c_dt_l", .5)
    dampedTrackObjCn(object, "j_sk_s_c_l", "j_sk_s_c_dt_l", .5)
    dampedTrackObjCn(object, "j_sk_b_c_l", "j_sk_b_c_dt_l", 1)

def skirtTrack(object):
    skirtCn(object)
    muteChannels(object, "j_sk_f_a_r")
    muteChannels(object, "j_sk_s_a_r")
    muteChannels(object, "j_sk_b_a_r")
    muteChannels(object, "j_sk_f_a_l")
    muteChannels(object, "j_sk_s_a_l")
    muteChannels(object, "j_sk_b_a_l")

def export(startFrame, endFrame, out_bin_file):
    arm_ob = helper.detect_armature()
    bpy.context.view_layer.objects.active = arm_ob
    bpy.context.active_object.select_set(state=True)

    numOriginalFrames = endFrame - startFrame
    duration = float(numOriginalFrames - 1) * 0.0345

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