# Troubleshooting

- **Panel Not Visible**: Ensure the add-on is enabled in `Edit > Preferences > Add-ons`. Restart Blender if needed.
- **No Valid Objects/Camera**: Check that selected items are meshes/cameras; use poll functions for validation.
- **Objects Behind Camera**: Warning indicates positive Z in camera space—reposition objects or camera.
- **Render Issues**: Verify clip planes; increase margin if clipping occurs and move the camera back along its LOCAL Z axis.
- **Errors During Compilation**: Ensure meshes have vertices; empty meshes are skipped.
- **Version Conflicts**: If using an older version of Blender, update or check compatibility.
- **Debugging**: Enable Blender's console (`Window > Toggle System Console`) for detailed logs.

If issues persist, check the add-on script for pylint annotations or report to S.A. Lowell.

For installation issues, see [installation-guide.md](installation-guide.md). For usage, see [usage.md](usage.md).

Return to [main README](../README.md) or [docs index](README.md).