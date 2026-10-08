# COHE academic redesign — local visual review

This document records the completed local visual-review handoff. At that
handoff, no commit had been pushed, no deployment had been triggered, and the
existing public site was unchanged.

The user subsequently approved publication with "일단 ㄱㄱ". The visual-approval
requirement is satisfied; the approved redesign may now be published through
the existing GitHub Pages workflow. The validation and screenshots below record
the reviewed version.

## Design

- White background, dark text, neutral borders, and a restrained muted-blue accent.
- Inter/Arial typography; 36px desktop and 27px mobile title, 26px/24px section
  headings, and a 960px maximum content width.
- Centered title, authors, university, optional department details, and exactly
  three bordered resource buttons: Paper, Code, and Checkpoints.
- Section order: title/resources, motivation, framework, abstract, experimental
  results, additional paper figures, and citation.
- Three horizontal gate tabs use simple borders and a subtle selected state.
  Definitions, claim boundaries, examples, and keyboard interaction are retained.
- Figure 1 appears directly below the framework. Figure 3 is visible in the
  additional figures section. On phones, the original vectors can be scrolled
  horizontally or opened at full resolution.
- Results use ordinary headings, horizontal bars, thin paired confidence
  intervals, compact explanations, and the original evidence links.

Removed the oversized acronym, burgundy and ivory palette, editorial serif
headings, dark framework band, two-column hero, decorative figure numbering,
large inequality illustration, dramatic headings, and magazine-style layouts.
The stylesheet was replaced rather than extended with corrective overrides.
The original paper figure typography is part of the unchanged SVG exports.

## Changed files

| File | Change |
| --- | --- |
| src/pages/index.astro | Centered hero and requested academic section order; original scientific result text and citation retained. |
| src/components/Gates.astro | Simple gate panels, unchanged definitions/interaction, and methodology figure directly beneath the framework. |
| src/components/EffectPlot.astro | Horizontal mean bars with the existing data, coordinate mapping, confidence intervals, and accessible labels. |
| src/styles/global.css | Complete readable white academic stylesheet and mobile layout. |
| public/favicon.svg | Neutral sans-serif favicon. |
| docs/REDESIGN_REVIEW.md | This review report and preview instructions. |

Local evidence is under qa/redesign/, an existing ignored QA directory. It
includes the browser harness, baseline file hashes, both screenshot passes,
machine-readable results, and public-site verification.

## Validation

- npm run check: zero errors, warnings, or hints.
- npm run build: successful static production build.
- git diff --check: clean.
- Final browser pass: **288 checks passed** at widths 1440, 1024, 768, and 390.
- **12 axe WCAG A/AA scans**, covering all three gate states at all four widths:
  zero violations. This is automated coverage plus screenshot inspection, not
  a formal accessibility certification.
- Click selection, selected ARIA state, roving focus, ArrowLeft/ArrowRight,
  Home/End, expandable details, exact clipboard copying, and denied-clipboard
  fallback all passed.
- With JavaScript disabled, all three gate evidence panels remain readable.
- No document horizontal overflow, failed browser requests, or runtime errors.
- Original abstract and BibTeX match exactly. All original result paragraphs,
  limits, captions, reproduction coverage, and external evidence/resource URLs
  are preserved.
- SHA-256 comparisons confirm all **16 protected files** are unchanged: data and
  seed records, both original SVGs, content provenance, Astro configuration,
  and the GitHub Pages workflow.
- The remote main branch remains at
  ebf8ebde95c0b96bf525cb08c76b3efe8860133e.
- Public HTML returned HTTP 200 and its before/after SHA-256 is identical:
  ff5844d5b1fce83af260b95ee64c03a13b8b53185198f43c3024e480bf32fbf3.

The initial browser pass passed 272 checks. Visual inspection then caught a
missing space between title spans on mobile; it was corrected and a title-text
regression check was added. The final pass adds scientific paragraph, citation,
and external-link preservation comparisons. Initial evidence remains in
qa/redesign/pass-1/; final evidence is in qa/redesign/final/.

## Screenshots inspected

The complete desktop and mobile captures were inspected, together with readable
section captures for the mobile page.

| Required view | File relative to the project |
| --- | --- |
| Desktop hero, 1440px | qa/redesign/final/desktop-hero.png |
| Full desktop page, 1440px | qa/redesign/final/desktop-full.png |
| Framework | qa/redesign/final/desktop-framework.png |
| Experimental results | qa/redesign/final/desktop-results.png |
| Mobile hero, 390px | qa/redesign/final/mobile-hero.png |
| Full mobile page, 390px | qa/redesign/final/mobile-full.png |

Additional captures include desktop predictive validity and the mobile
motivation, framework, abstract, DINOv2, DDPM, ImageNet-1K, positive control,
predictive validity, and citation sections. The final report is
qa/redesign/final/report.json.

## Local preview

The production preview is running at:

<http://127.0.0.1:4322/cohe-project-page/>

Open that address on the workspace machine. To restart with Node 22.12+:

    cd /home/poseidon/Desktop/Diana/cohe-project-page
    npm run preview -- --port 4322

This machine's default Node is older; select the isolated Node 22 environment:

    export PATH="/home/poseidon/Desktop/Diana/NeurIPS/cohe-website-evidence/tooling/node_modules/node/bin:/home/poseidon/Desktop/Diana/NeurIPS/cohe-website-evidence/tooling/node_modules/.bin:$PATH"

For further local edits:

    npm run check
    PAGES_URL=https://dayenajeong.github.io/cohe-project-page/ npm run build
    node qa/redesign/browser-qa.mjs another-review

The following flags record the original pre-publication review handoff, before
the user's subsequent approval.

    REDESIGN_IMPLEMENTED = TRUE
    ACADEMIC_STYLE_CONFIRMED = TRUE
    EDITORIAL_STYLE_REMOVED = TRUE
    SCIENTIFIC_RESULTS_UNCHANGED = TRUE
    DESKTOP_SCREENSHOTS_READY = TRUE
    MOBILE_SCREENSHOTS_READY = TRUE
    PUBLIC_SITE_MODIFIED = FALSE
    AWAITING_VISUAL_APPROVAL = TRUE
