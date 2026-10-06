import bpy

from . import helper
from mathutils import Vector

class Rotation:
    def __init__(self, min, max):
        self.min = min
        self.max = max

class XYZ:
    def __init__(self, X: Rotation, Y: Rotation, Z: Rotation):
        self.X = X
        self.Y = Y
        self.Z = Z

def get_pbone(obj, name):
    return obj.pose.bones.get(name)   # None if missing

def limitRot(object, name, xyz: XYZ):
    bone = get_pbone(object, name)
    if bone is None:
        return
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

def dampedTrackHelperCn(object, source, helper, influence):
    pose = object.pose
    name = "Simple Damped Track Helper"
    pb = pose.bones[pose.bones.find(source)]
    if pb.constraints.find(name) != -1:
        return

    cn = pb.constraints.new(type="DAMPED_TRACK")
    cn.name = name
    cn.target = object
    cn.subtarget = helper
    cn.influence = influence
    cn.track_axis = "TRACK_X"

def dampedTrackCn(object, source, target, influence):
    bone = get_pbone(object, source)
    if bone is None:
        return
    name = "Simple Damped Track"
    if bone.constraints.find(name) != -1:
        return
    
    cn = bone.constraints.new(type="DAMPED_TRACK")
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
    limitRot(object, "j_asi_d_r", XYZ(Rotation(-0.523599,0.523599),Rotation(-0.523599,0.523599),Rotation(-0.785398,0.785398)))

    limitRot(object, "j_te_l", XYZ(Rotation(-1.5708,1.5708),Rotation(-1.5708,1.5708),Rotation(-1.309,1.309)))
    limitRot(object, "j_sako_l", XYZ(Rotation(-0.261799,0.261799),Rotation(-0.261799,0.261799),Rotation(-0.261799,0.610865)))
    limitRot(object, "j_ude_a_l", XYZ(Rotation(-1.5708,1.5708),Rotation(-1.5708,1.5708),Rotation(-1.5708,1.5708)))
    limitRot(object, "j_ude_b_l", XYZ(Rotation(0,0),Rotation(0,0),Rotation(-2.61799,0)))
    limitRot(object, "j_asi_a_l", XYZ(Rotation(-0.785398,0.785398),Rotation(-0.436332,0.785398),Rotation(-2.44346,0.785398)))
    limitRot(object, "j_asi_b_l", XYZ(Rotation(0,0),Rotation(0,0),Rotation(0,1.309)))
    limitRot(object, "j_asi_c_l", XYZ(Rotation(0,0),Rotation(0,0),Rotation(0,1.309)))
    limitRot(object, "j_asi_d_l", XYZ(Rotation(-0.523599,0.523599),Rotation(-0.523599,0.523599),Rotation(-0.785398,0.785398)))

    #sebo and kosi can be used as rotation substitute to n_hara, better not add these all the time
    #limitRot(object, "j_kosi", XYZ(Rotation(-0.349066,0.349066),Rotation(-0.349066,0.349066),Rotation(-0.349066,0.349066)))
    #limitRot(object, "j_sebo_a", XYZ(Rotation(-0.349066,0.349066),Rotation(-0.349066,0.349066),Rotation(-0.349066,0.349066)))

    limitRot(object, "j_sebo_b", XYZ(Rotation(-0.349066,0.349066),Rotation(-0.349066,0.349066),Rotation(-0.349066,0.349066)))
    limitRot(object, "j_sebo_c", XYZ(Rotation(-0.349066,0.349066),Rotation(-0.349066,0.349066),Rotation(-0.349066,0.349066)))

def muteChannels(object, name):
    ad = object.animation_data
    for fcurve in helper.get_fcurves(ad):
        if fcurve.data_path.startswith('pose.bones["' + name + '"]'):
            fcurve.mute = True

    for pbone in object.pose.bones:
        if(pbone.name == name):
            pbone.rotation_quaternion = (1.0, 0.0, 0.0, 0.0)
            pbone.rotation_euler = (0.0, 0.0, 0.0)
            pbone.location = (0.0, 0.0, 0.0)
            pbone.scale = (1.0, 1.0, 1.0)

def wristCn(object, source, target):
    bone = get_pbone(object, source)
    if bone is None:
        return
    name = "Simple Copy Rotation"
    if bone.constraints.find(name) != -1:
        return

    cn = bone.constraints.new(type="COPY_ROTATION")
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
    bone = get_pbone(object, name)
    if bone is None:
        return
    bone.lock_ik_x = True
    bone.lock_ik_y = True

