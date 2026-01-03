---
name: render-docx
description: "Render a Microsoft Word document from existing inputs using sessions, a manifest, and a Word template."
argument-hint: "session=... source_md=... template_file=... output_docx=..."
agent: Document Renderer Agent
tools: ['read', 'edit', 'search']
---

# Render Word Document Workflow

## Specifications

Follow the session manifest specification defined in:

- `.github/specs/session-manifest.spec.md`

## Load Configuration

Load repository defaults from:

- `.github/config/docx-render.defaults.yml`

User-provided inputs override defaults.

---

## Required Inputs

The following inputs are mandatory:

- `${input:session}`
- `${input:source_md}`
- `${input:template_file}`

Optional inputs:

- `${input:images_dir}`
- `${input:output_docx}`

If any required input is missing, stop and report it.

---

## Session Initialisation

1. Resolve the session directory:
   - `sessions/<session>/`

2. Create the session folder if it does not exist.

3. Create or load `session.manifest.yml`.

4. Populate the manifest with resolved values for:
   - `version`
   - `session`
   - `inputs`
   - `conversion`
   - `outputs` (placeholders allowed initially)

Do not proceed until the manifest is complete and valid.

Expected session structure:

- `source.md`
- `images/`
- `notes.md`
- `session.manifest.yml`

---

## Validation Phase

Before rendering:

- Verify `${input:source_md}` exists.
- Verify `${input:template_file}` exists.
- Verify referenced images resolve locally.
- Verify all manifest paths are explicit and correct.

If validation fails, stop and report the issue.

---

## Rendering Phase

- Convert the provided Markdown to a Word document using the specified template.
- Apply heading, list, and image mappings as defined by the conversion tool and template.
- Do not modify, interpret, or restructure content.

---

## Manifest Update

After rendering:

- Update `outputs.docx_file`.
- Append a `history` entry with:
  - `action: render`
  - A clear description of inputs and template used

If rendering fails:
- Report the failure.
- Do not modify the manifest.

---

## Output Contract

Return:

1) Path to the generated `.docx` file  
2) Path to `session.manifest.yml`  
3) A short execution status (success or failure)