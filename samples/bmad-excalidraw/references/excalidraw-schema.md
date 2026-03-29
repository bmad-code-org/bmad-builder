# Excalidraw JSON Schema Reference

Reference for generating valid `.excalidraw` files. Use this when constructing diagram specifications or when direct JSON generation is needed.

## Top-Level Structure

```json
{
  "type": "excalidraw",
  "version": 2,
  "source": "bmad-excalidraw",
  "elements": [],
  "appState": {
    "gridSize": null,
    "viewBackgroundColor": "#ffffff"
  },
  "files": {}
}
```

## Element Types

Nine types: `rectangle`, `ellipse`, `diamond`, `arrow`, `line`, `freedraw`, `text`, `image`, `frame`

## Common Element Properties

Every element shares these base properties:

| Property          | Type        | Description                                             |
| ----------------- | ----------- | ------------------------------------------------------- |
| `id`              | string      | Unique identifier (use nanoid-style, 8+ chars)          |
| `type`            | string      | One of the nine element types                           |
| `x`               | number      | X position (pixels from origin)                         |
| `y`               | number      | Y position (pixels from origin)                         |
| `width`           | number      | Element width in pixels                                 |
| `height`          | number      | Element height in pixels                                |
| `angle`           | number      | Rotation in radians (0 = no rotation)                   |
| `strokeColor`     | string      | Border/stroke color (hex, e.g. `"#1e1e1e"`)             |
| `backgroundColor` | string      | Fill color (`"transparent"` or hex)                     |
| `fillStyle`       | string      | `"solid"`, `"hachure"`, `"cross-hatch"`                 |
| `strokeWidth`     | number      | Line thickness (1, 2, or 4)                             |
| `strokeStyle`     | string      | `"solid"`, `"dashed"`, `"dotted"`                       |
| `roughness`       | number      | 0 (architect/sharp), 1 (artist/default), 2 (cartoonist) |
| `opacity`         | number      | 0-100 (100 = fully opaque)                              |
| `groupIds`        | array       | Group membership `["group-id"]`                         |
| `frameId`         | string/null | Containing frame ID                                     |
| `roundness`       | object/null | `{"type": 3}` for rounded corners, `null` for sharp     |
| `seed`            | number      | Random seed for hand-drawn rendering                    |
| `version`         | number      | Element version counter (start at 1)                    |
| `versionNonce`    | number      | Random nonce for version (any integer)                  |
| `isDeleted`       | boolean     | Soft-delete flag (always `false` for new elements)      |
| `boundElements`   | array/null  | Elements bound to this one                              |
| `updated`         | number      | Timestamp in milliseconds                               |
| `link`            | string/null | Optional hyperlink                                      |
| `locked`          | boolean     | Whether element is locked                               |

## Shape Elements (rectangle, ellipse, diamond)

Use common properties only. For bound text, add to `boundElements`:

```json
{
  "id": "rect1",
  "type": "rectangle",
  "x": 100,
  "y": 100,
  "width": 200,
  "height": 80,
  "strokeColor": "#1e1e1e",
  "backgroundColor": "#a5d8ff",
  "fillStyle": "solid",
  "strokeWidth": 2,
  "strokeStyle": "solid",
  "roughness": 1,
  "opacity": 100,
  "groupIds": [],
  "frameId": null,
  "roundness": { "type": 3 },
  "seed": 12345,
  "version": 1,
  "versionNonce": 67890,
  "isDeleted": false,
  "boundElements": [
    { "id": "text1", "type": "text" },
    { "id": "arrow1", "type": "arrow" }
  ],
  "updated": 1700000000000,
  "link": null,
  "locked": false
}
```

## Text Elements

Additional properties for text:

