"""
ARA Rig Manager add-on initializer
"""

bl_info = {
    "name": "ARA Rig Manager",
    "author": "tosek",
    "version": (0, 3, 0),
    "blender": (2, 80, 0),
    "location": "View3D",
    "description": "Manage rig's bone groups and selection sets",
    "category": "Animation"
}

import bpy


from . import ui
from . import bone_groups
from . import selection_sets


def register():
    ui.register()
    bone_groups.ui.register()
    selection_sets.ui.register()


def unregister():
    ui.unregister()
    bone_groups.ui.unregister()
    selection_sets.ui.unregister()


if __name__ == "__main__":
    register()
