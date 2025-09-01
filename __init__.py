"""
    OrthoScale219 Blender Add-On
    
    Creates a uniform orthographic camera that renders at an explicitly set pixel to Blender Unit ratio.
    
    This add-on provides tools to set up an orthographic camera for rendering at a specified scale, bounding around target mesh
    objects with configurable margins. It includes a UI panel in the Render properties for managing multiple configurations,
    selecting cameras and objects, adjusting settings, and compiling the camera setup. The add-on supports undo/redo and reports
    status via Blender's reporting system.
    
    Classes:
        OrthoScale219ObjectItem: Property group for individual mesh objects.
        ORTHOSCALE219_UL_ObjectList: UI list for displaying mesh objects.
        OrthoScale219ConfigProperties: Property group for configuration settings.
        ORTHOSCALE219_UL_ConfigList: UI list for displaying configurations.
        OrthoScale219Settings: Main scene-level settings property group.
        OBJECT_OT_OrthoScale219AddConfig: Operator to add a new config.
        OBJECT_OT_OrthoScale219RemoveConfig: Operator to remove the active config.
        OBJECT_OT_OrthoScale219AddObject: Operator to add a selected object.
        OBJECT_OT_OrthoScale219AddSelectedObjects: Operator to add all selected meshes.
        OBJECT_OT_OrthoScale219RemoveObject: Operator to remove the selected object.
        OBJECT_OT_OrthoScale219CompileCamera: Operator to compile camera settings.
        RENDER_PT_OrthoScale219Panel: UI panel in Render properties.
    
    Functions:
        mesh_poll: Polls for valid mesh objects.
        camera_poll: Polls for valid camera objects.
        register: Registers all classes and scene properties.
        unregister: Unregisters all classes and scene properties.
    
    Notes:
        Compatible with Blender 4.5.0 and later.
        Access via Properties > Render > OrthoScale219 panel.
        Configurations persist at the scene level.
        The version string in blender_manifest.toml includes non-standard components (e.g., timestamps); refer to
            blender_manifest.toml for details.
    
    Author: S.A. Lowell
    Version: 2.1.9+109092.1756709219
"""
from __future__ import annotations
from typing import Any, cast, TYPE_CHECKING

import math
import bpy

from mathutils import Vector
from bpy.types import PropertyGroup, Operator, Panel, UIList
from bpy.props import FloatProperty, PointerProperty, CollectionProperty, IntProperty, StringProperty

import mathutils

if TYPE_CHECKING:
    from bpy.types import bpy_prop_collection

def mesh_poll(self:bpy.types.bpy_struct, obj:bpy.types.ID) -> bool: # noinspection PyUnusedLocal # pylint: disable=unused-argument # noqa: F841
    """
        Poll function to determine if an object is a valid mesh for selection.
        
        This function serves as a callback for PointerProperty polling in Blender add-ons. It checks whether the provided object
        is an instance of bpy.types.Object and specifically of type 'MESH', allowing only mesh objects to be selectable in
        properties that use this poll function.
        
        Args:
            self (bpy.types.bpy_struct): The struct owning the property, typically a bpy.types.bpy_struct instance. This
                parameter is unused in the function but required by Blender's polling API.
            obj (bpy.types.ID): The object to evaluate for validity.
        
        Returns:
            bool: True if the object is a mesh (instance of bpy.types.Object with type 'MESH'), False otherwise.
    """
    return isinstance(obj, bpy.types.Object) and obj.type == 'MESH'

def camera_poll(self:bpy.types.bpy_struct, obj:bpy.types.ID) -> bool: # noinspection PyUnusedLocal # pylint: disable=unused-argument # noqa: F841
    """
        Poll function to determine if an object is a valid camera for selection.
        
        This function serves as a callback for PointerProperty polling in Blender add-ons. It checks whether the provided object
        is an instance of bpy.types.Object and specifically of type 'CAMERA', allowing only camera objects to be selectable in
        properties that use this poll function.
        
        Args:
            self (bpy.types.bpy_struct): The struct owning the property, typically a bpy.types.bpy_struct instance. This
                parameter is unused in the function but required by Blender's polling API.
            obj (bpy.types.ID): The object to evaluate for validity.
        
        Returns:
            bool: True if the object is a camera (instance of bpy.types.Object with type 'CAMERA'), False otherwise.
    """
    return isinstance(obj, bpy.types.Object) and obj.type == 'CAMERA'

