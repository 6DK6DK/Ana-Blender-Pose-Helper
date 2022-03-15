import bpy
import json
from os import path
from mathutils import *
from bpy_extras.io_utils import ExportHelper

class LoadAnaPose(bpy.types.Operator):
    """Load an Anamnesis .pose file to the current armature"""
    bl_idname = "pose.load_ana_pose"
    bl_label = "Import"
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

        # support for proper bone orientations: get diff from original
        arm.bones['n_hara'].matrix_basis = Matrix()
        # axis-angle form of the diff quaternion we want to pass to each individual bone operation. shorthand to pack into a float vector property; this seems silly?
        aa = Quaternion([1,0,0,0]).rotation_difference(arm.bones['n_hara'].matrix.to_quaternion()).to_axis_angle()
        diff = [aa[0][0], aa[0][1], aa[0][2], aa[1]]

        for bone in arm.bones:
            bpy.ops.pose.load_ana_bone('EXEC_DEFAULT', bone=bone.name, path=self.filepath, diff=diff)
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
    diff: bpy.props.FloatVectorProperty(size=4)
    
    def execute(self, context):
        arm = context.scene.anamnesis_armature.pose

        with open(path.join(path.dirname(__file__), 'map.json'), 'r') as f:
            name_map = json.load(f)

        with open(self.path, 'r') as f:
            pose = json.load(f)['Bones']

        # check if the first bone in the pose file is in the map to determine legacy
        legacy = False
        if list(pose.keys())[0] in name_map.values():
            legacy = True

        # !!! The meat.
        bone = arm.bones[self.bone]
        # fucky legacy check switch thing to avoid redundant code
        rot = False
        if legacy and bone.name in name_map and name_map[bone.name] in pose:
            rot = pose[name_map[bone.name]]
        elif bone.name in pose:
            rot = pose[bone.name]

        if rot:
            rot = rot["Rotation"].split(", ")
            rot = [float(x) for x in rot]
            # .pose is XYZW, we need to switch to WXYZ
            rot.insert(0, rot.pop())
            diff = Quaternion(self.diff[0:3], self.diff[3])
            rot = Quaternion(rot) @ diff
            # key blender function for transforming from the character's space to the bone's space relative to rest.
            bone.rotation_quaternion = context.scene.anamnesis_armature.convert_space(pose_bone = bone, matrix = rot.to_matrix().to_4x4(), from_space = 'POSE', to_space = 'LOCAL').to_quaternion()
        
        return {'FINISHED'}

class ExportAnaPose(bpy.types.Operator, ExportHelper):
    """Export an Anamnesis .pose file from the current armature's pose"""
    bl_idname = "pose.export_ana_pose"
    bl_label = "Export"
    bl_options = {'REGISTER', 'UNDO'}

    filepath: bpy.props.StringProperty(subtype="FILE_PATH")
    filename_ext='.pose'
    filter_glob: bpy.props.StringProperty(
        default='*.pose',
        options={'HIDDEN'}
    )

    #don't enable the button if we don't have an armature set
    @classmethod
    def poll(cls, context):
        return context.scene.anamnesis_armature is not None

    def execute(self, context):
        arm = context.scene.anamnesis_armature.pose

        with open(self.filepath, 'w') as f:
            json_dict = {
                "FileExtension": ".pose",
                "TypeName": "Anamnesis Pose",
                "Bones": {}
            }

            for bone in arm.bones:
                quat = bone.matrix.to_quaternion()
                rot = "{0}, {1}, {2}, {3}".format(quat.x, quat.y, quat.z, quat.w)
                bone_dict = {
                    bone.name: {
                        "Rotation": rot
                    }
                }
                json_dict['Bones'].update(bone_dict)
            
            json.dump(json_dict, f)
            return {'FINISHED'}

    # def invoke(self, context, event):
    #     bpy.context.window_manager.fileselect_add(self)
    #     return {'RUNNING_MODAL'}
            

classes = [
    LoadAnaPose,
    LoadAnaBone,
    ExportAnaPose
]

def register():
    for cls in classes:
        bpy.utils.register_class(cls)

def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)

