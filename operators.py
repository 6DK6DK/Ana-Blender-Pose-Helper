import bpy
import json
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
    
    def execute(self, context):
        arm = context.scene.anamnesis_armature.pose
        for bone in arm.bones:
            bpy.ops.pose.load_ana_bone('EXEC_DEFAULT', bone=bone.name, path=self.filepath)
        arm.bones['n_hara'].rotation_quaternion = Quaternion([1,0,0,0])
        return {'FINISHED'}

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

        with open('.\map.json', 'r') as f:
            name_map = json.load(f)

        with open(self.path, 'r') as f:
            pose = json.load(f)['Bones']
        
        bone = arm.bones[self.bone]
        if bone.name in name_map and name_map[bone.name] in pose:
            rot = pose[name_map[bone.name]]["Rotation"].split(", ")
            rot = [float(x) for x in rot]
            rot.insert(0, rot.pop())
            rot = Quaternion(rot)
         
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