class OrthoScale219ObjectItem(PropertyGroup):
    """
        Property group representing a single mesh object item in an OrthoScale219 configuration.
        
        This class stores a pointer to a mesh object that will be used for bounding box calculations during the orthographic
        camera compilation. It is designed to be part of a collection in the configuration properties.
        
        Attributes:
            mesh_object (bpy.types.Object): Pointer to the mesh object used for bounding box calculations.
    """
    if TYPE_CHECKING:
        mesh_object:bpy.types.Object
    else:
        mesh_object:PointerProperty(
            name = "Object",
            type = bpy.types.Object,
            poll = mesh_poll
        )

class ORTHOSCALE219_UL_ObjectList(UIList): # pylint: disable=invalid-name # noqa: N801
    """
        UI list class for displaying and managing mesh object items in an OrthoScale219 configuration.
        
        This class handles the rendering of object items in the Blender UI, supporting default, compact, and grid layouts. It
        displays each item with an object data icon and allows for property editing without embossing.
    """
    def draw_item(self:ORTHOSCALE219_UL_ObjectList, context:bpy.types.Context, layout:bpy.types.UILayout, data:Any, item:Any, icon:int, active_data:Any, active_propname:str, index:int, flt_flag:int) -> None: # noinspection PyUnusedLocal,PyMethodOverriding # pylint: disable=unused-argument,arguments-renamed # type: ignore[override] # noqa: F841,PLW0237
        """
            Draws an individual mesh object item in the UI list.
            
            This method renders the item based on the layout type, using a property field for default/compact views or a centered
            label for grid views. It displays the mesh_object property without embossing and with an 'OBJECT_DATA' icon.
            
            Args:
                self (ORTHOSCALE219_UL_ObjectList): The UI list instance.
                context (bpy.types.Context): The current Blender context.
                layout (bpy.types.UILayout): The UI layout to draw into.
                data (Any): The data source (e.g., the config containing the objects).
                item (Any): The OrthoScale219ObjectItem to draw.
                icon (int): The icon ID (unused).
                active_data (Any): The active data source (unused).
                active_propname (str): The active property name (unused).
                index (int): The index of the item in the list (unused).
                flt_flag (int): Filter flag (unused).
            
            Returns:
                None
        """
        if self.layout_type in {'DEFAULT', 'COMPACT'}:
            layout.prop(
                data = item,
                property = "mesh_object",
                text = "",
                emboss = False,
                icon = 'OBJECT_DATA',
            )
        elif self.layout_type == 'GRID':
            layout.alignment = 'CENTER'
            layout.label(
                text = "",
                icon = 'OBJECT_DATA',
            )

class OrthoScale219ConfigProperties(PropertyGroup):
    """
        Property group containing all settings for a single OrthoScale219 configuration.
        
        This class holds configuration-specific properties such as the name, pixels per Blender unit, edge margin, selected
        camera, list of mesh objects, and related indices. It serves as an entry in the main settings' collection of
        configurations.
    """
    if TYPE_CHECKING:
        config_name:str
    else:
        config_name:StringProperty(
            name = "Config Name",
            description = "Name of this configuration.",
            default = "Config"
        )
    
    if TYPE_CHECKING:
        pixels_per_blender_unit:float
    else:
        pixels_per_blender_unit:FloatProperty(
            name = "Pixels per Blender Unit",
            description = "Pixels per Blender Unit (higher = more detail and larger files)",
            default = 10.0,
            min = 1.0,
        )
    
    if TYPE_CHECKING:
        edge_margin:float
    else:
        edge_margin:FloatProperty(
            name = "Margin (In Blender Units)",
            description = "Margin (in Blender Units) that will be padded around the edge of the render.",
            default = 1.0,
            min = 0.0,
        )
    
    if TYPE_CHECKING:
        camera:bpy.types.Object | None
    else:
        camera:PointerProperty(
            name = "Camera",
            type = bpy.types.Object,
            poll = camera_poll,
            description = "Select the camera to use."
        )
    
    if TYPE_CHECKING:
        blender_objects:bpy_prop_collection[OrthoScale219ObjectItem]
    else:
        blender_objects:CollectionProperty(
            type = OrthoScale219ObjectItem
        )
    
    if TYPE_CHECKING:
        active_object_index:int
    else:
        active_object_index:IntProperty()
    
    if TYPE_CHECKING:
        add_blender_object:bpy.types.Object | None
    else:
        add_blender_object:PointerProperty(
            name = "Add Blender Object",
            type = bpy.types.Object,
            poll = mesh_poll,
            description = "Select a Blender Object to add."
        )

