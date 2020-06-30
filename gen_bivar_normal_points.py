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
from scipy.stats import multivariate_normal
import numpy as np

class add_pdf_bivar_normal(bpy.types.Operator):
    """Add a bivariate normal curve"""
    bl_idname = "object.add_pdf_bivar_normal"
    bl_label = "Add a bivariate normal surface"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):   

        npoints = context.preferences.addons['add_distributions'].preferences.ncases
        npoints = int(npoints ** .5)
        d = 6 / npoints
        
        x, y = np.mgrid[-3:(3 + d):d, -3:(3 + d):d]
        side_size = x.shape[0]
        coord = np.empty(x.shape + (2, ))
        coord[:, :, 0] = x
        coord[:, :, 1] = y
        cov_xy = .8
        var = multivariate_normal([0.0, 0.0], [[1.0, cov_xy], [cov_xy, 1.0]])
        z = var.pdf(coord)

        z_scale = 10

        mesh        = bpy.data.meshes.new("bivar_normal_curve")
        object      = bpy.data.objects.new(mesh.name, mesh)
        collection  = bpy.data.collections.get("Collection")
        collection.objects.link(object)
        object.location = bpy.context.scene.cursor.location
        bpy.context.view_layer.objects.active = object

        vertices_all = list(zip(x.flatten(), y.flatten(), z_scale*z.flatten()))
        edges_all = []

        face_index = np.array(range(0, (side_size * side_size)))
        face_index = face_index.reshape((side_size, side_size))
        face_index = face_index[0:(side_size - 1),0:(side_size - 1)].flatten()
        face_vertices = list()
        for i in face_index:
            face_vertices.append((i, i + 1, i + side_size + 1, i + side_size))
        faces_all = face_vertices

        mesh.from_pydata(vertices_all, edges_all, faces_all)

        return {'FINISHED'}     
        

classes = (
    add_pdf_bivar_normal,
)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)

def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)

if __name__ == "__main__":
    register()    
    