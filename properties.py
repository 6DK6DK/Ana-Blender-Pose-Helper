import bpy

def armature_poll(self, object):
    return object.type == 'ARMATURE'
    
# unused property group in case we need to store more than just the single property for armature. 
class AnamnesisPoseProps(bpy.types.PropertyGroup):
    armature: bpy.props.PointerProperty(
        type=bpy.types.Object,
        poll=armature_poll
    )