class ORTHOSCALE219_UL_ConfigList(UIList): # pylint: disable=invalid-name # noqa: N801
    """
        UI list class for displaying and managing OrthoScale219 configurations.
        
        This class handles the rendering of configuration items in the Blender UI, supporting default, compact, and grid layouts.
        It displays each configuration with a preset icon and allows for property editing without embossing.
    """
    def draw_item(self:ORTHOSCALE219_UL_ConfigList, context:bpy.types.Context, layout:bpy.types.UILayout, data:Any, item:Any, icon:int, active_data:Any, active_propname:str, index:int, flt_flag:int) -> None: # noinspection PyUnusedLocal,PyMethodOverriding # pylint: disable=unused-argument,arguments-renamed # type: ignore[override] # noqa: F841,PLW0237
        """
            Draws an individual configuration item in the UI list.
            
            This method renders the item based on the layout type, using a property field for default/compact views or a centered
            label for grid views. It displays the config_name property without embossing and with a 'PRESET' icon.
            
            Args:
                self (ORTHOSCALE219_UL_ConfigList): The UI list instance.
                context (bpy.types.Context): The current Blender context.
                layout (bpy.types.UILayout): The UI layout to draw into.
                data (Any): The data source (e.g., the settings containing the configs).
                item (Any): The OrthoScale219ConfigProperties to draw.
                icon (int): The icon ID (unused).
                active_data (Any): The active data source (unused).
                active_propname (str): The active property name (unused).
                index (int): The index of the item in the list (unused).
                flt_flag (int): Filter flag (unused).
            
            Returns:
                None
        """
        if self.layout_type in {'DEFAULT', 'COMPACT'}:
            layout.prop(
                data = item,
                property = "config_name",
                text = "",
                emboss = False,
                icon = 'PRESET',
            )
        elif self.layout_type == 'GRID':
            layout.alignment = 'CENTER'
            layout.label(
                text = "",
                icon = 'PRESET',
            )

class OrthoScale219Settings(PropertyGroup):
    """
        Main property group for OrthoScale219 add-on settings.
        
        This class manages a collection of configurations and tracks the active configuration index. It is attached to the
        Blender scene for persistent storage across sessions.
        
        Attributes:
            configs (bpy_prop_collection[OrthoScale219ConfigProperties]): Collection of all configurations.
            active_config_index (int): Index of the active configuration in the configs collection. Default: 0.
    """
    if TYPE_CHECKING:
        configs:bpy_prop_collection[OrthoScale219ConfigProperties]
    else:
        configs:CollectionProperty(type = OrthoScale219ConfigProperties)
    
    if TYPE_CHECKING:
        active_config_index:int
    else:
        active_config_index:IntProperty()

class OBJECT_OT_OrthoScale219AddConfig(Operator): # pylint: disable=invalid-name # noqa: N801
    """
        Operator to add a new configuration to the OrthoScale219 settings.
        
        This operator creates a new OrthoScale219ConfigProperties instance, assigns it a default name based on the current number
        of configurations, adds it to the settings' collection, and sets it as the active configuration.
    """
    bl_idname:str = "ortho_scale_219.add_config"
    bl_label:str = "Add Config"
    bl_description:str = "Add a new configuration."
    bl_options:set[str] = {
        'REGISTER',
        'UNDO',
    }
    
    def execute(self:OBJECT_OT_OrthoScale219AddConfig, context:bpy.types.Context)-> set[str]:
        """
            Executes the addition of a new configuration.
            
            This method retrieves the settings, adds a new config with a default name, and updates the active index.
            
            Args:
                self (OBJECT_OT_OrthoScale219AddConfig): The operator instance.
                context (bpy.types.Context): The current Blender context.
            
            Returns:
                set[str]: {'FINISHED'} on success.
        """
        settings:OrthoScale219Settings = cast(OrthoScale219Settings, getattr(context.scene, "ortho_scale_219_settings"))
        configs = settings.configs
        new_config:OrthoScale219ConfigProperties = configs.add()
        new_config.config_name = f"Config {len(configs)}"
        settings.active_config_index = len(configs) - 1
        
        return {'FINISHED'}

