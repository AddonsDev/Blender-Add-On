"""Bone Groups helper functions"""

# Import Blender Python API
import bpy

# Import standard library
import json

#----------------------------------------------------------------#
#------------------------- CONSTANTS ----------------------------#
#----------------------------------------------------------------#

BL_ADDONS_PATH = bpy.utils.user_resource("SCRIPTS") + "\\addons"
ADDON_DATA_PATH = BL_ADDONS_PATH + "\\ara_rig_manager\\data"
STD_BG_JSON = ADDON_DATA_PATH + "\\bone_groups.json"

#----------------------------------------------------------------#
#----------------------- PROCESS RIG DATA -----------------------#
#----------------------------------------------------------------#

def get_rigs():
    """Get all rigs present in the scene"""
    
    print("Finding rigs")
    
    armatures = bpy.data.armatures.keys()

    rigs = [armature for armature in armatures if "meta" not in armature]
    
    return rigs



def get_bone_groups_data(rigs):
    """Get bone groups data from all the rigs present in the scene"""
    
    print("Gathering bone groups data")
    
    bone_groups_dict = {}

    for rig in rigs:
        bone_groups = bpy.data.objects[rig].pose.bone_groups
        for bone_group in bone_groups:
            bone_group_object = bpy.data.objects[rig].pose.bone_groups[bone_group.name]
            save_color_mode_and_colors(bone_groups_dict, bone_group.name, bone_group_object)
            get_bone_names(bone_groups_dict, bone_groups, bone_group)
    
    return bone_groups_dict


def save_color_mode_and_colors(bone_groups_dict, bone_group, bone_group_object):
    """Save bone groups color modes and colors"""
    
    bg_color_normal = bone_group_object.colors.normal.hsv
    bg_color_select = bone_group_object.colors.select.hsv
    bg_color_active = bone_group_object.colors.active.hsv
    bg_color_mode = bone_group_object.color_set
    bone_groups_dict[bone_group] = {}
    bone_groups_dict[bone_group]['MODE'] = bg_color_mode
    bone_groups_dict[bone_group]['NORMAL'] = bg_color_normal
    bone_groups_dict[bone_group]['SELECT'] = bg_color_select
    bone_groups_dict[bone_group]['ACTIVE'] = bg_color_active


def get_bone_names(bone_groups_dict, bone_groups, bone_group):
    """Get bone names of assigned bones of each bone group"""
    
    bone_groups.active = bone_group
    bpy.ops.pose.group_select()
            
    selected_bones = bpy.context.selected_pose_bones
    bone_groups_dict[bone_group.name]['BONES'] = []
    for selected_bone in selected_bones:
        bone_groups_dict[bone_group.name]['BONES'].append(selected_bone.name)
            
    bpy.ops.pose.group_deselect()



def remove_existing_bone_groups(rigs):
    """Remove existing bone groups"""
    
    print("Removing existing bone groups")
    
    for rig in rigs:
        bone_groups = bpy.data.objects[rig].pose.bone_groups.values()
        for bone_group in bone_groups:
            bpy.data.objects[rig].pose.bone_groups.remove(bone_group)



def create_bone_groups(rigs, bone_groups):
    """Create bone groups for rigs with presented bone groups data"""    
    
    print("Creating new bone groups with imported data")
    
    for rig in rigs:
        for index, bone_group in enumerate(bone_groups):
            index += 1
            assign_colors_to_bone_groups(bone_groups, rig, bone_group)
            assign_bones_to_bone_groups(bone_groups, rig, index, bone_group)
            bpy.ops.pose.group_deselect()


def assign_colors_to_bone_groups(bone_groups, rig, bone_group):
    """Assign colors and color modes to respective bone groups"""
    
    bpy.data.objects[rig].pose.bone_groups.new(name=bone_group)
    bone_group_object = bpy.data.objects[rig].pose.bone_groups[bone_group]
    bone_group_object.color_set = bone_groups[bone_group]['MODE']
    bone_group_object.colors.normal.hsv = bone_groups[bone_group]['NORMAL']
    bone_group_object.colors.select.hsv = bone_groups[bone_group]['SELECT']
    bone_group_object.colors.active.hsv = bone_groups[bone_group]['ACTIVE']        


def assign_bones_to_bone_groups(bone_groups, rig, index, bone_group):
    """Assign bones to respective bone groups"""
    
    curr_bones = bpy.data.objects[rig].pose.bones.keys()

    for bone in bone_groups[bone_group]['BONES']:
        if bone in curr_bones:
            selected_bone = bpy.data.objects[bpy.context.object.name].pose.bones[bone].bone
            bpy.context.object.data.bones.active = selected_bone
            selected_bone.select = True
    
    bpy_bone_groups = bpy.data.objects[rig].pose.bone_groups
    bpy_bone_groups.active = bpy_bone_groups[bone_group]
    bpy.ops.pose.group_select()
    bpy.ops.pose.group_assign(type=index)

#----------------------------------------------------------------#
#----------------------- FILE HANDLING --------------------------#
#----------------------------------------------------------------#

def import_bone_groups(filepath, rigs):
    """Import bone groups from .JSON file"""
    
    print("Importing bone groups data from external file")
    
    remove_existing_bone_groups(rigs)
    
    file = open(filepath, 'r', encoding='utf-8')
    imported_bone_groups = json.load(file)
    file.close()
    
    create_bone_groups(rigs, imported_bone_groups)
    
    return {'FINISHED'}



def export_bone_groups(filepath, bone_groups):  
    """Export bone groups to .JSON file"""
    
    print("Exporting bone groups data")
    
    file = open(filepath, 'w', encoding='utf-8')
    json.dump(bone_groups, file)
    file.close()
    
    return {'FINISHED'}



def read_std_bone_groups(filepath):
    """Read standard bone groups JSON file and return a dictionary"""
    
    file = open(filepath, 'r', encoding='utf-8')
    std_bone_groups = json.load(file)
    file.close()
    
    return std_bone_groups