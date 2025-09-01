# Usage Guide

### Quick Start

1. **Open the Panel**:
   - Switch to the `Properties` editor.
   - Select the `Render` tab.
   - Scroll to the `OrthoScale219` panel (it may be collapsed by default; expand it).

2. **Create a Configuration**:
   - Click the `+` icon next to the configurations list to add a new config.
   - Double click the `Configuration's default name` and start typing to rename it as desired.

3. **Select Camera**:
   - Choose a Camera from the `Camera` `dropdown` (only valid cameras are pollable) or via the `Eyedropped Data-Block` `tool` to the right of the dropdown.
   - Remove the Camera via the `x` to the `right side` of the `Camera` selectors.

3. **Select Objects**:
   - Add mesh objects using the `Add Blender Object` `dropdown`, the `Eyedropped Data-Block` `tool`, or by clicking the `Add All Selected Objects` button.
   - Remove objects with the `-` icon to the right of the `Objects:` list that shows all the currently added Objects.

4. **Adjust Settings**:
   - Set `Pixels per Blender Unit` (default: 10.0; min: 1.0) for render detail. This is how many pixels will take up 1 Blender Unit during rendering.
   - Set `Margin (In Blender Units)` (default: 1.0; min: 0.0) for edge padding. This is how many Blender Units will be used as padding around the selected objects.

5. **Compile the Camera**:
   - Click the `Compile Camera` button.
   - The add-on will validate inputs, compute bounds, adjust the camera and render resolution, and report the current status to Blender's System Console. The camera will calculate all of this while retaining AND relative to its current rotation values (ie: The Camera's rotation will not be changed, only its position and other settings required to meet all your given inputs and center the camera's view on the selected Objects.)

6. **Render**:
   - Proceed with Blender's standard rendering (F12 or Render menu).
   - The setup ensures the output matches your settings.

### Advanced Usage

- **Multiple Configurations**: Switch between configs in the list; each stores independent cameras, objects, and settings.
- **Object Management**: Use Blender's selection tools to pick meshes; the add-on filters non-meshes automatically.
- **Camera Positioning**: The compilation centers the camera on the bounding box's XY center and adjusts Z for clip planes.
- **Error Handling**: If no vertices are found or objects are invalid, the process cancels with an error report.
- **Customization**: Edit the script for custom behaviors if desired/needed, but note that changes may require restarting Blender.

For examples, configuration options, and scripting, see [api-docs.md](api-docs.md).

Return to [main README](../README.md) or [docs index](README.md).