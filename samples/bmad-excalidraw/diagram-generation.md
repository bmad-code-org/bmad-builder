**Language:** Use `{communication_language}` for all output.
**Output Location:** `{output_folder}/diagrams/`

# Diagram Generation

This stage receives either a confirmed specification from the guided-design stage or an inferred description from the user's autonomous/YOLO request. If a complete spec was confirmed in a prior stage, skip directly to Step 2. If inferring from user input, build the spec in Step 1 from the conversation context.

Generate a valid `.excalidraw` file from the diagram specification. Use the schema reference and generation script to produce a well-laid-out, visually clean diagram.

## Step 1: Build the Diagram Specification

Create a JSON specification that the generation script can consume. Load `references/excalidraw-schema.md` for the element format reference.

The specification format:

```json
{
  "title": "Diagram Title",
  "type": "flowchart|architecture|sequence|mindmap|er|swimlane|dataflow|wireframe|network|comparison|freeform",
  "direction": "LR|TB|RL|BT",
  "elements": [
    {
      "id": "unique-id",
      "type": "rectangle|diamond|ellipse|text",
      "label": "Display Text",
      "group": "optional-group-name"
    }
  ],
  "connections": [
    {
      "from": "source-id",
      "to": "target-id",
      "label": "optional label",
      "style": "arrow|line|dashed"
    }
  ],
  "groups": [
    {
      "name": "group-name",
      "label": "Group Label",
      "type": "frame|background"
    }
  ]
}
```

## Step 2: Generate the Excalidraw File

Run the generation script:

```bash
python3 scripts/generate_excalidraw.py --spec '<json-spec>' --output '{output_folder}/diagrams/{filename}.excalidraw'
```

Or pipe the spec via stdin:

```bash
echo '<json-spec>' | python3 scripts/generate_excalidraw.py --output '{output_folder}/diagrams/{filename}.excalidraw'
```

The script handles:

- Auto-layout based on diagram type and direction
- Element sizing based on text content
- Arrow routing between elements
- Proper spacing and alignment
- Hand-drawn style defaults (roughness, rounded corners)
- Unique ID generation for all elements

## Step 3: Validate

Run validation:

```bash
python3 scripts/validate_excalidraw.py '{output_folder}/diagrams/{filename}.excalidraw'
```

Fix any critical issues before delivering.

## Step 4: Deliver

Present the result:

1. Confirm the file was saved: "Diagram saved to `{output_folder}/diagrams/{filename}.excalidraw`"
2. Summarize what was created: element count, diagram type, key components
3. Explain how to open it: "Open in Excalidraw (excalidraw.com) or any compatible editor"

**For Guided/YOLO mode:** Ask "Want me to adjust anything — add elements, change layout, restyle?"

**For Autonomous mode:** Just output the file path and a one-line summary.

## Iteration

If the user wants changes:

- Read the existing file
- Apply modifications to the spec
- Re-run generation
- Re-validate and deliver

## Progression

**Guided/YOLO mode:** When the user confirms no further changes or declines the adjustment offer, this stage is complete. Confirm the final file path and summarize the diagram.

**Autonomous mode:** Stage completes immediately after the deliver step — output file path and one-line summary, then done. No iteration.
