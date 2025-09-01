"""
    OrthoScale219 E2E Testing
    
    End-to-end tests for the OrthoScale219 Blender Add-On.
    
    This test suite verifies the functionality of the OrthoScale219 add-on, including configuration management, object
    addition/removal, and camera compilation. Tests use pytest and pytest-blender to simulate Blender environments, ensuring
    operators, properties, and UI interactions work as expected. Each test starts with a clean scene and add-on settings for
    isolation.
    
    Fixtures:
        clean_scene: Fixture to reset the scene and add-on settings before each test.
    
    Tests:
        test_add_config: Test adding a new configuration.
        test_remove_config: Test removing the active configuration.
        test_add_object: Test adding a single object to the active config.
        test_add_selected_objects: Test adding all selected mesh objects to the active config.
        test_remove_object: Test removing an object from the active config's list.
        test_compile_camera: Test compiling the camera setup based on the config.
    
    Notes:
        Requires pytest and pytest-blender installed in Blender's Python environment.
        Compatible with Blender 4.5.0 and later.
        Run via pytest with --blender-executable flag for integration testing.
        Tests assume the add-on is installed and enabled via conftest.py.
    
    Author: S.A. Lowell
    Version: 2.1.9+109092.1756709219
"""
from typing import cast, TYPE_CHECKING

import math
import bpy
import pytest

if TYPE_CHECKING:
    from .. import OrthoScale219Settings
else:
    import importlib.util
    import sys
    import os

    addon_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "__init__.py")
    spec = importlib.util.spec_from_file_location("ortho_scale_219", addon_path)
    ortho_scale_219 = importlib.util.module_from_spec(spec)
    sys.modules["ortho_scale_219"] = ortho_scale_219
    spec.loader.exec_module(ortho_scale_219)

    from ortho_scale_219 import OrthoScale219Settings

@pytest.fixture(scope = "function")
def clean_scene():
    """
        Fixture to create a clean scene for each test.
        
        This fixture deletes all objects in the current scene and clears the OrthoScale219 configurations to start with a clean
        slate. It yields control to the test and cleans up afterward if needed.
        
        Yields:
            None
    """
    print("Starting clean_scene")
    
    bpy.ops.object.select_all(action = 'SELECT')
    bpy.ops.object.delete(use_global = False)
    
    settings:OrthoScale219Settings = cast(OrthoScale219Settings, getattr(bpy.context.scene, "ortho_scale_219_settings"))
    settings.configs.clear()
    settings.active_config_index = 0
    
    yield
    
    print("clean_scene completed")

def test_add_config(clean_scene:None): # noinspection PyUnusedLocal,PyShadowingNames # pylint: disable=unused-argument,redefined-outer-name # noqa: F841
    """
        Test adding a new configuration.
        
        This test invokes the add_config operator and verifies that a new config is added to the settings collection and set as
        active.
    """
    print("Starting test_add_config")
    
    settings:OrthoScale219Settings = cast(OrthoScale219Settings, getattr(bpy.context.scene, "ortho_scale_219_settings"))
    initial_len = len(settings.configs)
    bpy.ops.ortho_scale_219.add_config()
    assert len(settings.configs) == initial_len + 1
    assert settings.active_config_index == initial_len
    
    print("test_add_config completed")

def test_remove_config(clean_scene:None): # noinspection PyUnusedLocal,PyShadowingNames # pylint: disable=unused-argument,redefined-outer-name # noqa: F841
    """
        Test removing the active configuration.
        
        This test adds a config, then removes it, verifying the collection is empty afterward.
    """
    print("Starting test_remove_config")
    
    settings:OrthoScale219Settings = cast(OrthoScale219Settings, getattr(bpy.context.scene, "ortho_scale_219_settings"))
    bpy.ops.ortho_scale_219.add_config()
    bpy.ops.ortho_scale_219.remove_config()
    assert len(settings.configs) == 0
    assert settings.active_config_index == 0
    
    print("test_remove_config completed")

def test_add_object(clean_scene:None): # noinspection PyUnusedLocal,PyShadowingNames # pylint: disable=unused-argument,redefined-outer-name # noqa: F841
    """
        Test adding a single object to the active config.
        
        This test creates a mesh object, adds a config, sets the add_blender_object property, invokes the add_blender_object
        operator, and verifies the object is added to the list.
    """
    print("Starting test_add_object")
    
    settings:OrthoScale219Settings = cast(OrthoScale219Settings, getattr(bpy.context.scene, "ortho_scale_219_settings"))
    bpy.ops.ortho_scale_219.add_config()
    config = settings.configs[settings.active_config_index]
    
    mesh = bpy.data.meshes.new("TestMesh")
    obj = bpy.data.objects.new("TestObject", mesh)
    bpy.context.collection.objects.link(obj)
    
    config.add_blender_object = obj
    bpy.ops.ortho_scale_219.add_blender_object()
    assert len(config.blender_objects) == 1
    assert config.blender_objects[0].mesh_object == obj
    
    print("test_add_object completed")

