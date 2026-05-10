# Diagram Sources

Excalidraw source files for diagrams embedded in the docs. Edit the `.excalidraw` source here, then export PNG to `website/public/img/`.

## Files

| Source                          | Rendered PNG                                        | Used In                                      |
| ------------------------------- | --------------------------------------------------- | -------------------------------------------- |
| `eval-test-types.excalidraw`    | `website/public/img/eval-test-types.png`            | explanation/what-are-evals.md                |

## Exporting to PNG

A headless renderer is included. From the project root:

```bash
# Install playwright once if you have not (~50 MB)
npm install --no-save playwright

# Render any source file in this folder
node docs/_diagrams/render.mjs \
  docs/_diagrams/eval-test-types.excalidraw \
  website/public/img/eval-test-types.png \
  2
```

The third arg is the scale factor (2 = retina). The renderer loads `@excalidraw/utils` from esm.sh, exports to canvas, and writes the PNG. Internet is required on the first run; thereafter esm.sh caches.

If you prefer the GUI, drag the `.excalidraw` onto [excalidraw.com](https://excalidraw.com) and use File > Export image > PNG (scale 2x, white background).

The PNG is committed alongside the source so the docs render without a build step.

## Convention

- Two-character element indices only (`a0`, `aZ`, `b3`). Three-char indices like `d9a` silently break the file.
- Use distinct fill colors per logical group (e.g., workspace, artifact flow, trigger flow, output).
- Keep diagrams legible at 1200px wide.
