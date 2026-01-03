# Session Manifest Specification

## Overview

The session manifest is a structured, human-readable YAML file that records the full context, inputs, outputs, and history of a document authoring session.

It acts as the authoritative source of truth for:

- What document was created
- Which inputs and templates were used
- Where outputs are stored
- What actions occurred and when

This specification is mandatory for all authoring workflows that create or modify documents.

## File location

```
sessions/<session-id>/session.manifest.yml
```

## Design principles

- YAML format
- Human-readable
- Explicit paths
- Append-only history
- Deterministic and reproducible

## Schema version

```yaml
version: 1
```

Increment this only when introducing breaking changes to the schema.

## Top-level structure

```yaml
version: <int>
session: <object>
document: <object>
inputs: <object>
conversion: <object>
outputs: <object>
history: <array>
```

All top-level keys are required.

## Field specifications

### session

```yaml
session:
  id: <string>
  created_utc: <ISO-8601 UTC timestamp>
  created_by: <string>
```

| Field | Required | Description |
|------|----------|-------------|
| id | Yes | Folder-safe session identifier |
| created_utc | Yes | Creation timestamp in UTC |
| created_by | Yes | Agent or user identifier |

### document

```yaml
document:
  title: <string>
  doc_type: <string>
  audience: <string>
  tone: <string>
```

| Field | Required | Description |
|------|----------|-------------|
| title | Yes | Document title |
| doc_type | Yes | spec, report, api-docs, user-guide, etc |
| audience | Yes | Primary readership |
| tone | No | Writing tone |

### inputs

```yaml
inputs:
  markdown_file: <path>
  images_dir: <path>
  sources_notes: <string | path | null>
```

| Field | Required | Description |
|------|----------|-------------|
| markdown_file | Yes | Source Markdown file |
| images_dir | Yes | Directory containing images |
| sources_notes | No | Free text or reference path |

### conversion

```yaml
conversion:
  docx_mode: <string>
  template_file: <path>
  resource_path: <string>
  embed_media: <bool>
  fail_on_missing_images: <bool>
```

| Field | Required | Description |
|------|----------|-------------|
| docx_mode | Yes | Conversion mode. Currently `convert` only |
| template_file | Yes | Word template used |
| resource_path | Yes | Asset resolution path |
| embed_media | Yes | Whether images are embedded |
| fail_on_missing_images | Yes | Whether missing images are fatal |

### outputs

```yaml
outputs:
  markdown_file: <path>
  docx_file: <path | null>
  notes_file: <path | null>
```

| Field | Required | Description |
|------|----------|-------------|
| markdown_file | Yes | Final Markdown file |
| docx_file | Conditional | Present if DOCX generated |
| notes_file | No | Notes or assumptions file |

### history

```yaml
history:
  - timestamp_utc: <ISO-8601 UTC timestamp>
    action: <string>
    details: <string>
```

Rules:

- Append-only
- Never delete or modify previous entries
- One entry per significant action

## Canonical example

```yaml
version: 1

session:
  id: "20251224-1215-riverfed-hld"
  created_utc: "2025-12-24T12:15:00Z"
  created_by: "author-agent"

document:
  title: "RiverFed High Level Design"
  doc_type: "spec"
  audience: "Data & AI stakeholders"
  tone: "Professional, concise, British English"

inputs:
  markdown_file: "sessions/20251224-1215-riverfed-hld/source.md"
  images_dir: "sessions/20251224-1215-riverfed-hld/images"
  sources_notes: null

conversion:
  docx_mode: "convert"
  template_file: "templates/word/template.docx"
  resource_path: "docs:docs/images"
  embed_media: true
  fail_on_missing_images: true

outputs:
  markdown_file: "sessions/20251224-1215-riverfed-hld/source.md"
  docx_file: "sessions/20251224-1215-riverfed-hld/output.docx"
  notes_file: "sessions/20251224-1215-riverfed-hld/notes.md"

history:
  - timestamp_utc: "2025-12-24T12:15:40Z"
    action: "create"
    details: "Initial Markdown draft created"

  - timestamp_utc: "2025-12-24T12:18:10Z"
    action: "convert"
    details: "Converted Markdown to DOCX using templates/word/template.docx"
```

## Compliance rules

- The manifest must exist before outputs are produced
- All required fields must be populated
- History is append-only
- No undocumented fields are permitted
