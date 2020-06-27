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
from bpy.types import AddonPreferences
from bpy.props import StringProperty, IntProperty, BoolProperty, FloatProperty, EnumProperty


class add_distributions_prefs(AddonPreferences):
    bl_idname = "add_distributions"

    ncases: IntProperty(
        name = "Number of points",
        default = 50,
        min = 10,
        soft_min = 10
    )
    # add_icosphere: BoolProperty(
        # name = "Add icoshperes",
        # default = False,
    # )
    # dist_selected: EnumProperty(
        # name = "Distribution",
        # items = [
                # ("NORM", "Normal", "Normal", 1),
                # ("BINORM", "Bivariate normal", "Bivariate normal", 2),
                # ],
        # default = "NORM",
    # )
       
    def draw(self, context):
        layout = self.layout
        row = layout.row()
        row.prop(self, "ncases")
        # layout.prop(self, "add_icosphere")
        # layout.prop(self, "dist_selected")
        
classes = (
    add_distributions_prefs,
)
        
def register():
    bpy.utils.register_class(add_distributions_prefs)

def unregister():
    bpy.utils.unregister_class(add_distributions_prefs)
