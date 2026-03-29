# Supported Diagram Types

Reference for diagram type selection and element mapping. Use this to suggest the best diagram type for the user's needs.

## Type Catalog

### Flowchart

**Best for:** Sequential processes, decision trees, approval workflows, algorithms
**Elements:** Rectangles (steps), diamonds (decisions), ellipses (start/end), arrows (flow)
**Direction:** Usually LR (left-to-right) or TB (top-to-bottom)
**Signals:** User says "process", "steps", "decision", "if/then", "workflow", "flow"

### Architecture Diagram

**Best for:** System components, service relationships, infrastructure, tech stack
**Elements:** Rectangles (services/components), frames (boundaries/groups), arrows (data flow)
**Direction:** Usually TB or freeform
**Signals:** User says "system", "architecture", "components", "services", "infrastructure", "how things connect"

### Sequence Diagram

**Best for:** API calls, message passing, request/response flows, protocol interactions
**Elements:** Rectangles (participants), arrows (messages), text (labels)
**Direction:** TB (time flows down)
**Signals:** User says "sequence", "messages", "API flow", "request/response", "who talks to whom"

### Mind Map

**Best for:** Brainstorming, concept exploration, hierarchical categorization, knowledge organization
**Elements:** Ellipses/rectangles (nodes), lines (branches)
**Direction:** Radial from center
**Signals:** User says "brainstorm", "ideas", "categories", "mind map", "organize thoughts"

### Entity Relationship (ER) Diagram

**Best for:** Database schema, data models, entity relationships
**Elements:** Rectangles (entities), diamonds (relationships), text (attributes), arrows (connections)
**Direction:** Freeform or TB
**Signals:** User says "database", "schema", "entities", "relationships", "data model", "tables"

### Swimlane Diagram

**Best for:** Cross-functional processes, responsibility mapping, handoff visualization
**Elements:** Frames (lanes), rectangles (tasks), arrows (flow), text (labels)
**Direction:** LR with vertical lanes, or TB with horizontal lanes
**Signals:** User says "who does what", "responsibilities", "teams", "handoffs", "cross-functional"

### Data Flow Diagram

**Best for:** Data transformation pipelines, ETL processes, input/output mapping
**Elements:** Ellipses (processes), rectangles (data stores), arrows (data flow), text (labels)
**Direction:** LR or TB
**Signals:** User says "data flow", "pipeline", "transforms", "inputs/outputs", "ETL"

### Wireframe / Mockup

**Best for:** UI layout sketches, screen designs, page structure
**Elements:** Rectangles (containers/elements), text (labels/content), lines (dividers)
**Direction:** TB (page flow)
**Signals:** User says "wireframe", "mockup", "UI", "screen", "layout", "page design"

### Network / Topology Diagram

**Best for:** Network infrastructure, node relationships, cluster layouts
**Elements:** Ellipses/rectangles (nodes), lines/arrows (connections), frames (zones)
**Direction:** Freeform
**Signals:** User says "network", "topology", "nodes", "connections", "cluster"

### Comparison / Matrix

**Best for:** Feature comparisons, pros/cons, decision matrices
**Elements:** Rectangles (cells), text (labels/values), lines (grid)
**Direction:** Grid layout
**Signals:** User says "compare", "matrix", "pros/cons", "versus", "trade-offs"

## Selection Heuristic

1. Look for signal words in the user's description
2. If multiple types could work, suggest the top 2 with trade-offs
3. When in doubt, flowchart is the safest default for process-oriented requests
4. Architecture diagram is the safest default for system-oriented requests
5. Let the user override — they know their audience
