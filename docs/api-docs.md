# API and Advanced Documentation

## Configuration Options

The add-on uses property groups for settings:

- **Scene-Level Settings (OrthoScale219Settings)**:
  - `configs`: Collection of all configurations.
  - `active_config_index`: Currently selected config (default: 0).

- **Per-Configuration Settings (OrthoScale219ConfigProperties)**:
  - `config_name`: Custom name (default: "Config").
  - `pixels_per_blender_unit`: Scale factor (default: 10.0, min: 1.0).
  - `edge_margin`: Padding in BU (default: 1.0, min: 0.0).
  - `camera`: Selected camera object.
  - `blender_objects`: List of mesh objects.
  - `active_object_index`: Selected object in list (default: 0).
  - `add_blender_object`: Temporary picker for adding objects.

These are accessible via the UI or scripting (e.g., `bpy.context.scene.ortho_scale_219_settings`).

## Examples

### Basic Render Setup

1. Create a scene with a mesh (e.g., a cube).
2. Add a camera facing the direction you wish to render (The camera will be repositioned so that the objects are centered, but it will not be rotated. The rotation of the camera in 3D space is what will be used.)
3. In the panel, add a config, select the camera, add the cube.
4. Set pixels per unit to 20.0 and margin to 0.5.
5. Compile and render—output will be scaled accordingly.
6. If you're doing technical renders, you will likely have the camera set up at 90-degree increments for its rotations, rather than arbitrary angles such as 21.19 degrees.

### Multi-Object Bounding

- Select multiple meshes.
- Use "Add All Selected Objects".
- Compile: The camera bounds around the combined extents.

### Scripting Example

    import bpy

    # Access settings
    settings = bpy.context.scene.ortho_scale_219_settings

    # Add a config programmatically
    bpy.ops.ortho_scale_219.add_config()

    # Compile active config
    bpy.ops.render.ortho_scale_219_compile()

  Follow PEP 8 for Python code and include docstrings in Google style.

  If you're as obsessed with strict typing as I am, I have included stub files in the `typings` folder. Check your IDE's documentation on how to add stub files for strict typing validation.

  Additionally, if you already have your own copies of these stub files for strict typing you may need to merge mine with yours. I would highly suggest using an already existing app that provides that or an AI/ML model to do it for you. These are far more efficient than doing it manually. And likely a waste of time doing it manually unless you're doing it to learn. But it's your choice how you do this.

For usage instructions, see [usage.md](usage.md).

Return to [main README](../README.md) or [docs index](README.md).