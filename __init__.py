bl_info = {
    'name': 'Pose Helper',
    'category': 'All',
    'version': (1, 0, 2),
    'blender': (2, 93, 1)
}

import bpy
from . import ui
from . import operators
# from .properties import AnamnesisPoseProps

def armature_poll(self, object):
    return object.type == 'ARMATURE'

def register():

    # The data we need to store is attached to the scene. It feels a little high level, but I don't know anywhere else that would be a more specific fit. An unused property group is left here in case you need to store more data in the future (import/export options); it would be cleaner to get that stuff out of init. That data may also be better suited to preferences, a future decision.
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
