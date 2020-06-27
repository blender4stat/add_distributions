# ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ##### END GPL LICENSE BLOCK #####

bl_info = {
    "name": "add_distributions",
    "author": "Shu Fai Cheung",
    "version": (0, 0, 1),
    "blender": (2, 80, 0),
    "description": "Create a mesh based on a probability distribution or random values generated from one",
    "warning": "Under development",
    "category": "Object",
}

import bpy

from . import (
    ui,
    prefs,
    gen_normal_points,
    gen_bivar_normal_points,
)
    
classes =  ui.classes + prefs.classes
classes += gen_normal_points.classes + gen_bivar_normal_points.classes
    
def register():
    for cls in classes:
        bpy.utils.register_class(cls)

def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)

if __name__ == "__main__":
    register()    
    