class OBJECT_OT_OrthoScale219RemoveConfig(Operator): # pylint: disable=invalid-name # noqa: N801
    """
        Operator to remove the active configuration from the OrthoScale219 settings.
        
        This operator removes the configuration at the active index from the settings' collection and adjusts the active index to
        the previous valid one (or 0 if none remain).
    """
    bl_idname:str = "ortho_scale_219.remove_config"
    bl_label:str = "Remove Config"
    bl_description:str = "Remove the selected configuration."
    bl_options:set[str] = {
        'REGISTER',
        'UNDO',
    }
    
    def execute(self:OBJECT_OT_OrthoScale219RemoveConfig, context:bpy.types.Context)-> set[str]:
        """
            Executes the removal of the active configuration.
            
            This method retrieves the settings, removes the config at the active index if valid, and adjusts the active index.
            
            Args:
                self (OBJECT_OT_OrthoScale219RemoveConfig): The operator instance.
                context (bpy.types.Context): The current Blender context.
            
            Returns:
                set[str]: {'FINISHED'} on success.
        """
        settings:OrthoScale219Settings = cast(OrthoScale219Settings, getattr(context.scene, "ortho_scale_219_settings"))
        index:int = settings.active_config_index
        
        if 0 <= index < len(settings.configs):
            settings.configs.remove(index)
            settings.active_config_index = max(0, index - 1)
        
        return {'FINISHED'}

class OBJECT_OT_OrthoScale219AddObject(Operator): # pylint: disable=invalid-name # noqa: N801
    """
        Operator to add a selected mesh object to the active configuration's object list.
        
        This operator checks for an active configuration, verifies the selected object is not already in the list, adds it as a
        new OrthoScale219ObjectItem if valid, and clears the add object pointer. Reports warnings for invalid states like no
        object selected or duplicates.
    """
    bl_idname:str = "ortho_scale_219.add_blender_object"
    bl_label:str = "Add Object"
    bl_description:str = "Add the selected object to the active config's list"
    bl_options:set[str] = {
        'REGISTER',
        'UNDO',
    }
    
    def execute(self:OBJECT_OT_OrthoScale219AddObject, context:bpy.types.Context)-> set[str]:
        """
            Executes the addition of a selected object to the active config's list.
            
            This method validates the active config, checks for duplicates, adds the object if valid, and clears the temporary
            pointer.
            
            Args:
                self (OBJECT_OT_OrthoScale219AddObject): The operator instance.
                context (bpy.types.Context): The current Blender context.
            
            Returns:
                set[str]: {'FINISHED'} on success (even if duplicate), or {'CANCELLED'} if no active config.
            
            Notes:
                Reports WARNING via self.report if no object selected, duplicate, or no active config.
        """
        settings:OrthoScale219Settings = cast(OrthoScale219Settings, getattr(context.scene, "ortho_scale_219_settings"))
        
        if not 0 <= settings.active_config_index < len(settings.configs):
            self.report({'WARNING'}, "No active config selected.")
            
            return {'CANCELLED'}
        
        config:OrthoScale219ConfigProperties = settings.configs[settings.active_config_index]
        
        if config.add_blender_object:
            for item in config.blender_objects:
                if item.mesh_object == config.add_blender_object:
                    self.report({'WARNING'}, "Object already in the list!")
                    config.add_blender_object = None
                    
                    return {'FINISHED'}
            
            item:OrthoScale219ObjectItem = config.blender_objects.add()
            item.mesh_object = config.add_blender_object
            config.add_blender_object = None
        else:
            self.report({'WARNING'}, "No object selected to add.")
        
        return {'FINISHED'}

