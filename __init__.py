bl_info = {
    'name': 'Pose Helper BETA',
    'category': 'All',
    'version': (0, 0, 1),
    'blender': (2, 93, 1)
}

import bpy
from . import ui
from . import operators
# from .properties import AnamnesisPoseProps

def armature_poll(self, object):
    return object.type == 'ARMATURE'

def register():
    bpy.types.Scene.anamnesis_armature = bpy.props.PointerProperty(
        type=bpy.types.Object,
        poll=armature_poll
    )
    # bpy.types.Scene.anamnesis_props = bpy.props.CollectionProperty(type=AnamnesisPoseProps)
    ui.register()
    operators.register()

def unregister():
    ui.unregister()
    operators.unregister()
 
if __name__ == "__main__":
    register()
