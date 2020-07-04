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
from numpy.random import MT19937
from numpy.random import RandomState, SeedSequence


class add_rnd_normal(bpy.types.Operator):
    """Add a histogram of random normal data"""
    bl_idname = "object.add_random_normal"
    bl_label = "Add a histogram of random normal data"
    bl_options = {'REGISTER', 'UNDO'}
    
    npoints: IntProperty(
        name = "Number of points",
        default = 100,
        min = 10,
        soft_min = 10,
    )
    xmean: FloatProperty(
        name = "Mean",
        default = 0,
    )
    xsd: FloatProperty(
        name = "Standard deviation",
        default = 1,
        min = 0,
        soft_min = 0,
    )
    xmin: FloatProperty(
        name = "Minimum of X",
        default = -3,
    )
    xmax: FloatProperty(
        name = "Maximum of X",
        default =  3,
    )
    zscale: FloatProperty(
        name = "Scale for Z axis",
        default = 10,
        min = 0,
        soft_min = 0,
    )
    jointpoints: BoolProperty(
        name = "Joint the points",
        default = True,
    )
    seed: IntProperty(
        name = "Random seed",
        default = 0,
        min = 0,
        soft_min = 0,
    )
    nbins: IntProperty(
        name = "Number of bins",
        default = 10,
        min = 2,
        soft_min = 3,
    )
#    range_lo: FloatProperty(
#        name = "Range minimum",
#        default = None,
#    )
#    range_hi: FloatProperty(
#        name = "Range maximum",
#        default = None,
#    )
    addfaces: BoolProperty(
        name = "Add faces",
        default = True,
    )
    
    def execute(self, context):   

        if self.seed > 0:
            rs = RandomState(MT19937(SeedSequence(self.seed)))
    
        n = self.npoints
        nbins = self.nbins
        
        # x = np.linspace(self.xmin, self.xmax, n)
        x = np.random.normal(self.xmean, self.xsd, n)
        print(x)
        x_hist, x_bins = np.histogram(x, bins = nbins, 
                                      density = True)
        x_hist = x_hist * self.zscale
        # z = self.zscale * norm.pdf(x * self.xsd)

        mesh        = bpy.data.meshes.new("normal_curve")
        object      = bpy.data.objects.new(mesh.name, mesh)
        collection  = bpy.data.collections.get("Collection")
        collection.objects.link(object)
        object.location = bpy.context.scene.cursor.location
        bpy.context.view_layer.objects.active = object

              
        vertices_all = list()
        face_vertices = list()
        for i in range(nbins):
            vertices_all.append((x_bins[i],     0, 0))
            vertices_all.append((x_bins[i],     0, x_hist[i]))
            vertices_all.append((x_bins[i + 1], 0, x_hist[i]))
            vertices_all.append((x_bins[i + 1], 0, 0))        
            j = i * 4
            face_vertices.append((j, j + 1, j + 2, j + 3))
            
        n_vertices = len(vertices_all)
        if (self.jointpoints):
            edges_all = list(zip(range(0, n_vertices - 1), range(1, n_vertices)))
            edges_all += [(j * 4, j * 4 + 3) for j in range(nbins)]
        else:
            edges_all = []
        
        if (self.addfaces):
            faces_all = face_vertices
        else:
            faces_all = []

        mesh.from_pydata(vertices_all, edges_all, faces_all)

        return {'FINISHED'}     

    def invoke(self, context, event):
        wm = context.window_manager
        return wm.invoke_props_dialog(self)    
    
    def draw(self, context):
        layout = self.layout
        col = layout.column()
        col.prop(self, "npoints")
        col.prop(self, "xmean")
        col.prop(self, "xsd")
        row = layout.row()
#        row.prop(self, "range_lo")
#        row.prop(self, "range_hi")
        col = layout.column()
        col.prop(self, "nbins")
        col.prop(self, "zscale")
        col.prop(self, "jointpoints")
        col.prop(self, "addfaces")
        col.prop(self, "seed")
            
        
classes = (
    add_rnd_normal,
)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)

def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)

if __name__ == "__main__":
    register()    
    