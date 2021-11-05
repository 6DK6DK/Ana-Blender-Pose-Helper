import bpy
import json
from os import path
from mathutils import *

class LoadAnaPose(bpy.types.Operator):
    """Load an Anamnesis .pose file to the current armature"""
    bl_idname = "pose.load_ana_pose"
    bl_label = "Load Anamnesis Pose"
    bl_options = {'REGISTER', 'UNDO'}

    filepath: bpy.props.StringProperty(subtype="FILE_PATH")
    filter_glob: bpy.props.StringProperty(
        default='*.pose',
        options={'HIDDEN'}
    )

    # don't enable the button if we don't have an armature set
    @classmethod
    def poll(cls, context):
        return context.scene.anamnesis_armature is not None
    
    def execute(self, context):
        arm = context.scene.anamnesis_armature.pose
        for bone in arm.bones:
            bpy.ops.pose.load_ana_bone('EXEC_DEFAULT', bone=bone.name, path=self.filepath)
        # rotate the whole thing to be upright, otherwise it can turn based on the transform of the armature object
        arm.bones['n_hara'].rotation_quaternion = Quaternion([1,0,0,0])
        return {'FINISHED'}

    # don't forget this so we can get the file select popup
    def invoke(self, context, event):
        bpy.context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}        
        
class LoadAnaBone(bpy.types.Operator):
    """Load a single bone from the current Anamnesis .pose file to the current armature"""
    bl_idname = "pose.load_ana_bone"
    bl_label = "Load Anamnesis Bone"
    bl_options = {'REGISTER'}
    
    bone: bpy.props.StringProperty()
    path: bpy.props.StringProperty()
    
    def execute(self, context):
        arm = context.scene.anamnesis_armature.pose

        # v1.0.1: old code for opening library file left in comment. I think the below will be more reliable, but I've used it less myself.
        # with open(bpy.utils.script_path_user() + '\\addons\\Pose_Helper\\map.json', 'r') as f:
        with open(path.join(path.dirname(__file__), 'map.json'), 'r') as f:
            name_map = json.load(f)

        with open(self.path, 'r') as f:
            pose = json.load(f)['Bones']
        
        # !!! The meat.
        bone = arm.bones[self.bone]
        if bone.name in name_map and name_map[bone.name] in pose:
            rot = pose[name_map[bone.name]]["Rotation"].split(", ")
            rot = [float(x) for x in rot]
            # .pose is XYZW, we need to switch to WXYZ
            rot.insert(0, rot.pop())
            rot = Quaternion(rot)
         
            # key blender function for transforming from the character's space to the bone's space relative to rest.
            bone.rotation_quaternion = context.object.convert_space(pose_bone = bone, matrix = rot.to_matrix().to_4x4(), from_space = 'POSE', to_space = 'LOCAL').to_quaternion()
        
        return {'FINISHED'}

classes = [
    LoadAnaPose,
    LoadAnaBone
]

def register():
    for cls in classes:
        bpy.utils.register_class(cls)

def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)

