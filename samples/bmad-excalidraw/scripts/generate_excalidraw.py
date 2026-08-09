# /// script
# requires-python = ">=3.9"
# ///
"""
Excalidraw Diagram Generator

Takes a diagram specification JSON and produces a valid .excalidraw file
with auto-layout positioning.

Usage:
    uv run generate_excalidraw.py --spec '{"title":"My Diagram",...}' --output diagram.excalidraw
    echo '{"title":"My Diagram",...}' | uv run generate_excalidraw.py --output diagram.excalidraw
    uv run generate_excalidraw.py --spec-file spec.json --output diagram.excalidraw

Spec format:
{
  "title": "Diagram Title",
  "type": "flowchart|architecture|sequence|mindmap|er|swimlane|freeform|network|comparison",
  "direction": "LR|TB|RL|BT",
  "elements": [
    {"id": "e1", "type": "rectangle", "label": "Step 1", "group": "optional"},
    {"id": "e2", "type": "diamond", "label": "Decision?"},
    {"id": "e3", "type": "ellipse", "label": "End"}
  ],
  "connections": [
    {"from": "e1", "to": "e2", "label": "next", "style": "arrow"},
    {"from": "e2", "to": "e3", "label": "yes", "style": "arrow"}
  ],
  "groups": [
    {"name": "group-name", "label": "Group Label", "type": "frame"}
  ]
}
"""

import argparse
import json
import math
import random
import sys
import time
from pathlib import Path


# --- Constants ---

ELEMENT_SIZES = {
    "rectangle": (200, 80),
    "diamond": (140, 100),
    "ellipse": (160, 60),
    "text": (200, 30),
}

GAPS = {
    "horizontal": 80,
    "vertical": 60,
}

COLORS = {
    "stroke": "#1e1e1e",
    "bg_blue": "#a5d8ff",
    "bg_green": "#b2f2bb",
    "bg_red": "#ffc9c9",
    "bg_yellow": "#ffec99",
    "bg_purple": "#d0bfff",
    "bg_gray": "#e9ecef",
}

BG_CYCLE = ["bg_blue", "bg_green", "bg_yellow", "bg_purple", "bg_red", "bg_gray"]


def generate_id(length=8):
    """Generate a random alphanumeric ID."""
    chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    return "".join(random.choice(chars) for _ in range(length))


def generate_seed():
    """Generate a random seed for hand-drawn rendering."""
    return random.randint(100000, 999999999)


def now_ms():
    """Current time in milliseconds."""
    return int(time.time() * 1000)


# --- Element Builders ---


def make_base_element(elem_type, x, y, width, height, **overrides):
    """Create a base element with all required properties."""
    base = {
        "id": generate_id(),
        "type": elem_type,
        "x": x,
        "y": y,
        "width": width,
        "height": height,
        "angle": 0,
        "strokeColor": COLORS["stroke"],
        "backgroundColor": "transparent",
        "fillStyle": "solid",
        "strokeWidth": 2,
        "strokeStyle": "solid",
        "roughness": 1,
        "opacity": 100,
        "groupIds": [],
        "frameId": None,
        "roundness": {"type": 3} if elem_type in ("rectangle", "diamond", "ellipse") else None,
        "seed": generate_seed(),
        "version": 1,
        "versionNonce": random.randint(1, 999999999),
        "isDeleted": False,
        "boundElements": [],
        "updated": now_ms(),
        "link": None,
        "locked": False,
    }
    base.update(overrides)
    return base


def make_shape(elem_type, x, y, label, width=None, height=None, bg_color=None):
    """Create a shape element (rectangle, diamond, ellipse) with bound text."""
    default_w, default_h = ELEMENT_SIZES.get(elem_type, (200, 80))
    w = width or default_w
    h = height or default_h

    # Auto-size based on text length
    text_width = len(label) * 10 + 40
    if text_width > w:
        w = text_width

    shape = make_base_element(elem_type, x, y, w, h)
    if bg_color:
        shape["backgroundColor"] = COLORS.get(bg_color, bg_color)

    # Create bound text
    text_elem = make_text(x, y, label, container_id=shape["id"], width=w, height=h)
    shape["boundElements"] = [{"id": text_elem["id"], "type": "text"}]

    return shape, text_elem


def make_text(x, y, text, container_id=None, width=200, height=80, font_size=20):
    """Create a text element, optionally bound to a container."""
    text_height = 25
    text_width = len(text) * 10

    if container_id:
        # Center text in container
        tx = x + (width - text_width) / 2
        ty = y + (height - text_height) / 2
    else:
        tx = x
        ty = y

    elem = make_base_element("text", tx, ty, text_width, text_height)
    elem.update({
        "text": text,
        "fontSize": font_size,
        "fontFamily": 1,
        "textAlign": "center",
        "verticalAlign": "middle",
        "containerId": container_id,
        "originalText": text,
        "autoResize": True,
        "lineHeight": 1.25,
        "roundness": None,
    })
    return elem


