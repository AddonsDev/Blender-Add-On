"""Selection Sets helper functions"""

# Import Blender Python API
import bpy

# Import standard library
import json

#----------------------------------------------------------------#
#------------------------- CONSTANTS ----------------------------#
#----------------------------------------------------------------#

BL_ADDONS_PATH = bpy.utils.user_resource("SCRIPTS") + "\\addons"
ADDON_DATA_PATH = BL_ADDONS_PATH + "\\ara_rig_manager\\data"
STD_SS_JSON = ADDON_DATA_PATH + "\\selection_sets.json"

#----------------------------------------------------------------#
#---------------------- PROCESS RIG DATA ------------------------#
#----------------------------------------------------------------#

def get_rigs():
    """Get all rigs present in the scene"""
    
    print("Finding rigs")
    
    armatures = bpy.data.armatures.keys()

    rigs = [armature for armature in armatures if "meta" not in armature]
    
    return rigs


def get_selection_sets():
    """Get selection sets of selected rig"""
    
    print("Getting current selection sets")
    
    selection_sets = bpy.context.object.selection_sets
    
    return selection_sets


def get_selection_sets_data(selection_sets):
    """Get selection sets data of selected rig"""
    
    print("Gathering data of current selection sets")
    
    selections = {}
    
    for selection_set in selection_sets:
        ss_name = selection_set.name
        bones = []
        for bone in selection_set.bone_ids:
            bones.append(bone.name)
        selections[ss_name] = bones
    
    return selections


def remove_selection_sets():
    """Remove present selection sets"""
    
    print("Removing current selection sets from the rig")
    
    selection_sets = get_selection_sets()
    
    while len(selection_sets) != 0:
        bpy.ops.pose.selection_set_remove()


def create_selection_sets(selection_sets):
    """Create selection sets with presented data"""
    
    print("Creating selection sets for the rig")
    
    rig = get_rigs()
    curr_bones = bpy.data.objects[rig[0]].pose.bones.keys()
    
    for index, selection_set in enumerate(selection_sets):
        bpy.ops.pose.selection_set_add()
        bpy.context.object.active_selection_set = index
        bpy.context.object.selection_sets[index].name = selection_set
        
        for bone in selection_sets[selection_set]:
            if bone in curr_bones:
                selected_bone = bpy.data.objects[bpy.context.object.name].pose.bones[bone].bone
                bpy.context.object.data.bones.active = selected_bone
                selected_bone.select = True
        
        bpy.ops.pose.selection_set_assign()
        bpy.ops.pose.selection_set_select()
        bpy.ops.pose.selection_set_deselect()

#----------------------------------------------------------------#
#------------------------ FILE HANDLING -------------------------#
#----------------------------------------------------------------#

def export_selection_sets(filepath):
    """Export selection sets to a JSON file"""
    
    selection_sets = get_selection_sets()
    selection_sets_data = get_selection_sets_data(selection_sets)
    
    file = open(filepath, 'w', encoding='utf-8')
    json.dump(selection_sets_data, file)
    file.close()
    
    return {'FINISHED'}


def import_selection_sets(filepath):
    """Import selection sets from a JSON file"""
    
    remove_selection_sets()
    
    file = open(filepath, 'r', encoding='utf-8')
    imported_selection_sets = json.load(file)
    file.close()
    
    create_selection_sets(imported_selection_sets)
    
    return {'FINISHED'}


def read_std_selection_sets(filepath):
    """Import standard selection sets and return a dictionary"""
    
    file = open(filepath, 'r', encoding='utf-8')
    std_selection_sets = json.load(file)
    file.close()
    
    return std_selection_sets