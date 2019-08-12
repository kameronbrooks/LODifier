bl_info = {
    "name": "LODifier",
    "author" : "Kameron Brooks",
    "description" : "Create a LOD version on your object. Process is destructive, do a save as first!",
    "category" : "Object",
    "location" : "View3D > Object",
    "blender" : (2, 80, 0),
    "version" : (0, 5) 
}

import bpy
import bmesh

from bpy.props import (FloatProperty)

def split_object_seams(mesh):
    bm = bmesh.new()
    bm.from_mesh(mesh)
    seams = []
    
    for edge in bm.edges:
        if(edge.seam):     
            seams.append(edge)
    
    if(len(seams) < 1):
        bm.free()
        return mesh
    
    bmesh.ops.split_edges(bm,edges=seams)
    
    new_mesh = bpy.data.meshes.new("Mesh")
    bm.to_mesh(new_mesh)
    bm.free()
        
    return new_mesh




class LODifierOperator(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "object.lodifier"
    bl_label = "LODifier"
    bl_description = "Create a LOD version on your object. Process is destructive, do a save as first!"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_options = {'REGISTER', 'UNDO'}
    
    collapse_ratio: bpy.props.FloatProperty(
        name = "Collapse Ratio",
        default = 0.5,
        min = 0.001,
        max = 1.0,
        description = "The ratio of triangles on the resulting LOD mesh"
    )
    
    def main(self, context):
        for ob in context.selected_objects: 
            if ob.type != "MESH":
                continue
            ob.data = split_object_seams(ob.data)
            modDec = ob.modifiers.new("Decimate", type="DECIMATE")
            modDec.use_collapse_triangulate = True
            modDec.ratio = self.collapse_ratio
        
    
    @classmethod
    def poll(cls, context):
        for ob in context.selected_objects:
            if(ob.type == 'MESH'):
                return True
        return False
    
    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)
    
    def execute(self, context):
        self.main(context)
        return {'FINISHED'}
    
def menu_func(self, context):
    self.layout.operator(LODifierOperator.bl_idname)

def register():
    bpy.utils.register_class(LODifierOperator)
    bpy.types.VIEW3D_MT_object.append(menu_func)


def unregister():
    bpy.utils.unregister_class(LODifierOperator)
    bpy.types.VIEW3D_MT_object.remove(menu_func)

if __name__ == "__main__":
    register()

    # test call
    #bpy.ops.object.lodifier()