def make_arrow(x1, y1, x2, y2, start_id=None, end_id=None, label=None,
               style="arrow", start_shape=None, end_shape=None):
    """Create an arrow/line element connecting two points or elements."""
    dx = x2 - x1
    dy = y2 - y1
    width = abs(dx)
    height = abs(dy)

    elem = make_base_element("arrow", x1, y1, width, height)
    elem.update({
        "points": [[0, 0], [dx, dy]],
        "startArrowhead": None,
        "endArrowhead": "arrow" if style != "line" else None,
        "lastCommittedPoint": None,
        "roundness": {"type": 2},
    })

    if style == "dashed":
        elem["strokeStyle"] = "dashed"

    if start_id and start_shape:
        sw, sh = start_shape["width"], start_shape["height"]
        # Determine fixedPoint based on direction
        fp = _compute_fixed_point(dx, dy, "start")
        elem["startBinding"] = {
            "elementId": start_id,
            "focus": 0,
            "gap": 1,
            "fixedPoint": fp,
        }

    if end_id and end_shape:
        fp = _compute_fixed_point(dx, dy, "end")
        elem["endBinding"] = {
            "elementId": end_id,
            "focus": 0,
            "gap": 1,
            "fixedPoint": fp,
        }

    elements = [elem]

    # Add label text on arrow if specified
    if label:
        mid_x = x1 + dx / 2
        mid_y = y1 + dy / 2 - 15
        label_elem = make_text(mid_x, mid_y, label, font_size=16)
        elem["boundElements"] = [{"id": label_elem["id"], "type": "text"}]
        label_elem["containerId"] = elem["id"]
        elements.append(label_elem)

    # Register arrow in shape boundElements
    if start_id and start_shape:
        if "boundElements" not in start_shape:
            start_shape["boundElements"] = []
        start_shape["boundElements"].append({"id": elem["id"], "type": "arrow"})

    if end_id and end_shape:
        if "boundElements" not in end_shape:
            end_shape["boundElements"] = []
        end_shape["boundElements"].append({"id": elem["id"], "type": "arrow"})

    return elements


def _compute_fixed_point(dx, dy, end):
    """Compute fixedPoint for binding based on arrow direction."""
    if abs(dx) > abs(dy):
        # Horizontal arrow
        if dx > 0:
            return [1, 0.5] if end == "start" else [0, 0.5]
        else:
            return [0, 0.5] if end == "start" else [1, 0.5]
    else:
        # Vertical arrow
        if dy > 0:
            return [0.5, 1] if end == "start" else [0.5, 0]
        else:
            return [0.5, 0] if end == "start" else [0.5, 1]


def make_frame(x, y, width, height, name):
    """Create a frame element."""
    elem = make_base_element("frame", x, y, width, height)
    elem["name"] = name
    elem["roundness"] = None
    return elem


# --- Layout Engines ---


def layout_grid(elements, direction="LR", start_x=100, start_y=100):
    """
    Position elements in a grid layout based on connection topology.
    Returns dict mapping element ID to (x, y) position.
    """
    positions = {}
    n = len(elements)
    if n == 0:
        return positions

    if direction in ("LR", "RL"):
        # Arrange in rows with horizontal flow
        cols = math.ceil(math.sqrt(n))
        for i, elem in enumerate(elements):
            col = i % cols
            row = i // cols
            ew, eh = ELEMENT_SIZES.get(elem.get("type", "rectangle"), (200, 80))
            x = start_x + col * (ew + GAPS["horizontal"])
            y = start_y + row * (eh + GAPS["vertical"])
            if direction == "RL":
                x = start_x + (cols - 1 - col) * (ew + GAPS["horizontal"])
            positions[elem["id"]] = (x, y)
    else:
        # TB/BT — arrange in columns with vertical flow
        rows = math.ceil(math.sqrt(n))
        for i, elem in enumerate(elements):
            row = i % rows
            col = i // rows
            ew, eh = ELEMENT_SIZES.get(elem.get("type", "rectangle"), (200, 80))
            x = start_x + col * (ew + GAPS["horizontal"])
            y = start_y + row * (eh + GAPS["vertical"])
            if direction == "BT":
                y = start_y + (rows - 1 - row) * (eh + GAPS["vertical"])
            positions[elem["id"]] = (x, y)

    return positions


