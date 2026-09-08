# ImageGen Prompt Detail and Length

Apply this rule whenever a scientific figure's ImageGen production prompt is adapted from a supplied or selected prompt template. It covers new candidates, split figures and revisions, including ImageGen-first workflows followed by editable PPT reconstruction. The user's requirement is a hard lower bound, not a suggestion to be concise. It governs production instructions, not how much text appears inside the figure.

## Bind the template before drafting

Use the user's explicitly selected template. If the current task continues an established template-led figure, retain that figure's bound template; do not switch to a shorter example or replace the template with the latest abbreviated correction. Record the template file/version and figure id in the existing design or reconstruction notes, not a new registry.

For a new figure with no explicitly selected template, choose and read the appropriate full file from [Bundled Prompt Templates](prompt-templates.md) after the manuscript editorial pass. This is an internal default, not a requirement for the user to supply another file. Fill and adapt its drawing instructions with verified scientific content; the installed template file, not an abbreviated outline or the short README usage example, supplies the length baseline.

Read the complete template prompt, including its common style and rendering instructions. If embedded in a conversation or document, save the actual prompt body separately from the surrounding commentary, without summarizing it. A reference PNG is a composition reference, not proof of the original prompt's length. If a required template cannot be recovered from the supplied sources, ask for the prompt rather than inventing a baseline or claiming the gate passed.

For Fig.1 and Fig.2, bind and check each separately. Never add their lengths together. If the user supplies one combined prompt as the template for splitting, each new standalone figure prompt must meet that full template's length; do not halve the threshold unless the user explicitly assigns separate baselines. Remove irrelevant scientific content from each figure while expanding its own drawing instructions to the required detail.

## Hard length gate

Use non-whitespace Unicode character count for both prompt bodies. Spaces, tabs and line breaks do not contribute. Keep the template's language unless the user requests another language; changing language is not a way to satisfy the floor. If the user specifies another counting unit, honor it explicitly and record that method instead.

The exact production text must satisfy:

`production_prompt_length >= bound_template_length`

Count only the complete text intended for the image-generation tool. Exclude the surrounding discussion, provenance report, length report and unrelated pasted material from both inputs. A library's search results or a list of asset paths are not additional drawing detail.

Save the template and production prompt as UTF-8 text files, then run the bundled check from this skill directory:

```bash
python scripts/check_prompt_length.py --template /absolute/path/template.txt --prompt /absolute/path/fig1-prompt.txt
```

Exit 0 means the length floor passed; exit 1 means the prompt is too short; exit 2 means an input is missing, unreadable or empty. A failed length check prevents the generation call: expand the actual scene instructions, save and recheck. After any edit to the prompt, rerun the check and submit that exact complete text. Do not validate a long file and send a shortened paraphrase, a pointer to that file, or only a correction delta.

Keep the template path, prompt path, lengths and decision with the existing production notes. Show a concise length comparison alongside the prompt when presenting it to the user; do not print it inside the generated figure. The helper verifies length only, not scientific correctness, absence of filler or visual quality.

## Required drawing specificity

Write the following as concrete production instructions, using the scope and proportions of the approved reference when one exists. Do not force a particular panel count or canvas ratio on unrelated papers.

1. **Figure purpose and scope.** State the single scientific message, main reading order, intended publication size and what each figure explains in a multi-figure set. Establish the scientific facts before describing their appearance.
2. **Canvas and composition.** Specify aspect ratio, relative region sizes, margins, gutters, alignments, focal hierarchy and how meaningful graphic content occupies each region. Keep an approved composition fixed during a micro-edit.
3. **Every region's visible contents.** Name its objects and visual carriers: grids, stacks, sequences, image fields, operator blocks, comparison branches or insets. Specify their local order, relative scale, placement, grouping and short visible labels. Do not substitute "draw an overview" for these instructions.
4. **Operations and correspondences.** Explain what visibly moves, changes, reverses, merges or stays associated. Specify arrow sources and targets, branch and merge points, route lanes, styles and interpretation-changing order. Position identity must not silently imply equal feature values.
5. **Exact scientific text.** Supply required labels, symbols, dimensions, formulas, index conventions, metric definitions and parameter relationships from the source. A value without its correct definition is insufficient. Do not fabricate indices, activations or results to fill a template.
6. **Visual grammar.** Specify role-based colors, typography hierarchy, stroke and border behavior, arrow conventions, depth cues and image-to-text balance. For a referenced revision, say which existing styles and arrangements remain unchanged.
7. **Atomic empirical assets.** Describe each field's role, source binding, pairing, crop/display treatment and whether it will be inserted after generation. Generative illustrations cannot substitute for preserved MRI/CT pixels, measured curves or computed geometry. Retain symbolic grids and tokens where they explain an operation better than a photograph.
8. **Rendering and change boundaries.** Identify which words should actually be printed and which prose is drawing guidance. Specify local fit, unobstructed connectors and readable output. For revisions, name the allowed changes and the surrounding content that must remain fixed; reproduce the full updated instructions, not just this change list.

Inspect applicable template instructions region by region. Each must be retained, adapted to a source-grounded drawing instruction, or omitted for a concrete scope/content reason recorded in the working notes. An omitted scientific panel does not lower the length floor or justify importing it into another figure to fill space.

Length and detail are separate requirements. Reject repetition, strings of aesthetic adjectives, copied unrelated material, inflated warning lists and invented scientific complexity as padding. If short, add missing object geometry, placement, relation, label, preservation or asset instructions. A long prompt should yield a precise image with short labels, not a text-heavy poster. Respect the user's removal of disclaimer/status text while retaining necessary algorithm definitions and conditions.

## Continue the approved workflow

Only after length and source-grounded detail are satisfied should the prompt enter ImageGen. Inspect the actual result for correspondence to the prompt and reference; length does not guarantee fidelity. Once the user approves the visual draft, use it as the composition authority for editable PPT translation and local real-data replacement. Do not reinterpret a detailed prompt as permission to redesign the accepted figure.