class OBJECT_OT_OrthoScale219AddSelectedObjects(Operator): # pylint: disable=invalid-name # noqa: N801
    """
        Operator to add all currently selected mesh objects to the active configuration's object list.
        
        This operator checks for an active configuration, iterates over selected objects, filters for mesh types not already in
        the list, adds them as new OrthoScale219ObjectItem instances, and reports the number added or info if none were eligible.
    """
    bl_idname:str = "ortho_scale_219.add_selected_objects"
    bl_label:str = "Add All Selected Objects"
    bl_description:str = "Add all currently selected mesh objects to the active config's list"
    bl_options:set[str] = {
        'REGISTER',
        'UNDO',
    }
    
    def execute(self:OBJECT_OT_OrthoScale219AddSelectedObjects, context:bpy.types.Context) -> set[str]:
        """
            Executes the addition of all selected mesh objects to the active config's list.
            
            This method validates the active config, filters and adds eligible meshes, and reports the result.
            
            Args:
                self (OBJECT_OT_OrthoScale219AddSelectedObjects): The operator instance.
                context (bpy.types.Context): The current Blender context.
            
            Returns:
                set[str]: {'FINISHED'} on success, or {'CANCELLED'} if no active config.
            
            Notes:
                Reports INFO via self.report on the number of objects added or if none were eligible.
                Reports WARNING if no active config.
        """
        settings:OrthoScale219Settings = cast(OrthoScale219Settings, getattr(context.scene, "ortho_scale_219_settings"))
        
        if not 0 <= settings.active_config_index < len(settings.configs):
            self.report({'WARNING'}, "No active config selected.")
            
            return {'CANCELLED'}
        
        config:OrthoScale219ConfigProperties = settings.configs[settings.active_config_index]
        added_count:int = 0
        
        for obj in context.selected_objects:
            if obj.type != 'MESH':
                continue
            if any(item.mesh_object == obj for item in config.blender_objects):
                continue
            
            item:OrthoScale219ObjectItem = config.blender_objects.add()
            item.mesh_object = obj
            added_count += 1
        
        if added_count > 0:
            self.report({'INFO'}, f"Added {added_count} object(s) to the list.")
        else:
            self.report({'INFO'}, "No new mesh objects to add (already in list or none selected).")
        
        return {'FINISHED'}

class OBJECT_OT_OrthoScale219RemoveObject(Operator): # pylint: disable=invalid-name # noqa: N801
    """
        Operator to remove the selected object from the active configuration's object list.
        
        This operator checks for an active configuration, removes the object item at the active object index, and adjusts the
        active object index to the previous valid one (or 0 if none remain).
    """
    bl_idname:str = "ortho_scale_219.remove_object"
    bl_label:str = "Remove Object"
    bl_description:str = "Remove the selected object from the active config's list"
    bl_options:set[str] = {
        'REGISTER',
        'UNDO',
    }
    
    def execute(self:OBJECT_OT_OrthoScale219RemoveObject, context:bpy.types.Context) -> set[str]:
        """
            Executes the removal of the selected object from the active config's list.
            
            This method validates the active config, removes the object at the active index if valid, and adjusts the index.
            
            Args:
                self (OBJECT_OT_OrthoScale219RemoveObject): The operator instance.
                context (bpy.types.Context): The current Blender context.
            
            Returns:
                set[str]: {'FINISHED'} on success, or {'CANCELLED'} if no active config.
        """
        settings:OrthoScale219Settings = cast(OrthoScale219Settings, getattr(context.scene, "ortho_scale_219_settings"))
        
        if not 0 <= settings.active_config_index < len(settings.configs):
            return {'CANCELLED'}
        
        config:OrthoScale219ConfigProperties = settings.configs[settings.active_config_index]
        index:int = config.active_object_index
        
        if 0 <= index < len(config.blender_objects):
            config.blender_objects.remove(index)
            config.active_object_index = max(0, index - 1)
        
        return {'FINISHED'}

