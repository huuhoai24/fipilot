# Resume Upload Step Specification

## Source and placement

Directly observed on `https://www.hackerrank.com/mock-interviews/all-roles/recruiter` on 2026-08-19. In the AI Fluency clone this is the second setup step, between experience selection and Audio & Camera Settings.

Reference screenshots: `resume-upload-desktop.png`, `resume-upload-tablet.png`, `resume-upload-mobile.png`, `resume-upload-error-desktop.png`, `resume-upload-processing-desktop.png`, `resume-upload-success-desktop.png`, `resume-upload-success-tablet.png`, and `resume-upload-success-mobile.png`.

## Structure and text

- Title: `Upload Resume`
- Subtitle: `Add your resume so mock interviewer can reference it during conversation. (Optional)`
- Focusable drop zone with a document-upload outline icon.
- Main label: `Drag and drop your resume here`
- Detail: `Supported formats: PDF`
- Detail: `Max size: 5 MB`
- Footer actions: `Back` and `Continue`.

## Measurements and styles

The shared dialog is 640x650 desktop, 614.39x650 tablet, and 312x650 mobile. It uses the same backdrop, title, subtitle, body, and footer geometry as the experience step. The scrollable body is 592x534 desktop with 12px 20px 16px padding.

The desktop drop zone is x440/y263, 560x310. Its center stack contains a 16px/24px weight-700 main label (8px top margin), then two 12px/20px details. The upload control has pointer cursor; its hidden file input is `accept=.pdf`. Continue is enabled while the drop zone is empty because upload is optional.

At 768px the drop zone remains 560x310 inside the 614px dialog. At 390px it narrows to 224x310 at x83 while preserving height and centered content. The mobile footer remains visible at the bottom of the 650px dialog.

## Interaction contract

Back returns to experience selection. Continue advances to Audio & Camera Settings without requiring a file. Activating the drop zone opens the local PDF chooser.

## Directly observed upload states

### Invalid format

Uploading a non-PDF leaves the empty drop zone in place and shows a top-center toast: `Unsupported file format. Only pdf formats are allowed.` At the observed 1920px viewport the toast was x749.19/y76, 421.63x44, flex, padding 12px 16px 12px 8px, radius 4px, and background `rgb(235,235,243)`. It contains a 20px warning icon, 14px/20px message, and 20px close control. Continue remains enabled because resume is optional.

### Processing

After choosing a valid PDF, the drop zone replaces its empty prompt with `Uploading <filename>...`. The Continue action becomes a disabled `Uploading...` button with an inline spinner. Back remains visible. This is a transient asynchronous state.

### Success

The 560x310 desktop/tablet drop zone retains its position and becomes a `rgb(247,248,253)` panel with a 1px dashed `rgb(235,235,243)` border, 16px radius, 48px padding, centered column content. Text:

- `Your resume has been added` — 16px/24px, weight 700, 4px bottom margin.
- `You can update this resume in your profile anytime` — 14px/20px.

A selected-file card appears below at 462x74 desktop/tablet, padding 16px, gap 16px, border 1px `rgb(235,235,243)`, radius 16px. It contains a PDF outline icon, the real filename in a single ellipsized line, an eye icon, and a remove icon. The observed desktop card is x489/y417. Continue returns to its enabled green state.

At 390px the drop zone is x83/y271, 224x310. The success file card narrows to 126x74 at x132/y457; long filenames ellipsize. The desktop/tablet card remains 462x74.

The eye and remove controls were directly observed. Their downstream preview/remove states were not activated because the source controls were not focusable and normal pointer clicks remained blocked by the page's continuous animation; no additional confirmation screen is inferred.