def addHelperBones(context, specs):
    """specs: list of (name, parent_bone_name, offset in parent's local space)."""
    armature = context.object
    prev_mode = armature.mode
    created = []

    bpy.ops.object.mode_set(mode='EDIT')
    edit_bones = armature.data.edit_bones
    for name, parent, offset in specs:
        if name in edit_bones or parent not in edit_bones:
            continue
        parent_eb = edit_bones[parent]
        eb = edit_bones.new(name)
        eb.head = parent_eb.matrix @ Vector(offset)
        eb.tail = eb.head + Vector((0, 0, 0.02))
        eb.parent = parent_eb
        eb.use_connect = False
        eb.use_deform = False
        created.append(name)
    bpy.ops.object.mode_set(mode=prev_mode)

    for name in created:
        bone = armature.data.bones[name]
        bone[helper.HELPER_PROP] = True
        bone.hide = True

def addSkirtBones(context):
    offsetFw = -.20
    offsetSi = .14
    offsetBk = .22
    specs = [
        ("j_sk_f_a_dt_r", "j_asi_b_r", (0, offsetFw, 0)),
        ("j_sk_s_a_dt_r", "j_asi_b_r", (0, 0, -offsetSi)),
        ("j_sk_b_a_dt_r", "j_asi_b_r", (0, offsetBk, 0)),
        ("j_sk_f_a_dt_l", "j_asi_b_l", (0, offsetFw, 0)),
        ("j_sk_s_a_dt_l", "j_asi_b_l", (0, 0, offsetSi)),
        ("j_sk_b_a_dt_l", "j_asi_b_l", (0, offsetBk, 0)),

        ("j_sk_f_b_dt_r", "j_asi_c_r", (0, offsetFw, 0)),
        ("j_sk_s_b_dt_r", "j_asi_c_r", (0, 0, -offsetSi)),
        ("j_sk_b_b_dt_r", "j_asi_d_r", (0, offsetBk, 0)),
        ("j_sk_f_b_dt_l", "j_asi_c_l", (0, offsetFw, 0)),
        ("j_sk_s_b_dt_l", "j_asi_c_l", (0, 0, offsetSi)),
        ("j_sk_b_b_dt_l", "j_asi_d_l", (0, offsetBk, 0)),

        ("j_sk_f_c_dt_r", "j_asi_c_r", (0, offsetFw, 0)),
        ("j_sk_s_c_dt_r", "j_asi_d_r", (0, 0, -offsetSi)),
        ("j_sk_b_c_dt_r", "j_asi_d_r", (0, offsetBk, 0)),
        ("j_sk_f_c_dt_l", "j_asi_c_l", (0, offsetFw, 0)),
        ("j_sk_s_c_dt_l", "j_asi_d_l", (0, 0, offsetSi)),
        ("j_sk_b_c_dt_l", "j_asi_d_l", (0, offsetBk, 0)),
    ]
    addHelperBones(context, specs)

def skirtCn(object):
    for side in ("r", "l"):
        for part in ("f", "s", "b"):
            dampedTrackHelperCn(object, f"j_sk_{part}_a_{side}", f"j_sk_{part}_a_dt_{side}", 1)
            dampedTrackHelperCn(object, f"j_sk_{part}_b_{side}", f"j_sk_{part}_b_dt_{side}", .5)
            # back "c" bones track at full influence, front/side at .5
            dampedTrackHelperCn(object, f"j_sk_{part}_c_{side}", f"j_sk_{part}_c_dt_{side}", 1 if part == "b" else .5)

def skirtTrack(object):
    skirtCn(object)
    muteChannels(object, "j_sk_f_a_r")
    muteChannels(object, "j_sk_s_a_r")
    muteChannels(object, "j_sk_b_a_r")
    muteChannels(object, "j_sk_f_a_l")
    muteChannels(object, "j_sk_s_a_l")
    muteChannels(object, "j_sk_b_a_l")

FRAME_TIME = 1/30

def export(startFrame, endFrame, out_bin_file):
    arm_ob = helper.detect_armature()
    scene = bpy.context.scene
    original_frame = scene.frame_current

    numFrames = endFrame - startFrame + 1          # inclusive
    duration = (numFrames - 1) * FRAME_TIME

    tracks = {b.name: [] for b in arm_ob.data.bones
              if b.name != "n_root" and not helper.is_helper_bone(b)}

    try:
        for i in range(numFrames):
            scene.frame_set(startFrame + i)
            for pb in arm_ob.pose.bones:
                if pb.name not in tracks:
                    continue
                m = (pb.parent.matrix.inverted() @ pb.matrix) if pb.parent else pb.matrix
                loc, rot, scl = m.decompose()
                t = helper.Transform()
                t.translation, t.rotation, t.scale = loc, rot, scl
                tracks[pb.name].append(t)
    finally:
        scene.frame_set(original_frame)            # don't leave the user on the last frame

    with open(out_bin_file, 'wb') as f:
        helper.write_int(f, numFrames)
        helper.write_int(f, len(tracks))
        helper.write_float(f, duration)
        for name in tracks:
            helper.write_cstring(f, name)
        for i in range(numFrames):
            for name in tracks:
                tracks[name][i].write(f)