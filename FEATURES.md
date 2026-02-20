# Features Reference

Quick reference guide for all features in the CMSSW Graph Visualization tool.

## Table of Contents

- [Graph Visualization](#graph-visualization)
- [Module Details Panel](#module-details-panel)
- [Search & Navigation](#search--navigation)
- [Focus & Filtering](#focus--filtering)
- [Dependency Analysis](#dependency-analysis)
- [Keyboard Shortcuts](#keyboard-shortcuts)

---

## Graph Visualization

### Visual Encoding

**Node Colors:**
- 🟢 **Green** (`#2ecc71`): Reconstruction modules (reco workflow)
- ⚪ **Gray** (`#d3d3d3`): Analysis modules (PAT/analysis workflow)

**Node Shapes:**
- **Diamond** (◆): EDFilter modules
- **Rectangle** (▭): EDProducer and EDAnalyzer modules

**Node Size:** 50×35 pixels with visible labels

**Edge Style:**
- Directed arrows showing dependency flow
- Bezier curves to reduce overlap
- Color inherited from source node attributes

### Interaction

| Action | Gesture |
|--------|---------|
| **Pan graph** | Click + drag on background |
| **Zoom** | Mouse wheel / pinch |
| **Select node** | Click on node |
| **View details** | Click opens side panel |
| **Hover tooltip** | Mouse over node (if available) |

### Layout

- **Algorithm**: COSE (Compound Spring Embedder) - force-directed
- **Node repulsion**: 800,000 (high spacing)
- **Ideal edge length**: 250px
- **Initial temperature**: 200
- **Iterations**: 1,000

---

## Module Details Panel

### Display Sections

1. **Module Header**
   - Module name (large, bold)
   - Type (EDProducer, EDFilter, EDAnalyzer)
   - Plugin class name

2. **Input Tags Section**
   - Regular InputTags (individual items)
   - VInputTag groups (expandable lists)
   - ESInputTag (Event Setup inputs)
   - Color coding:
     - Blue background: Clickable (found in graph)
     - Red background: Not found in graph

3. **Parameters Section**
   - All non-InputTag parameters
   - Type annotations (cms.int32, cms.string, etc.)
   - Values displayed verbatim

4. **Raw Configuration**
   - Original Python config snippet
   - Monospace font for readability

### Panel Interactions

**Resize:**
- Drag the left edge to adjust width
- Min width: 300px
- Max width: 80% of viewport
- Width saved to localStorage

**Navigate:**
- Click any InputTag to jump to that module
- Breadcrumbs show navigation history
- Click breadcrumb to go back

**Close:**
- Click × button in header
- Press **Esc** key
- Click graph background

---

## Search & Navigation

### Search Module

**Location:** Top controls bar

**Usage:**
1. Type module name (partial match, case-insensitive)
2. Press **Enter** or click **Find**

**Results:**
- **Single match**: Opens panel, zooms to node
- **Multiple matches**: Highlights all, dims others
- **No matches**: Alert dialog

**Clear:**
- Click **Clear** button
- Resets all highlights
- Fits full graph to view

### Breadcrumb Navigation

**Location:** Side panel header

**Display:** `ModuleA › ModuleB › ModuleC`

**Interaction:**
- Current module: Plain text (not clickable)
- Previous modules: Blue, clickable
- Click any to jump back in history

---

## Focus & Filtering

### Focus Radius (Ego Graph)

**Purpose:** Show N-hop neighborhood around selected module

**Controls:**
- **Focus Radius**: 1-5 hops (number input)
- **Apply**: Show neighborhood
- **Reset View**: Restore full graph

**Algorithm:** BFS (Breadth-First Search) undirected

**Behavior:**
- Hides nodes outside N-hop radius
- Hides edges with hidden endpoints
- Fits view to visible nodes

**Example:**
- Radius 1: Show only direct neighbors
- Radius 2: Show neighbors + neighbors of neighbors

### Category Filters

**Location:** Filter controls wrapper (blue background)

**Stage Filters:**
- ☑ **Reco**: Reconstruction modules (green)
- ☑ **Analysis**: Analysis modules (gray)

**Specific Filters:**
- ☑ **PAT**: PAT (Physics Analysis Toolkit) modules
- ☑ **HLT**: High-Level Trigger modules

**Type Filters:**
- ☑ **Producer**: EDProducer modules
- ☑ **Filter**: EDFilter modules
- ☑ **Analyzer**: EDAnalyzer modules

**Quick Actions:**
- **All**: Enable all filters
- **None**: Disable all filters

**Stats Display:** Shows "Showing X of Y nodes (Z%)"

**Filter Logic:**
1. Stage filter applied first (Reco OR Analysis)
2. Specific filters applied (exclude PAT/HLT if unchecked)
3. Type filters applied (exclude Producer/Filter/Analyzer if unchecked)

---

## Dependency Analysis

### Dependency Explorer

**Purpose:** Trace upstream/downstream dependencies with configurable depth

**Controls:**
- **Selected module**: Display current module name
- **Depth**: 1-10 levels (number input)
- **Show Dependencies**: Both upstream and downstream
- **Upstream Only**: Modules this depends on (predecessors)
- **Downstream Only**: Modules that depend on this (successors)

**Requirements:**
- Must select a module first (click to open panel)

**Behavior:**
- BFS traversal up to specified depth
- Hides nodes outside dependency tree
- Highlights selected module (red border)
- Fits view to dependency tree

**Use Cases:**
- **Upstream**: "What does this module need to run?"
- **Downstream**: "What depends on this module's output?"
- **Both**: "What's the full context around this module?"

**Example:**
```
Depth 1 Upstream:
  moduleA ← moduleB ← [moduleC]
         (selected)

Depth 2 Downstream:
  [moduleC] → moduleD → moduleE
  (selected)     ↓
              moduleF
```

---

## Keyboard Shortcuts

Press **?** to toggle help overlay.

### Navigation Keys

| Key | Action | Details |
|-----|--------|---------|
| **↑** | Navigate up | Move to nearest node above |
| **↓** | Navigate down | Move to nearest node below |
| **←** | Navigate left | Move to nearest node left |
| **→** | Navigate right | Move to nearest node right |
| **Tab** | Cycle next | Move to next visible node |
| **Enter** | Open panel | Show details for selected node |

### Control Keys

| Key | Action | Details |
|-----|--------|---------|
| **Esc** | Close panel | Close side panel, clear highlights |
| **R** | Reset view | Show all nodes, fit to screen |
| **?** | Toggle help | Show/hide keyboard shortcuts |

### Visual Feedback

- **Selected node**: Orange border (`#f39c12`)
- **Highlighted node**: Red border (`#e74c3c`)
- **Dimmed node**: 30% opacity

### Notes

- Shortcuts disabled when typing in input fields
- Arrow keys navigate spatially (geometric direction)
- Tab cycles through nodes in array order
- Selection persists until cleared (Esc or R)

---

## Tips & Tricks

### Efficient Workflow

1. **Start broad, then narrow:**
   - Load full graph
   - Use filters to reduce clutter
   - Use focus radius or dependency explorer for details

2. **Follow the data flow:**
   - Click a module
   - Click its InputTags to trace producers
   - Use breadcrumbs to backtrack

3. **Find related modules:**
   - Search for a keyword (e.g., "hgcal")
   - Multiple matches will all be highlighted
   - Use dependency explorer to see connections

4. **Keyboard navigation for exploration:**
   - Use arrow keys to browse nearby modules
   - Press Enter to quickly view details
   - Press Esc to close and continue browsing

### Performance Optimization

- **Large graphs**: Use filters early to reduce visible nodes
- **Slow layout**: Wait for initial layout to complete before interacting
- **Memory**: Close unused browser tabs if graph is very large

### Customization

- **Panel width**: Resize once, it's saved automatically
- **Layout**: Edit `graph.js` to change algorithm (dagre, breadthfirst, etc.)
- **Colors**: Edit `style.css` to change color scheme

---

## Feature Comparison

| Feature | Basic View | Focus Radius | Dependency Explorer | Filters |
|---------|-----------|--------------|---------------------|---------|
| **Shows** | All nodes | N-hop neighborhood | Dependency chain | Category subset |
| **Direction** | - | Undirected | Directed/Both | - |
| **Depth** | - | Fixed radius | Configurable | - |
| **Use case** | Overview | Local context | Trace dependencies | Reduce clutter |

---

## Data Coverage

### Input Statistics (Example Dataset)

- **Total nodes**: 1,316 modules
- **Total edges**: 3,427 dependencies
- **Module configs**: 6,383 entries
- **InputTags**: 27,992 references
- **VInputTag groups**: ~2,000

### Coverage

- ✅ **InputTag resolution**: ~95% found in graph
- ✅ **VInputTag extraction**: Supports both object and string formats
- ✅ **ESInputTag**: Fully supported
- ✅ **Parameter types**: int32, string, bool, double, and more

### Edge Cases

- InputTags pointing to non-existent modules: Shown with "not found" label
- Modules in config but not in graph: Not navigable (grayed out)
- Modules in graph but not in config: Panel shows "N/A"

---

**For full documentation, see [README.md](README.md)**