def layout_linear(elements, connections, direction="LR", start_x=100, start_y=100):
    """
    Position elements in a linear chain following connections.
    Better for flowcharts than grid layout.
    """
    if not elements:
        return {}

    # Build adjacency from connections
    adj = {}
    incoming = set()
    for conn in connections:
        adj.setdefault(conn["from"], []).append(conn["to"])
        incoming.add(conn["to"])

    # Find root nodes (no incoming connections)
    all_ids = [e["id"] for e in elements]
    roots = [eid for eid in all_ids if eid not in incoming]
    if not roots:
        roots = [all_ids[0]]

    # BFS to determine levels
    levels = {}
    visited = set()
    queue = [(r, 0) for r in roots]
    for r in roots:
        visited.add(r)

    while queue:
        node, level = queue.pop(0)
        levels.setdefault(level, []).append(node)
        for neighbor in adj.get(node, []):
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append((neighbor, level + 1))

    # Place unvisited nodes at the end
    for eid in all_ids:
        if eid not in visited:
            max_level = max(levels.keys()) + 1 if levels else 0
            levels.setdefault(max_level, []).append(eid)

    # Compute positions
    positions = {}
    elem_lookup = {e["id"]: e for e in elements}

    for level, nodes in sorted(levels.items()):
        for lane, node_id in enumerate(nodes):
            elem = elem_lookup.get(node_id, {})
            ew, eh = ELEMENT_SIZES.get(elem.get("type", "rectangle"), (200, 80))

            if direction in ("LR", "RL"):
                x = start_x + level * (ew + GAPS["horizontal"])
                y = start_y + lane * (eh + GAPS["vertical"])
                if direction == "RL":
                    max_level = max(levels.keys())
                    x = start_x + (max_level - level) * (ew + GAPS["horizontal"])
            else:
                x = start_x + lane * (ew + GAPS["horizontal"])
                y = start_y + level * (eh + GAPS["vertical"])
                if direction == "BT":
                    max_level = max(levels.keys())
                    y = start_y + (max_level - level) * (eh + GAPS["vertical"])

            positions[node_id] = (x, y)

    return positions


def layout_radial(elements, connections, start_x=500, start_y=400):
    """Position elements in a radial layout for mind maps."""
    if not elements:
        return {}

    positions = {}
    center_id = elements[0]["id"]
    positions[center_id] = (start_x, start_y)

    # Find children of center
    children = []
    for conn in connections:
        if conn["from"] == center_id:
            children.append(conn["to"])

    if not children:
        # No connections — arrange all around center
        children = [e["id"] for e in elements[1:]]

    radius = 250
    for i, child_id in enumerate(children):
        angle = (2 * math.pi * i) / len(children) - math.pi / 2
        x = start_x + radius * math.cos(angle)
        y = start_y + radius * math.sin(angle)
        positions[child_id] = (x, y)

    # Place any remaining elements further out
    remaining = [e["id"] for e in elements if e["id"] not in positions]
    if remaining:
        radius2 = 450
        for i, eid in enumerate(remaining):
            angle = (2 * math.pi * i) / len(remaining)
            x = start_x + radius2 * math.cos(angle)
            y = start_y + radius2 * math.sin(angle)
            positions[eid] = (x, y)

    return positions


# --- Main Generator ---