class OBJECT_OT_OrthoScale219CompileCamera(Operator): # pylint: disable=invalid-name # noqa: N801
    """
        Operator to set up the orthographic camera and render settings based on the active configuration.
        
        This operator validates the active configuration, selected camera, and mesh objects; computes the bounding box in camera
        space; adjusts camera position, orthographic scale, clip planes, and render resolution; and applies padding margins. It
        reports errors for invalid states, warnings for objects behind the camera, and info on completion.
    """
    bl_idname:str = "render.ortho_scale_219_compile"
    bl_label:str = "Compile Camera"
    bl_description:str = "Applies all the configuration settings to the camera."
    bl_options:set[str] = {
        'REGISTER',
        'UNDO',
    }
    
    def execute(self:OBJECT_OT_OrthoScale219CompileCamera, context:bpy.types.Context) -> set[str]:
        """
            Executes the compilation of the camera and render settings.
            
            This method validates inputs, computes the bounding box, adjusts camera and render properties, and reports status.
            
            Args:
                self (OBJECT_OT_OrthoScale219CompileCamera): The operator instance.
                context (bpy.types.Context): The current Blender context.
            
            Returns:
                set[str]: {'FINISHED'} on success, or {'CANCELLED'} on validation errors.
            
            Notes:
                Reports ERROR via self.report for no config/objects/camera/vertices.
                Reports WARNING for objects behind the camera or invalid states.
                Reports INFO on completion with setup details.
                Uses a helper function get_bbox to compute bounds and center the camera.
        """
        settings:OrthoScale219Settings = cast(OrthoScale219Settings, getattr(context.scene, "ortho_scale_219_settings"))
        
        if not 0 <= settings.active_config_index < len(settings.configs):
            self.report({'ERROR'}, "No active config selected.")
            
            return {'CANCELLED'}
        
        config:OrthoScale219ConfigProperties = settings.configs[settings.active_config_index]
        objs:list[bpy.types.Object] = [item.mesh_object for item in config.blender_objects if item.mesh_object and item.mesh_object.type == 'MESH']
        
        if not objs:
            self.report({'ERROR'}, "No valid objects in the active config's list!")
            
            return {'CANCELLED'}
        
        cam_obj:bpy.types.Object | None = config.camera
        
        if cam_obj is None or cam_obj.type != 'CAMERA':
            self.report({'ERROR'}, "No valid camera selected in active config.")
            
            return {'CANCELLED'}
        
        def get_bbox(objs:list[bpy.types.Object], context:bpy.types.Context, cam_obj:bpy.types.Object | None) -> tuple[mathutils.Vector, mathutils.Vector, float, float]:
            """
                Computes the bounding box of objects in camera space and centers the camera.
                
                This helper function evaluates meshes, transforms vertices to camera coordinates, finds min/max extents, centers
                the camera on the XY plane, and returns the updated bounds.
                
                Args:
                    objs (list[bpy.types.Object]): List of mesh objects to bound.
                    context (bpy.types.Context): The current Blender context for depsgraph access.
                    cam_obj (bpy.types.Object | None): The camera object for transformation matrix.
                
                Returns:
                    tuple[mathutils.Vector, mathutils.Vector, float, float]: (min_co, max_co, min_z, max_z) in camera space.
                        Returns zeros if no camera or no vertices.
                
                Notes:
                    Modifies cam_obj.location to center the view.
                    Uses evaluated depsgraph for accurate mesh data.
                    Clears temporary meshes after use.
            """
            if cam_obj is None:
                return Vector((0.0, 0.0, 0.0)), Vector((0.0, 0.0, 0.0)), 0.0, 0.0
            
            depsgraph:bpy.types.Depsgraph = context.evaluated_depsgraph_get()
            cam_matrix_inv:mathutils.Matrix = cam_obj.matrix_world.inverted()
            
            min_x:float = float('inf')
            min_y:float = float('inf')
            min_z:float = float('inf')
            max_x:float = -float('inf')
            max_y:float = -float('inf')
            max_z:float = -float('inf')
            
            has_verts:bool = False
            
            for obj in objs:
                eval_obj:bpy.types.Object | None = depsgraph.objects.get(obj.name)
                
                if eval_obj is None:
                    continue
                
                mesh:bpy.types.Mesh = eval_obj.to_mesh(
                    preserve_all_data_layers = True,
                    depsgraph = depsgraph,
                )
                
                if not mesh.vertices:
                    eval_obj.to_mesh_clear()
                    
                    continue
                
                has_verts = True
                
                for vert in mesh.vertices:
                    world_co:mathutils.Vector = eval_obj.matrix_world @ vert.co
                    cam_co:mathutils.Vector = cam_matrix_inv @ world_co
                    
                    min_x = min(min_x, cam_co.x)
                    max_x = max(max_x, cam_co.x)
                    min_y = min(min_y, cam_co.y)
                    max_y = max(max_y, cam_co.y)
                    min_z = min(min_z, cam_co.z)
                    max_z = max(max_z, cam_co.z)
                
                eval_obj.to_mesh_clear()
            
            if not has_verts:
                return Vector((0.0, 0.0, 0.0)), Vector((0.0, 0.0, 0.0)), 0.0, 0.0
            
            center_cam_x:float = (min_x + max_x) / 2
            center_cam_y:float = (min_y + max_y) / 2
            
            if abs(center_cam_x) < 1e-6:
                center_cam_x = 0
            
            if abs(center_cam_y) < 1e-6:
                center_cam_y = 0
            
            delta_local:mathutils.Vector = Vector((center_cam_x, center_cam_y, 0))
            delta_world:mathutils.Vector = cam_obj.matrix_world.to_3x3() @ delta_local
            
            cam_obj.location += delta_world
            
            return Vector((min_x, min_y, 0)), Vector((max_x, max_y, 0)), min_z, max_z
        
        min_co:mathutils.Vector = Vector((0.0, 0.0, 0.0))
        max_co:mathutils.Vector = Vector((0.0, 0.0, 0.0))
        min_z:float = 0.0
        max_z:float = 0.0
        
        min_co, max_co, min_z, max_z = get_bbox(objs, context, cam_obj)
        
        if min_co == Vector((0.0, 0.0, 0.0)) and max_co == Vector((0.0, 0.0, 0.0)):
            self.report({'ERROR'}, "No valid vertices found in objects!")
            
            return {'CANCELLED'}
        
        if max_z > 0:
            self.report({'WARNING'}, "Some objects are behind the camera; they may not render correctly.")
        
        width_bu:float = max_co.x - min_co.x
        height_bu:float = max_co.y - min_co.y
        
        view_width_bu:float = width_bu + 2 * config.edge_margin
        view_height_bu:float = height_bu + 2 * config.edge_margin
        
        ppbu:float = config.pixels_per_blender_unit
        res_x:int = math.ceil(ppbu * view_width_bu)
        res_y:int = math.ceil(ppbu * view_height_bu)
        
        world_width:float = res_x / ppbu
        world_height:float = res_y / ppbu
        
        scene:bpy.types.Scene = context.scene
        scene.render.resolution_x = res_x
        scene.render.resolution_y = res_y
        scene.render.resolution_percentage = 100
        
        cam_data:bpy.types.Camera = cast(bpy.types.Camera, cam_obj.data)
        cam_data.type = 'ORTHO'
        
        if res_x >= res_y:
            cam_data.ortho_scale = world_width
        else:
            cam_data.ortho_scale = world_height
        
        cam_data.shift_x = 0
        cam_data.shift_y = 0
        
        small:float = 0.001
        target_closest:float = -(config.edge_margin + small)
        k:float = max_z - target_closest
        
        delta_local_z:mathutils.Vector = Vector((0, 0, k))
        delta_world_z:mathutils.Vector = cam_obj.matrix_world.to_3x3() @ delta_local_z
        cam_obj.location += delta_world_z
        
        new_min_z:float = min_z - k
        
        cam_data.clip_start = small
        cam_data.clip_end = -new_min_z + config.edge_margin
        
        self.report({'INFO'}, f"OrthoScale219 camera compiling complete: Resolution {res_x}x{res_y}, Orthographic Scale {cam_data.ortho_scale}, Pixels Per Blender Unit {ppbu}, Clip Start/End {cam_data.clip_start}/{cam_data.clip_end}")
        
        return {'FINISHED'}

