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
#--------------------- SELECTION SETS UI ------------------------#
#----------------------------------------------------------------#


#----------------------------------------------------------------#
#------------------------- OPERATORS ----------------------------#
#----------------------------------------------------------------#

class ARA_OT_SaveSelectionSets(Operator):
    """Save current rig's selection sets"""
    
    bl_idname = "ara.save_selection_sets"
    bl_label = "Save Selection Sets"
    
    def execute(self, context):
        scene = context.scene
        
        scene.ara_selection_sets.clear()
        
        selection_sets = get_selection_sets()
        selection_sets_data = get_selection_sets_data(selection_sets)
        
        scene.ara_selection_sets.update(selection_sets_data)
        export_selection_sets(STD_SS_JSON)
        
        return {'FINISHED'}


class ARA_OT_SetSelectionSets(Operator):
    """Set selection sets for current rig"""
    
    bl_idname = "ara.set_selection_sets"
    bl_label = "Set Selection Sets"
    
    def execute(self, context):
        scene = context.scene
        
        remove_selection_sets()
        create_selection_sets(scene.ara_selection_sets)
        
        return {'FINISHED'}


class ARA_OT_ExportSelectionSets(Operator, ExportHelper):
    """Export selection sets to a specified JSON file"""
    
    bl_idname = "ara.export_selection_sets"
    bl_label = "Export Selection Sets"
    
    filename_ext = ".json"
    
    filter_glob: StringProperty(
        default="*.json",
        oprtions={'HIDDEN'},
        maxlen=255
    )
    
    def execute(self, context):
        scene = context.scene
        
        return export_selection_sets(self.filepath)


class ARA_OT_ImportSelectionSets(Operator, ImportHelper):
    """Import Selection Sets from a specified JSON file"""
    
    bl_idname = "ara.import_selection_sets"
    bl_label = "Import Selection Sets"
    
    filename_ext = ".json"
    
    filter_glob: StringProperty(
        default="*.json",
        options={'HIDDEN'},
        maxlen=255
    )
    
    def execute(self, context):
        scene = context.scene
        
        return import_selection_sets(self.filepath)

#----------------------------------------------------------------#
#-------------------------- PANELS ------------------------------#
#----------------------------------------------------------------#

class ARA_PT_MenuSelectionSets(Panel, ARAPanel):
    """Selection Sets Manager UI Panel"""
    
    bl_label = "Selection Sets"
    bl_parent_id = "ARA_PT_MenuMain"
    
    def draw(self, context):
        layout = self.layout
        scene = context.scene
        ara_properties = scene.ara_properties
        
        layout.prop(ara_properties, "external_selection_sets", text="External Selection Sets")
        
        col = layout.column(align=True)
        col.scale_y = 1.5
        col.operator(ARA_OT_SaveSelectionSets.bl_idname, ARA_OT_SaveSelectionSets.bl_label)
        
        col = layout.column(align=True)
        col.scale_y = 1.5
        col.operator(ARA_OT_SetSelectionSets.bl_idname, ARA_OT_SetSelectionSets.bl_label)


class ARA_PT_TransferSelectionSets(Panel, ARAPanel):
    """Selection Sets Transfer UI Panel"""
    
    bl_label = "Transfer Selection Sets"
    bl_parent_id = "ARA_PT_MenuSelectionSets"
    
    def draw(self, context):
        layout = self.layout
        scene = context.scene
        ara_properties = scene.ara_properties
        
        col = layout.column(align=True)
        col.scale_y = 1.5
        col.operator(ARA_OT_ExportSelectionSets.bl_idname, text=ARA_OT_ExportSelectionSets.bl_label)
        if ara_properties.external_selection_sets == False:
            col.enabled = False
        
        col = layout.column(align=True)
        col.scale_y = 1.5
        col.operator(ARA_OT_ImportSelectionSets.bl_idname, text=ARA_OT_ImportSelectionSets.bl_label)
        if ara_properties.external_selection_sets == False:
            col.enabled = False

#----------------------------------------------------------------#
#---------------------- CLASS REGISTRATION ----------------------#
#----------------------------------------------------------------#

classes = [
    ARA_OT_ExportSelectionSets,
    ARA_OT_ImportSelectionSets,
    ARA_OT_SaveSelectionSets,
    ARA_OT_SetSelectionSets,
    ARA_PT_MenuSelectionSets,
    ARA_PT_TransferSelectionSets
]


def menu_func_export(self, context):
    self.layout.operator(ARA_OT_ExportSelectionSets.bl_idname, text="Export Selection Sets (.json)")


def menu_func_import(self, context):
    self.layout.opertaor(ARA_OT_ImportSelectionSets.bl_idname, text="Import Selection Sets (.json)")


def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    
    bpy.types.Scene.ara_selection_sets = read_std_selection_sets(STD_SS_JSON)

    bpy.types.TOPBAR_MT_file_export.append(menu_func_export)
    bpy.types.TOPBAR_MT_file_import.append(menu_func_import)


def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)
    
    del bpy.types.Scene.ara_selection_sets
    
    bpy.types.TOPBAR_MT_file_export.remove(menu_func_export)
    bpy.types.TOPBAR_MT_file_import.remove(menu_func_import)