def generate_excalidraw(spec):
    """Generate a complete .excalidraw JSON from a diagram specification."""
    diagram_type = spec.get("type", "flowchart")
    direction = spec.get("direction", "TB" if diagram_type == "sequence" else "LR")
    spec_elements = spec.get("elements", [])
    spec_connections = spec.get("connections", [])
    spec_groups = spec.get("groups", [])

    # Choose layout engine
    if diagram_type == "mindmap":
        positions = layout_radial(spec_elements, spec_connections)
    elif spec_connections:
        positions = layout_linear(spec_elements, spec_connections, direction)
    else:
        positions = layout_grid(spec_elements, direction)

    # Build Excalidraw elements
    all_elements = []
    shape_lookup = {}  # id -> shape element (for arrow binding)
    id_mapping = {}  # spec id -> generated element id

    # Create group frames first
    group_id_map = {}
    for group in spec_groups:
        group_name = group["name"]
        group_label = group.get("label", group_name)
        # Find elements in this group to compute frame bounds
        group_elem_ids = [e["id"] for e in spec_elements if e.get("group") == group_name]
        if group_elem_ids:
            min_x = min(positions.get(eid, (100, 100))[0] for eid in group_elem_ids) - 40
            min_y = min(positions.get(eid, (100, 100))[1] for eid in group_elem_ids) - 50
            max_x = max(positions.get(eid, (100, 100))[0] + 200 for eid in group_elem_ids) + 40
            max_y = max(positions.get(eid, (100, 100))[1] + 80 for eid in group_elem_ids) + 40

            frame = make_frame(min_x, min_y, max_x - min_x, max_y - min_y, group_label)
            group_id_map[group_name] = frame["id"]
            all_elements.append(frame)

    # Create shape elements
    bg_idx = 0
    for spec_elem in spec_elements:
        eid = spec_elem["id"]
        etype = spec_elem.get("type", "rectangle")
        label = spec_elem.get("label", "")
        x, y = positions.get(eid, (100, 100))

        # Pick background color
        bg_color = spec_elem.get("color", None)
        if not bg_color:
            if etype == "diamond":
                bg_color = "bg_yellow"
            elif etype == "ellipse":
                bg_color = "bg_gray"
            else:
                bg_color = BG_CYCLE[bg_idx % len(BG_CYCLE)]
                bg_idx += 1

        shape, text = make_shape(etype, x, y, label, bg_color=bg_color)

        # Assign to frame if in a group
        group_name = spec_elem.get("group")
        if group_name and group_name in group_id_map:
            shape["frameId"] = group_id_map[group_name]
            text["frameId"] = group_id_map[group_name]

        shape_lookup[eid] = shape
        id_mapping[eid] = shape["id"]
        all_elements.extend([shape, text])

    # Create connections
    for conn in spec_connections:
        from_id = conn["from"]
        to_id = conn["to"]
        label = conn.get("label")
        style = conn.get("style", "arrow")

        from_shape = shape_lookup.get(from_id)
        to_shape = shape_lookup.get(to_id)

        if not from_shape or not to_shape:
            print(f"Warning: skipping connection {from_id} -> {to_id}, element not found", file=sys.stderr)
            continue

        # Compute arrow start/end points (from shape centers/edges)
        fx = from_shape["x"] + from_shape["width"] / 2
        fy = from_shape["y"] + from_shape["height"] / 2
        tx = to_shape["x"] + to_shape["width"] / 2
        ty = to_shape["y"] + to_shape["height"] / 2

        # Adjust to edges
        dx = tx - fx
        dy = ty - fy

        if abs(dx) > abs(dy):
            # Horizontal connection
            if dx > 0:
                sx = from_shape["x"] + from_shape["width"]
                ex = to_shape["x"]
            else:
                sx = from_shape["x"]
                ex = to_shape["x"] + to_shape["width"]
            sy = fy
            ey = ty
        else:
            # Vertical connection
            sx = fx
            ex = tx
            if dy > 0:
                sy = from_shape["y"] + from_shape["height"]
                ey = to_shape["y"]
            else:
                sy = from_shape["y"]
                ey = to_shape["y"] + to_shape["height"]

        arrow_elems = make_arrow(
            sx, sy, ex, ey,
            start_id=from_shape["id"], end_id=to_shape["id"],
            label=label, style=style,
            start_shape=from_shape, end_shape=to_shape,
        )
        all_elements.extend(arrow_elems)

    # Add title if specified
    title = spec.get("title")
    if title:
        # Place title above the diagram
        min_y = min(e["y"] for e in all_elements if "y" in e) if all_elements else 100
        min_x = min(e["x"] for e in all_elements if "x" in e) if all_elements else 100
        title_elem = make_text(min_x, min_y - 50, title, font_size=28)
        all_elements.insert(0, title_elem)

    # Assemble the document
    doc = {
        "type": "excalidraw",
        "version": 2,
        "source": "bmad-excalidraw",
        "elements": all_elements,
        "appState": {
            "gridSize": None,
            "viewBackgroundColor": "#ffffff",
        },
        "files": {},
    }

    return doc


def main():
    parser = argparse.ArgumentParser(
        description="Generate Excalidraw diagrams from a JSON specification",
    )
    parser.add_argument("--spec", help="JSON specification string")
    parser.add_argument("--spec-file", help="Path to JSON specification file")
    parser.add_argument("--output", "-o", required=True, help="Output .excalidraw file path")
    parser.add_argument("--help-spec", action="store_true", help="Show specification format")

    args = parser.parse_args()

    if args.help_spec:
        print(__doc__)
        sys.exit(0)

    # Read spec from args, file, or stdin
    if args.spec:
        spec = json.loads(args.spec)
    elif args.spec_file:
        spec = json.loads(Path(args.spec_file).read_text())
    elif not sys.stdin.isatty():
        spec = json.loads(sys.stdin.read())
    else:
        print("Error: provide --spec, --spec-file, or pipe JSON to stdin", file=sys.stderr)
        sys.exit(2)

    # Generate
    doc = generate_excalidraw(spec)

    # Write output
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(doc, indent=2))

    print(json.dumps({
        "status": "success",
        "output": str(output_path),
        "elements": len(doc["elements"]),
        "type": spec.get("type", "flowchart"),
    }))


if __name__ == "__main__":
    main()
