"""Bone Groups UI"""

# Import Blender Python API
import bpy
from bpy.props import StringProperty
from bpy.types import Operator, Panel
from bpy_extras.io_utils import ExportHelper, ImportHelper

# Local imports
from .helpers import *
from ..ui import ARAPanel


#----------------------------------------------------------------#
#---------------------- BONE GROUPS UI --------------------------#
#----------------------------------------------------------------#


#----------------------------------------------------------------#
#------------------------- OPERATORS ----------------------------#
#----------------------------------------------------------------#

class ARA_OT_SetBoneGroups(Operator):
    """Set and assign bone groups"""
    
    bl_idname = "ara.set_bone_groups"
    bl_label = "Set Bone Groups"
    
    def execute(self, context):
        scene = context.scene
        
        if scene.ara_source_rig != None:
            remove_existing_bone_groups([scene.ara_source_rig.name])
            create_bone_groups([scene.ara_source_rig.name], scene.ara_bone_groups)
            
            return {'FINISHED'}
        else:
            rigs = get_rigs()
            remove_existing_bone_groups(rigs)
            create_bone_groups(rigs, scene.ara_bone_groups)
            
            return {'FINISHED'}


class ARA_OT_SaveBoneGroups(Operator):
    """Save current Bone Groups in scene properties"""
    
    bl_idname = "ara.save_bone_groups"
    bl_label = "Save Bone Groups"
    
    def execute(self, context):
        scene = context.scene
        
        if scene.ara_source_rig != None:
            scene.ara_bone_groups.clear()
            
            bone_groups = get_bone_groups_data([scene.ara_source_rig.name])
            scene.ara_bone_groups.update(bone_groups)
            
            export_bone_groups(STD_BG_JSON, bone_groups)
            
            return {'FINISHED'}
        else:
            self.report({'ERROR'}, "Please select a rig!")
            
            return {'CANCELLED'}


class ARA_OT_ImportBoneGroups(Operator, ImportHelper):
    """Import Bone Groups from a specified JSON file"""
    
    bl_idname = "ara.import_bone_groups"
    bl_label = "Import Bone Groups"
    
    filename_ext = ".json"
    
    filet_glob: StringProperty(
        default="*.json",
        options={'HIDDEN'},
        maxlen=255
    )
    
    def execute(self, context):
        scene = context.scene
        
        if scene.ara_source_rig != None:
            return import_bone_groups(self.filepath, [scene.ara_source_rig.name])
        else:
            return import_bone_groups(self.filepath, get_rigs())


class ARA_OT_ExportBoneGroups(Operator, ExportHelper):
    """Export Bone Groups to a specified JSON file"""
    
    bl_idname = "ara.export_bone_groups"
    bl_label = "Export Bone Groups"
    
    filename_ext = ".json"
    
    filter_glob: StringProperty(
        default="*.json",
        options={'HIDDEN'},
        maxlen=255
    )
    
    def execute(self, context):
        scene = context.scene
        
        if scene.ara_source_rig != None:
            bone_groups = get_bone_groups_data([scene.ara_source_rig.name])
            
            return export_bone_groups(self.filepath, bone_groups)
        else:
            rigs = get_rigs()
            bone_groups = get_bone_groups_data(rigs)
            
            return export_bone_groups(self.filepath, bone_groups)

#----------------------------------------------------------------#
#-------------------------- PANELS ------------------------------#
#----------------------------------------------------------------#

class ARA_PT_MenuBoneGroupsMain(Panel, ARAPanel):
    """Bone Groups Manager UI Panel"""
    
    bl_label = "Bone Groups"
    bl_parent_id = "ARA_PT_MenuMain"
    
    def draw(self, context):
        layout = self.layout
        scene = context.scene
        ara_properties = scene.ara_properties
        
        layout.prop(ara_properties, "external_bone_groups", text="External Bone Groups")
        
        col = layout.column(align=True)
        col.scale_y = 1.5
        col.label(text="Select rig")
        col.prop_search(scene, "ara_source_rig", bpy.data, "armatures", text="")
        col.separator()
        
        col = layout.column(align=True)
        col.scale_y = 1.5
        col.operator(ARA_OT_SetBoneGroups.bl_idname, text=ARA_OT_SetBoneGroups.bl_label)
        
        col = layout.column(align=True)
        col.scale_y = 1.5
        col.operator(ARA_OT_SaveBoneGroups.bl_idname, text=ARA_OT_SaveBoneGroups.bl_label)


class ARA_PT_TransferBoneGroups(Panel, ARAPanel):
    """Bone Groups Manager File Operators UI Panel"""
    
    bl_label = "Transfer Bone Groups"
    bl_parent_id = "ARA_PT_MenuBoneGroupsMain"
    
    def draw(self, context):
        layout = self.layout
        scene = context.scene
        ara_properties = scene.ara_properties
        
        layout.use_property_split = True
        layout.use_property_decorate = False
        
        col = layout.column(align=True)
        col.scale_y = 1.5
        col.operator(ARA_OT_ExportBoneGroups.bl_idname, ARA_OT_ExportBoneGroups.bl_label)
        if ara_properties.external_bone_groups == False:
            col.enable = False
        
        col = layout.column(align=True)
        col.scale_y = 1.5
        col.operator(ARA_OT_ImportBoneGroups.bl_idname, ARA_OT_ImportBoneGroups.bl_label)
        if ara_properties.external_bone_groups == False:
            col.enabled = False

#----------------------------------------------------------------#
#---------------------- CLASS REGISTRATION ----------------------#
#----------------------------------------------------------------#

classes = [
    ARA_OT_SetBoneGroups,
    ARA_OT_ExportBoneGroups,
    ARA_OT_ImportBoneGroups,
    ARA_OT_SaveBoneGroups,
    ARA_PT_MenuBoneGroupsMain,
    ARA_PT_TransferBoneGroups
]


def menu_func_export(self, context):
    self.layout.operator(ARA_OT_ExportBoneGroups.bl_idname, text="Export Bone Groups (.json)")


def menu_func_import(self, context):
    self.layout.operator(ARA_OT_ImportBoneGroups.bl_idname, text="Import Bone Groups (.json)")


def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    
    bpy.types.Scene.ara_bone_groups = read_std_bone_groups(STD_BG_JSON)
    
    bpy.types.TOPBAR_MT_file_export.append(menu_func_export)
    bpy.types.TOPBAR_MT_file_import.append(menu_func_import)


def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)
    
    del bpy.types.Scene.ara_bone_groups
    
    bpy.types.TOPBAR_MT_file_export.remove(menu_func_export)
    bpy.types.TOPBAR_MT_file_import.remove(menu_func_import)