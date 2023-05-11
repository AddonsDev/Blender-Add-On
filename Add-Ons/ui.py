import bpy
from bpy.props import BoolProperty, PointerProperty, StringProperty
from bpy.types import Panel, PropertyGroup


#----------------------------------------------------------------#
#--------------------- ARA RIG MANAGER UI -----------------------#
#----------------------------------------------------------------#

class ARAPanel:
    """ARA Rig Manager UI Panel"""
    
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "ARA"
    bl_context = "posemode"


class ARA_PT_MenuMain(Panel, ARAPanel):
    """ARA Rig Manager Main Menu Panel"""
    
    bl_label = "ARA Rig Manager"
    
    def draw(self, context):
        layout = self.layout
        scene = context.scene
        ara_properties = scene.ara_properties


class ARA_Properties(PropertyGroup):
    """ARA Rig Manager Properties"""
    
    external_bone_groups: BoolProperty(
        name="External Bone Groups",
        description="Enable import and export of bone groups",
        default=False
    )
    
    external_selection_sets: BoolProperty(
        name="External Selection Sets",
        description="Enable import and export of selection sets",
        default=False
    )

#----------------------------------------------------------------#
#---------------------- CLASS REGISTRATION ----------------------#
#----------------------------------------------------------------#

classes = [
    ARA_Properties,
    ARA_PT_MenuMain
]


def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    
    bpy.types.Scene.ara_source_rig = PointerProperty(type=bpy.types.Armature)
    bpy.types.Scene.ara_properties = PointerProperty(type=ARA_Properties)


def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)
    
    del bpy.types.Scene.ara_source_rig
    del bpy.types.Scene.ara_properties