| Property        | Type        | Description                                             |
| --------------- | ----------- | ------------------------------------------------------- |
| `text`          | string      | The displayed text                                      |
| `fontSize`      | number      | Font size (16, 20, 28, 36)                              |
| `fontFamily`    | number      | 1 (Virgil/hand-drawn), 2 (Helvetica), 3 (Cascadia/mono) |
| `textAlign`     | string      | `"left"`, `"center"`, `"right"`                         |
| `verticalAlign` | string      | `"top"`, `"middle"`                                     |
| `containerId`   | string/null | Parent shape ID (when text is inside a shape)           |
| `originalText`  | string      | Same as `text`                                          |
| `autoResize`    | boolean     | Whether text auto-resizes (`true`)                      |
| `lineHeight`    | number      | Line height multiplier (1.25 default)                   |

**Bound text** (text inside a shape):

```json
{
  "id": "text1",
  "type": "text",
  "x": 120,
  "y": 125,
  "width": 160,
  "height": 25,
  "text": "Process Step",
  "fontSize": 20,
  "fontFamily": 1,
  "textAlign": "center",
  "verticalAlign": "middle",
  "containerId": "rect1",
  "originalText": "Process Step",
  "autoResize": true,
  "lineHeight": 1.25
}
```

## Linear Elements (arrow, line)

Additional properties:

| Property             | Type        | Description                                       |
| -------------------- | ----------- | ------------------------------------------------- |
| `points`             | array       | Array of `[x, y]` offsets from element origin     |
| `startBinding`       | object/null | Connection to start element                       |
| `endBinding`         | object/null | Connection to end element                         |
| `startArrowhead`     | string/null | `null`, `"arrow"`, `"bar"`, `"dot"`, `"triangle"` |
| `endArrowhead`       | string/null | Same options as startArrowhead                    |
| `lastCommittedPoint` | null        | Always `null`                                     |

**Arrow connecting two shapes:**

```json
{
  "id": "arrow1",
  "type": "arrow",
  "x": 300,
  "y": 140,
  "width": 100,
  "height": 0,
  "points": [
    [0, 0],
    [100, 0]
  ],
  "startBinding": {
    "elementId": "rect1",
    "focus": 0,
    "gap": 1,
    "fixedPoint": [1, 0.5]
  },
  "endBinding": {
    "elementId": "rect2",
    "focus": 0,
    "gap": 1,
    "fixedPoint": [0, 0.5]
  },
  "startArrowhead": null,
  "endArrowhead": "arrow",
  "lastCommittedPoint": null
}
```

**Binding fixedPoint values:**

- `[0, 0.5]` = left center
- `[1, 0.5]` = right center
- `[0.5, 0]` = top center
- `[0.5, 1]` = bottom center

## Frame Elements

Frames act as containers. Other elements reference frames via `frameId`.

```json
{
  "id": "frame1",
  "type": "frame",
  "x": 50,
  "y": 50,
  "width": 500,
  "height": 400,
  "name": "Backend Services"
}
```

## Color Palette

### Recommended stroke colors

- `"#1e1e1e"` — Black (default)
- `"#e03131"` — Red
- `"#2f9e44"` — Green
- `"#1971c2"` — Blue
- `"#f08c00"` — Orange
- `"#6741d9"` — Purple

### Recommended background colors

- `"transparent"` — No fill
- `"#a5d8ff"` — Light blue
- `"#b2f2bb"` — Light green
- `"#ffc9c9"` — Light red/pink
- `"#ffec99"` — Light yellow
- `"#d0bfff"` — Light purple
- `"#e9ecef"` — Light gray

## Layout Constants

Use these for consistent spacing:

| Constant                  | Value     | Use                        |
| ------------------------- | --------- | -------------------------- |
| Element width (standard)  | 200       | Rectangles, diamonds       |
| Element height (standard) | 80        | Rectangles                 |
| Diamond size              | 140 x 100 | Decision diamonds          |
| Ellipse size              | 160 x 60  | Start/end terminals        |
| Horizontal gap            | 80        | Between elements (LR flow) |
| Vertical gap              | 60        | Between elements (TB flow) |
| Text padding              | 20        | Inside shapes              |
| Frame padding             | 40        | Inside frames              |
| Font size (label)         | 20        | Standard labels            |
| Font size (title)         | 28        | Titles/headers             |
| Font size (small)         | 16        | Annotations                |
