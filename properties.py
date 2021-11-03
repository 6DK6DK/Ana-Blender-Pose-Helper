import bpy

class AnamnesisPoseProps(bpy.types.PropertyGroup):
    armature: bpy.props.CollectionProperty(type = bpy.types.Armature)

