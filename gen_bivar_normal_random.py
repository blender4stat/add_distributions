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
from bpy.props import StringProperty, IntProperty, BoolProperty, FloatProperty, EnumProperty
from numpy.random import MT19937
from numpy.random import RandomState, SeedSequence

class add_random_bivar_normal(bpy.types.Operator):
    """Add a 2D histogram of bivariate normal data"""
    bl_idname = "object.add_random_bivar_normal"
    bl_label = "Add a 2D histogram of bivariate normal data"
    bl_options = {'REGISTER', 'UNDO'}

    npoints: IntProperty(
        name = "Number of points",
        default = 100,
        min = 5,
        soft_min = 5,
    )
    xmean: FloatProperty(
        name = "Mean of X",
        default = 0,
    )
    ymean: FloatProperty(
        name = "Mean of Y",
        default = 0,
    )
    xsd: FloatProperty(
        name = "SD of X",
        default = 1,
    )
    ysd: FloatProperty(
        name = "SD of Y",
        default = 1,
    )
    vmin: FloatProperty(
        name = "Minimum of each variable",
        default = -3,
    )
    vmax: FloatProperty(
        name = "Maximum of each variable",
        default =  3,
    )
    xycor: FloatProperty(
        name = "Correlation between X and Y",
        default =  .8,
        min = -.99,
        max =  .99,
        soft_min = -.99,
        soft_max =  .99,
    )
    zscale: FloatProperty(
        name = "Scale for Z axis",
        default = 12,
        min = 0,
        soft_min = 0,
    )    
    addface: BoolProperty(
        name = "Add faces",
        default = True,
    )
    seed: IntProperty(
        name = "Random seed",
        default = 0,
        min = 0,
        soft_min = 0,
    )
    xnbins: IntProperty(
        name = "Number of bins for X",
        default = 10,
        min = 2,
        soft_min = 3,
    )
    ynbins: IntProperty(
        name = "Number of bins for Y",
        default = 10,
        min = 2,
        soft_min = 3,
    )
    
    def execute(self, context):   

        if self.seed > 0:
            rs = RandomState(MT19937(SeedSequence(self.seed)))
    
        n = self.npoints
        #d = (self.vmax - self.vmin) / self.npoints
        xymean = [self.xmean, self.ymean]
        xycov = [[self.xsd ** 2, self.xycor * self.xsd * self.ysd], 
                 [self.xycor * self.xsd * self.ysd, self.ysd ** 2]]
        dat = np.random.multivariate_normal(xymean,
                                            xycov,
                                            n)
        xynbins = [self.xnbins, self.ynbins]
        
        xy_hist, x_bins, y_bins = np.histogram2d(dat[:, 0], dat[:, 1],
                                                 bins = xynbins,
                                                 density = True)
        xy_hist = xy_hist * self.zscale

        # x, y = np.mgrid[self.vmin:(self.vmax + d):d, self.vmin:(self.vmax + d):d]
        # side_size = x.shape[0]
        # coord = np.empty(x.shape + (2, ))
        # coord[:, :, 0] = x
        # coord[:, :, 1] = y
        # cov_xy = self.vcov
        # var = multivariate_normal([0.0, 0.0], [[1.0, cov_xy], [cov_xy, 1.0]])
        # z = var.pdf(coord)

#        z_scale = 10

        mesh        = bpy.data.meshes.new("bivar_normal_curve")
        object      = bpy.data.objects.new(mesh.name, mesh)
        collection  = bpy.data.collections.get("Collection")
        collection.objects.link(object)
        object.location = bpy.context.scene.cursor.location
        bpy.context.view_layer.objects.active = object

        vertices_all = list()
        face_vertices = list()
        k = 0
        
        for i in range(xynbins[0]):
            for j in range(xynbins[1]):
                vertices_temp = [(x_bins[i],     y_bins[j],     0),
                                 (x_bins[i + 1], y_bins[j],     0),
                                 (x_bins[i + 1], y_bins[j + 1], 0),
                                 (x_bins[i],     y_bins[j + 1], 0),
                                 (x_bins[i],     y_bins[j],     xy_hist[i, j]),
                                 (x_bins[i + 1], y_bins[j],     xy_hist[i, j]),
                                 (x_bins[i + 1], y_bins[j + 1], xy_hist[i, j]),
                                 (x_bins[i],     y_bins[j + 1], xy_hist[i, j])]
                vertices_all += vertices_temp
                face_vertices_temp = [(k,     k + 1, k + 2, k + 3),
                                      (k + 4, k + 5, k + 6, k + 7),
                                      (k,     k + 1, k + 5, k + 4),
                                      (k + 1, k + 2, k + 6, k + 5),
                                      (k + 2, k + 3, k + 7, k + 6),
                                      (k + 3, k    , k + 4, k + 7)]
                face_vertices += face_vertices_temp
                k += 8
        
        edges_all = []

        if (self.addface):
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
        col.prop(self, "vcov")
        row = layout.row()
        row.prop(self, "xmean")
        row.prop(self, "ymean")
        row = layout.row()
        row.prop(self, "xsd")
        row.prop(self, "ysd")
        row = layout.row()
        row.prop(self, "xycor")
        row = layout.row()
        row.prop(self, "xnbins")
        row.prop(self, "ynbins")
        col = layout.column()
        col.prop(self, "zscale")
        col.prop(self, "addface")
        col.prop(self, "seed")
 
classes = (
    add_random_bivar_normal,
)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)

def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)

if __name__ == "__main__":
    register()    
    