def test_add_selected_objects(clean_scene:None): # noinspection PyUnusedLocal,PyShadowingNames # pylint: disable=unused-argument,redefined-outer-name # noqa: F841
    """
        Test adding all selected mesh objects to the active config.
        
        This test creates two mesh objects, selects them, adds a config, invokes the add_selected_objects operator, and verifies
        both are added to the list.
    """
    print("Starting test_add_selected_objects")
    
    settings:OrthoScale219Settings = cast(OrthoScale219Settings, getattr(bpy.context.scene, "ortho_scale_219_settings"))
    bpy.ops.ortho_scale_219.add_config()
    config = settings.configs[settings.active_config_index]
    
    mesh1 = bpy.data.meshes.new("TestMesh1")
    obj1 = bpy.data.objects.new("TestObject1", mesh1)
    bpy.context.collection.objects.link(obj1)
    obj1.select_set(True)
    
    mesh2 = bpy.data.meshes.new("TestMesh2")
    obj2 = bpy.data.objects.new("TestObject2", mesh2)
    bpy.context.collection.objects.link(obj2)
    obj2.select_set(True)
    
    bpy.ops.ortho_scale_219.add_selected_objects()
    assert len(config.blender_objects) == 2
    assert any(item.mesh_object == obj1 for item in config.blender_objects)
    assert any(item.mesh_object == obj2 for item in config.blender_objects)
    
    print("test_add_selected_objects completed")

def test_remove_object(clean_scene:None): # noinspection PyUnusedLocal,PyShadowingNames # pylint: disable=unused-argument,redefined-outer-name # noqa: F841
    """
        Test removing an object from the active config's list.
        
        This test adds a config and an object, sets the active object index, invokes the remove_object operator, and verifies the
        list is empty.
    """
    print("Starting test_remove_object")
    
    settings:OrthoScale219Settings = cast(OrthoScale219Settings, getattr(bpy.context.scene, "ortho_scale_219_settings"))
    bpy.ops.ortho_scale_219.add_config()
    config = settings.configs[settings.active_config_index]
    
    mesh = bpy.data.meshes.new("TestMesh")
    obj = bpy.data.objects.new("TestObject", mesh)
    bpy.context.collection.objects.link(obj)
    config.add_blender_object = obj
    bpy.ops.ortho_scale_219.add_blender_object()
    
    config.active_object_index = 0
    bpy.ops.ortho_scale_219.remove_object()
    assert len(config.blender_objects) == 0
    
    print("test_remove_object completed")

def test_compile_camera(clean_scene:None): # noinspection PyUnusedLocal,PyShadowingNames # pylint: disable=unused-argument,redefined-outer-name # noqa: F841
    """
        Test compiling the camera setup based on the config.
        
        This test creates a camera and a cube, adds a config, sets the camera and adds the cube, sets pixels_per_blender_unit and
        edge_margin, invokes the compile operator, and verifies render resolution, orthographic scale, and clip planes are set
        correctly for a simple case.
    """
    print("Starting test_compile_camera")
    
    settings:OrthoScale219Settings = cast(OrthoScale219Settings, getattr(bpy.context.scene, "ortho_scale_219_settings"))
    bpy.ops.ortho_scale_219.add_config()
    config = settings.configs[settings.active_config_index]
    
    cam_data = bpy.data.cameras.new("TestCamera")
    cam_obj = bpy.data.objects.new("TestCamera", cam_data)
    bpy.context.collection.objects.link(cam_obj)
    cam_obj.location = (0, -10, 0)
    cam_obj.rotation_euler = (math.radians(90), 0, math.radians(180))
    
    bpy.ops.mesh.primitive_cube_add(location=(0, 0, 0))
    
    cube = bpy.context.active_object
    
    config.camera = cam_obj
    config.pixels_per_blender_unit = 10.0
    config.edge_margin = 0.0
    
    config.add_blender_object = cube
    bpy.ops.ortho_scale_219.add_blender_object()
    
    bpy.ops.render.ortho_scale_219_compile()
    
    scene = bpy.context.scene
    assert scene.render.resolution_x == pytest.approx(20, abs=1)
    assert scene.render.resolution_y == pytest.approx(20, abs=1)
    assert cam_data.type == 'ORTHO'
    assert cam_data.ortho_scale == pytest.approx(2.0, abs=0.1)
    assert cam_data.clip_start == pytest.approx(0.001, abs=0.001)
    assert cam_data.clip_end == pytest.approx(2.001, abs=0.1)
    
    print("test_compile_camera completed")