class RENDER_PT_OrthoScale219Panel(Panel): # pylint: disable=invalid-name # noqa: N801
    """
        Panel in the Render properties for configuring OrthoScale219 settings.
        
        This panel displays UI elements for managing configurations, selecting cameras and objects, adjusting pixels per unit and
        margins, and executing the setup operator. It is collapsible and located in the Properties window under Render context.
    """
    bl_label:str = "OrthoScale219"
    bl_idname:str = "RENDER_PT_ortho_scale_219"
    bl_space_type:str = 'PROPERTIES'
    bl_region_type:str = 'WINDOW'
    bl_context:str = "render"
    bl_options:set[str] = {'DEFAULT_CLOSED'}
    
    def draw(self:RENDER_PT_OrthoScale219Panel, context:bpy.types.Context):
        """
            Draws the UI elements for the OrthoScale219 panel.
            
            This method lays out boxes, rows, columns, labels, property fields, template lists, and operators for configurations,
            cameras, objects, and settings. It conditionally renders elements based on the active configuration index.
        """
        layout:bpy.types.UILayout = self.layout
        settings:OrthoScale219Settings = cast(OrthoScale219Settings, getattr(context.scene, "ortho_scale_219_settings"))
        
        box:bpy.types.UILayout = layout.box()
        row:bpy.types.UILayout = box.row()
        col:bpy.types.UILayout = row.column()
        col.label(text = "Configurations:")
        col.template_list(
            listtype_name = "ORTHOSCALE219_UL_ConfigList",
            list_id = "ortho_scale_219_configs",
            dataptr = settings,
            propname = "configs",
            active_dataptr = settings,
            active_propname = "active_config_index",
            rows = 2,
        )
        sub:bpy.types.UILayout = row.column(align = True)
        sub.operator(
            operator = "ortho_scale_219.add_config",
            text = "",
            icon = 'ADD',
        )
        sub.operator(
            operator = "ortho_scale_219.remove_config",
            text = "",
            icon = 'REMOVE',
        )
        
        if not 0 <= settings.active_config_index < len(settings.configs):
            return
        
        config:OrthoScale219ConfigProperties = settings.configs[settings.active_config_index]
        
        layout.separator()
        col = layout.column()
        col.label(text = "Camera:")
        col.prop(
            data = config,
            property = "camera",
            text = "",
            icon = 'CAMERA_DATA',
        )
        layout.separator()
        
        box = layout.box()
        box.label(text = "Objects:")
        row = box.row()
        col = row.column()
        col.template_list(
            listtype_name = "ORTHOSCALE219_UL_ObjectList",
            list_id = "ortho_scale_219_objects",
            dataptr = config,
            propname = "blender_objects",
            active_dataptr = config,
            active_propname = "active_object_index",
            rows = 3,
        )
        sub = row.column(align = True)
        box.separator()
        sub.operator(
            operator = "ortho_scale_219.remove_object",
            text = "",
            icon = 'REMOVE',
        )
        sub = box.row(align = True)
        sub.prop(
            data = config,
            property = "add_blender_object",
            text = "",
        )
        sub.operator(
            operator = "ortho_scale_219.add_blender_object",
            text = "",
            icon = 'ADD',
        )
        box.operator(
            operator = "ortho_scale_219.add_selected_objects"
        )
        
        layout.separator()
        layout.prop(
            data = config,
            property = "pixels_per_blender_unit",
        )
        layout.prop(
            data = config,
            property = "edge_margin",
        )
        layout.separator()
        
        row = layout.row()
        row.scale_x = 3.0
        row.scale_y = 3.0
        row.operator(operator = "render.ortho_scale_219_compile")

