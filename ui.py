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

import bpy
from bpy.types import Panel

class OBJECT_PT_add_distributions(Panel):
    bl_label = "Add a Distribution"
    bl_idname = "OBJECT_PT_add_distributions"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "scene"

    def draw(self, context):
        layout = self.layout
        row = layout.row()
        btn_pdf_normal = row.operator("object.add_pdf_normal")
        row = layout.row()
        row.operator("object.add_pdf_bivar_normal")
        
classes = (
    OBJECT_PT_add_distributions,
)
             
def register():
    bpy.utils.register_class(OBJECT_PT_add_distributions)


def unregister():
    bpy.utils.unregister_class(OBJECT_PT_add_distributions)
    
