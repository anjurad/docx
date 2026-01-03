---
name: render-from-manifest
description: "Deterministically re-render a Word document using only an existing session manifest."
argument-hint: "session=..."
agent: Document Renderer Agent
tools: ['read', 'edit', 'search']
---

# Render Word Document From Manifest

## Purpose

This prompt regenerates a Microsoft Word (.docx) document using only
the information recorded in an existing session manifest.

No content is authored, inferred, edited, or overridden.

## Specifications

Follow the session manifest specification defined in:

- .github/specs/session-manifest.spec.md

The manifest is authoritative.

## Required Input

- ${input:session}

This must identify an existing session directory:

sessions/<session-id>/

If the input is missing, stop and report the error.

## Load Session Manifest

1. Resolve the session directory:
   - sessions/<session-id>/

2. Read:
   - sessions/<session-id>/session.manifest.yml

3. Validate that the manifest:
   - Exists
   - Conforms to the specification
   - Contains all required sections and fields

If validation fails, stop and report exactly what is missing or invalid.

## Required Manifest Fields

### Inputs
- inputs.markdown_file
- inputs.images_dir

### Conversion
- conversion.docx_mode
- conversion.template_file
- conversion.resource_path
- conversion.embed_media
- conversion.fail_on_missing_images

### Outputs
- outputs.docx_file

If any required field is missing, stop and report it.

## Validation Phase

Before rendering:

- Verify inputs.markdown_file exists.
- Verify conversion.template_file exists.
- Verify all images referenced by the Markdown resolve locally.
- Verify all paths are workspace-relative and explicit.

If validation fails, stop and report the issue.

## Rendering Phase

- Render the Word document by converting the Markdown file specified in inputs.markdown_file.
- Use the Word template specified in conversion.template_file.
- Apply conversion behaviour strictly as defined in the manifest.
- Do not modify, reinterpret, or restructure content.

## Manifest Update

After successful rendering:

Append a new entry to history:

- timestamp_utc: <current UTC timestamp>
  action: regenerate
  details: "Re-rendered DOCX strictly from session manifest"

Do not modify any other manifest fields.

If rendering fails:
- Do not update the manifest.
- Report the failure.

## Output Contract

Return:

1) Path to the regenerated .docx file
2) Path to session.manifest.yml
3) Execution status (success or failure)

## Behavioural Constraints

- Do not accept overrides.
- Do not ask questions.
- Do not infer missing values.
- Do not change content.
- Do not change templates.
- Do not change paths.

This prompt must be fully deterministic.
