import bpy

# everything meaningful currently lives in this class, the two subpanels are commented out of register(). It may be useful to turn them into their own panels if they get enough content to be worth collapsing.
class PH_PoseHelper(bpy.types.Panel):
    bl_idname = "PH_PT_PoseHelper"
    bl_label = "Pose Helper"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Pose Helper"

    def draw(self, context):
        layout = self.layout

        scene = context.scene

        layout.prop(scene, "anamnesis_armature", text="Armature")
        layout.operator("pose.load_ana_pose", text="Import")
        layout.operator("pose.export_ana_pose", text="Export")

# UNUSED
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

# UNUSED
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

