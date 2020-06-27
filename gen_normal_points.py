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

# Generate the points on the density function.

import bpy
from scipy.stats import norm
import numpy as np
from bpy.props import StringProperty, IntProperty, BoolProperty, FloatProperty, EnumProperty


class add_pdf_normal(bpy.types.Operator):
    """Add a normal curve"""
    bl_idname = "object.add_pdf_normal"
    bl_label = "Add a normal curve"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):   

        scale_x = 3
        scale_z = 12

        npoints = context.preferences.addons['add_distributions'].preferences.ncases

        x = np.linspace(-9, 9, npoints)
        z = scale_z * norm.pdf(x / scale_x)

        mesh        = bpy.data.meshes.new("normal_curve")
        object      = bpy.data.objects.new(mesh.name, mesh)
        collection  = bpy.data.collections.get("Collection")
        collection.objects.link(object)
        bpy.context.view_layer.objects.active = object

        vertices_all = list(zip(x, [0] * npoints, z))
        edges_all = list(zip(range(0, npoints - 1), range(1, npoints)))
        faces_all = []

        mesh.from_pydata(vertices_all, edges_all, faces_all)

        return {'FINISHED'}     
        
classes = (
    add_pdf_normal,
)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)

def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)

if __name__ == "__main__":
    register()    
    