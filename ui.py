import bpy

class PH_PoseHelper(bpy.types.Panel):
    bl_idname = "PH_PT_PoseHelper"
    bl_label = "Pose Helper"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Pose Helper"

    def draw(self, context):
        layout = self.layout

        scene = context.scene

        # layout.label(text="Hello Pose Helper!")
        layout.prop(scene, "anamnesis_armature")
        layout.operator("pose.load_ana_pose")

class PH_Import(bpy.types.Panel):
    bl_idname = "PH_PT_Import"
    bl_label = "Import"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Pose Helper"
    bl_parent_id = "PH_PT_PoseHelper"

    def draw(self, context):
        layout = self.layout

        scene = context.scene


        # column.prop(scene, "armature")

class PH_Export(bpy.types.Panel):
    bl_idname = "PH_PT_Export"
    bl_label = "Export"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Pose Helper"
    bl_parent_id = "PH_PT_PoseHelper"

    def draw(self, context):
        layout = self.layout

        layout.label(text="Hello Export!")

classes = [
    PH_PoseHelper,
    # PH_Import,
    # PH_Export
]

def register():
    for cls in classes:
        bpy.utils.register_class(cls)

def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)