rna_classes = (
    OrthoScale219ObjectItem,
    ORTHOSCALE219_UL_ObjectList,
    OrthoScale219ConfigProperties,
    ORTHOSCALE219_UL_ConfigList,
    OrthoScale219Settings,
    OBJECT_OT_OrthoScale219AddConfig,
    OBJECT_OT_OrthoScale219RemoveConfig,
    OBJECT_OT_OrthoScale219AddObject,
    OBJECT_OT_OrthoScale219AddSelectedObjects,
    OBJECT_OT_OrthoScale219RemoveObject,
    OBJECT_OT_OrthoScale219CompileCamera,
    RENDER_PT_OrthoScale219Panel,
)

ortho_scale_219_registered = [False]

def register() -> None:
    """
        Registers all classes and properties for the OrthoScale219 add-on.
        
        This function registers each class in the 'rna_classes' tuple with Blender and attaches the OrthoScale219Settings
        property group to the Scene type for scene-level persistence.
    """
    if ortho_scale_219_registered[0]:
        return
    
    for cls in rna_classes:
        bpy.utils.register_class(cls)
    
    bpy.types.Scene.ortho_scale_219_settings = bpy.props.PointerProperty(type = OrthoScale219Settings)
    ortho_scale_219_registered[0] = True

def unregister():
    """
        Unregisters all classes and properties for the OrthoScale219 add-on.
        
        This function unregisters each class in the 'rna_classes' tuple in reverse order and removes the OrthoScale219Settings
        property from the Scene type.
    """
    if not ortho_scale_219_registered[0]:
        return
    
    for cls in reversed(rna_classes):
        try:
            bpy.utils.unregister_class(cls)
        except RuntimeError:
            pass
    
    if hasattr(bpy.types.Scene, "ortho_scale_219_settings"):
        del bpy.types.Scene.ortho_scale_219_settings
    
    ortho_scale_219_registered[0] = False

if __name__ == "__main__":
    register()
