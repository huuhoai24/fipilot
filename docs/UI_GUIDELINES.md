# Fipilot UI Guidelines

Status: design direction for future frontend work. This document does not change the current implementation.

## 1. Product principles

Fipilot is an AI interview platform for candidates and recruiters. The interface should feel trustworthy, focused, and professional. It should help a person complete an interview task, understand system status, or make a hiring decision without visual distraction.

Use these priorities in order:

1. Make the current task and its next action obvious.
2. Make AI, upload, realtime, and evaluation states understandable.
3. Present candidate evidence and interview results accurately.
4. Preserve user confidence through clear language, accessibility, and predictable behavior.
5. Add visual character only when it does not compete with the task.

Clarity and task completion take priority over visual decoration.

### Product voice

- Use direct, specific product language.
- Name the object and the action: `Upload CV`, `Start text interview`, `Submit answer`, `Generate report`, `Invite candidate`.
- Explain system activity in plain language: `Analyzing your CV`, `Transcribing your answer`, `Generating interview report`.
- State what happened and what the user can do next.
- Do not describe AI as magic, human, infallible, or autonomous.
- Do not use generic marketing phrases such as `Unlock your potential`, `Elevate hiring`, `Seamless intelligence`, or `Revolutionize interviews`.
- Do not invent customer names, scores, candidate data, or performance claims.

## 2. Current frontend audit

This guideline is based on the frontend in `frontend/src`, its Tailwind configuration, global CSS, shared components, and route definitions.

### Current stack

- React 18 with TypeScript and Vite
- React Router
- Tailwind CSS 3 with CSS custom properties
- Lucide icons
- Zustand for UI state
- TanStack Query
- Satoshi with `"Segoe UI"` fallback

Keep this implementation context in mind when applying the guidelines. Do not introduce a second component or design system without a separate architecture decision.

### Current routes and primary jobs

| Route | Current job | Primary action |
| --- | --- | --- |
| `/login` | Enter the candidate workspace | `Continue with Google` |
| `/text-interview` | Upload a CV and configure a text interview | `Start text interview` |
| `/text-interview/:sessionId` | Answer the current question | `Submit answer` |
| `/text-interview/:sessionId/report` | Review the completed report | `Start another interview` or the next supported workflow action |
| `/speech-interview` | Upload a CV and configure a speech interview | `Start speech interview` |
| `/speech-interview/:sessionId` | Complete the realtime speech interview | The microphone or connection recovery action, depending on state |
| `/interview-history` | Resume a session or review a report | The action on the most relevant session, or `Start an interview` when empty |
| `/settings` | Change default interview preferences | `Save preferences` |

The current frontend is candidate-focused. Recruiter routes and role permissions are not yet represented in the inspected application. When recruiter workflows are added, make role context explicit and do not mix candidate practice actions with recruiter hiring actions in the same navigation or page.

### Existing components

- Layout: `AppLayout`, `Sidebar`, `UserMenu`, `ProtectedRoute`
- Primitives: `Button`, `Input`, `Select`, `Label`, `Textarea`, `Card`, `Badge`
- Interview: `InterviewExperienceIntro`
- Voice: `VoiceMicrophoneButton`, `VoiceStatusIndicator`, `VoiceWaveformPlaceholder`, `TranscriptPreview`

Extend these shared primitives before creating route-specific copies. A primitive must support its relevant loading, error, disabled, focus, and success states.

### Existing brand assets and patterns to preserve

- Product name: `Fipilot`
- Microphone mark used with the wordmark
- One mint or deep-green accent, adjusted for light and dark themes
- Satoshi as the product typeface
- Dark and light theme support
- Calm neutral surfaces with clear borders
- Real, interview-related photography on the login and interview introduction screens
- Direct candidate copy such as `Upload your latest CV`, `Submit answer`, and `Generating final report`
- Existing skip link, visible focus treatment, reduced-motion rule, semantic status messages, and live-region usage

The favicon currently uses an older indigo color while the application uses mint green. Future brand asset work should resolve that mismatch without changing the Fipilot identity.

### Existing patterns to standardize or retire

These are present in the current code but are not approved patterns for new work:

- `.glass-panel`, backdrop blur, and translucent floating navigation
- Decorative ambient grids, blurred accent orbs, and glow effects
- More than two radius values, currently ranging from 8px to 28px plus full circles
- Multiple shadow recipes across buttons, cards, menus, sidebars, and media
- Hover lift and hover translation on cards and navigation
- Oversized marketing-style headings inside task flows
- Wide-tracked uppercase labels repeated throughout product screens
- Cards nested inside cards or used for every section
- Long decorative transitions and automatic fade-ins

No screenshot files were found in the repository. The visual audit therefore uses the implemented React and CSS source. The external Pexels images referenced by the login and interview introduction screens are the only current product photography found.

## 3. Design direction

Use a restrained, product-first visual language:

- Design variance: low. Prefer stable alignment and predictable hierarchy.
- Motion intensity: low. Use motion for feedback and state change only.
- Visual density: medium. Keep enough information visible to complete the task without large empty zones.
- Theme: support the existing light and dark modes with hierarchy parity.
- Accent: use only the existing green brand family as the primary accent.

The product should resemble a dependable assessment workspace, not an AI marketing site.

## 4. Design tokens

Semantic tokens are the source of truth. Components must not introduce arbitrary colors, spacing, radii, or shadows.

### Color

Preserve the current green brand direction:

| Role | Dark theme | Light theme | Usage |
| --- | --- | --- | --- |
| Background | `#090d0c` | `#f1f2ec` | Page background |
| Surface | `#111714` | `#fbfcf7` | Primary content surface |
| Raised surface | `#19211d` | `#e7ebe3` | Inputs, selected rows, secondary grouping |
| Border | `#2a3530` | `#cdd4ca` | Low-emphasis separation |
| Primary text | `#f5f4eb` | `#111a16` | Headings and body |
| Muted text | `#a8b4ad` | `#526059` | Secondary copy |
| Faint text | `#6f7d76` | `#7c8982` | Nonessential metadata only |
| Accent | `#65e6bd` | `#08785f` | Primary action, active navigation, focus reinforcement |
| Accent hover | `#8af0ce` | `#075f4d` | Primary action hover |
| Focus | `#f3d675` | `#8d5d08` | Keyboard focus outline |

Rules:

- Green is the only brand and interactive accent.
- Theme variants of green count as one accent family.
- Success, warning, and danger colors are permitted only for their semantic meaning. They are not alternative accents.
- Do not use accent color for large text blocks, decorative backgrounds, or every icon.
- Do not hard-code `#07110d` for text on accent. Create and use an `on-accent` semantic token.
- `text-faint` in the current light theme is about 3.24:1 against the page background. Do not use it for required labels, instructions, or small meaningful text.
- The current default borders are below 3:1 against adjacent surfaces. Interactive controls, selected boundaries, and focus states need a stronger boundary token. A suitable starting point is `#6f7d76` in dark mode and `#7c8982` in light mode, verified against the actual adjacent surface.
- Body text must meet WCAG AA, with 4.5:1 minimum contrast. Large text needs at least 3:1.
- Controls, focus indicators, and meaningful graphics need at least 3:1 against adjacent colors.

### Gradient rule

The existing product uses ambient radial gradients and photo scrims. Do not extend the decorative gradient system.

The only approved gradient is a functional image scrim when text must sit over photography. It must improve legibility and meet contrast requirements. Do not use:

- Gradient text
- Gradient buttons
- Mesh or aurora backgrounds
- Accent glow gradients
- Decorative gradients in cards or reports

The current ambient body gradient is a legacy treatment. New screens should use solid semantic backgrounds.

### Typography hierarchy

Use Satoshi for display and body text. Use `"Segoe UI"` and `sans-serif` as fallbacks. Use the mono stack only for session IDs, timers, and technical values where fixed-width alignment helps.

| Style | Desktop | Mobile | Weight | Usage |
| --- | --- | --- | --- | --- |
| Display | 48/56 | 40/48 | 600 | Login or interview introduction only |
| Page title | 40/48 | 32/40 | 600 | One per screen |
| Section title | 24/32 | 24/32 | 600 | Major content section |
| Subsection title | 18/24 | 18/24 | 600 | Group within a section |
| Body | 16/24 | 16/24 | 400 | Default reading text |
| Compact body | 14/24 | 14/24 | 400 or 500 | Tables, history, helper text |
| Label | 14/24 | 14/24 | 600 | Form and control labels |
| Metadata | 12/16 | 12/16 | 500 | Timestamps and IDs |

Typography rules:

- Keep page titles to one or two lines.
- Use sentence case for headings, labels, navigation, buttons, and badges.
- Use negative letter spacing only for display and page titles, no tighter than `-0.03em`.
- Avoid uppercase wide-tracked eyebrows. Use a normal heading or visible field label.
- Do not use type size alone to create hierarchy. Combine size, weight, alignment, and spacing.
- Keep prose to about 65 characters per line.
- Use tabular numerals for timers, scores, and aligned numeric data.
- Never shrink required text below 12px.

### Spacing scale

Use an 8px base system:

| Token | Value | Typical use |
| --- | --- | --- |
| `space-1` | 8px | Icon-to-label gap, tight stack |
| `space-2` | 16px | Field spacing, control groups |
| `space-3` | 24px | Card padding, grid gap |
| `space-4` | 32px | Section padding, page header gap |
| `space-5` | 40px | Desktop page gutter |
| `space-6` | 48px | Major section separation |
| `space-8` | 64px | Large page transition |
| `space-10` | 80px | Maximum intentional section separation |

Rules:

- Use only multiples of 8px for layout spacing, gaps, padding, and margins.
- Do not use 12px, 20px, 28px, or one-off arbitrary values.
- Do not use spacing to simulate an empty hero. Product screens should begin near the top of the content region.
- Prefer `gap` on parent layouts over margins on individual children.

### Borders, radii, and shadow

Use 1px solid semantic borders. Use borders and spacing for hierarchy before elevation.

There are exactly two approved radius values:

1. `8px`: buttons, inputs, alerts, menus, cards, dialogs, images, and content containers.
2. `9999px`: intrinsically circular or pill-shaped controls only, including avatars, the microphone control, radio controls, and short status badges.

Do not use 12px, 16px, 20px, 24px, or 28px radii. Do not apply the pill radius to navigation items, form fields, panels, or long labels.

There is exactly one approved shadow level:

```css
--shadow-overlay: 0 8px 24px rgb(3 8 6 / 18%);
```

Use it only when elevation communicates layering, such as a menu, popover, dialog, or sticky element over scrolling content. Cards, buttons, sidebars, and static sections should not have shadows. Never combine the shadow with a glow.

## 5. Layout and alignment

### Content frame

- Use one app-shell content frame with a maximum width of 1280px.
- Align page title, main content, and page-level actions to the same left and right edges.
- Use 40px desktop gutters at 1440px, 24px gutters at 1024px and 768px, and 16px gutters at 390px.
- Use narrower reading and form widths inside the frame when the task benefits, but keep them aligned to the frame grid.
- Do not center isolated forms without a layout reason. Settings and setup forms should align with the page heading.
- Avoid excessive empty space. A completed task area may breathe, but should not require large blank panels.

### Page structure

Every screen should use this order where applicable:

1. App navigation and role context
2. Page title and concise description
3. One obvious primary action
4. Task content
5. Supporting information and secondary actions

Use a stable 12-column desktop grid or simple CSS Grid layouts. Avoid percentage calculations and arbitrary fixed widths.

### Candidate and recruiter separation

- Candidate navigation should focus on practice, active sessions, reports, history, and preferences.
- Recruiter navigation should focus on jobs, interview plans, candidates, invitations, reports, and team settings.
- Show the active workspace or role in the shell when both roles exist.
- Do not expose recruiter hiring recommendations to candidates unless the product explicitly supports that policy.
- Keep candidate evidence, AI interpretation, and human decisions visually distinct in recruiter reports.

## 6. Primary action rule

Each screen must have one obvious primary action.

- Use one filled accent button for the primary action.
- The primary action label must name the outcome.
- Secondary actions may use outlined or text styles.
- Destructive actions must not share the accent treatment.
- If the primary action is unavailable, keep it in place, disable it, and explain what is required.
- A realtime screen may use a large functional control, such as the microphone, as its primary action instead of a standard button.
- Do not present several equally prominent actions.

Examples:

| Context | Primary | Secondary |
| --- | --- | --- |
| Login | `Continue with Google` | None |
| CV setup | `Upload and analyze` | `Choose another file` |
| Interview setup | `Start text interview` or `Start speech interview` | `Edit preferences` |
| Text question | `Submit answer` | `Save draft` only if supported |
| Voice connection error | `Reconnect` | `Back to setup` |
| Completed interview | `View report` | `Back to history` |
| Empty history | `Start an interview` | None |
| Settings | `Save preferences` | `Reset defaults` only if supported |
| Recruiter invitation | `Invite candidate` | `Save draft` |
| Recruiter report | `Record hiring decision` | `Download report` |

## 7. Buttons

### Hierarchy

1. Primary: filled accent background with `on-accent` text. One per screen or clearly bounded task region.
2. Secondary: opaque surface with a strong border and primary text.
3. Tertiary: text or ghost treatment for low-priority actions.
4. Danger: danger text and border, reserved for destructive actions.

### Rules

- Standard height: 40px. Large primary action: 48px.
- Minimum touch target: 44 by 44px, using padding when the visual control is smaller.
- Use 16px horizontal padding for standard buttons and 24px for large buttons.
- Keep labels on one line.
- Use an icon only when it clarifies the action.
- Icon-only buttons require an accessible name and a visible tooltip on hover and keyboard focus.
- Do not animate buttons vertically on hover.
- Use a simple color or border transition of 150ms or less.
- The active state may darken the fill or reduce opacity slightly. Do not scale the control.
- A loading button retains its width, shows progress, and uses a present-participle label such as `Uploading` or `Saving`.
- Disabled buttons must remain readable. Do not rely on low opacity alone.

## 8. Forms

### Field structure

Every field must include:

1. A visible label above the control
2. The control
3. Optional helper text
4. Inline validation or error text when needed

Rules:

- Connect every label with `htmlFor` and a unique input `id`.
- Never use a placeholder as the only label.
- Use placeholders only for example input, not instructions.
- Connect helper and error text with `aria-describedby`.
- Set `aria-invalid="true"` on invalid controls.
- Place validation next to the field that needs correction.
- Validate after blur or submit. Do not show errors while the user is still entering a valid partial value.
- Preserve entered values after an error.
- Put units in labels or adjacent text: `Duration (minutes)`.
- Provide useful bounds in copy and markup: `5 to 180 minutes`.
- Use native input types and autocomplete values where possible.
- File uploads must show accepted formats, size limit, selected filename, file size, upload progress, success, and recovery from failure.
- Do not disable copy, paste, browser password management, or keyboard shortcuts.

### Keyboard behavior

- Tab order must follow the visual order.
- All controls must work without a pointer.
- Enter submits a focused single-step form when safe.
- Textareas preserve Enter for line breaks. Use the visible submit button or a documented modifier shortcut.
- Escape closes menus, popovers, and dialogs and returns focus to the trigger.
- Dialogs trap focus and restore it on close.
- Do not create positive `tabindex` values.
- Sticky content must not cover the focused element.

### Validation copy

Write precise, recoverable messages:

- `Choose a PDF or DOCX file.`
- `The CV must be 10 MB or smaller.`
- `Enter a duration from 5 to 180 minutes.`
- `Your answer could not be submitted. Check your connection and try again.`

Avoid `Invalid input`, `Something went wrong`, or error codes without explanation.

## 9. Cards and content grouping

Cards are for distinct objects or independent tasks, not general decoration.

Use a card for:

- A single interview session that is independently actionable
- A candidate summary
- A report module with a distinct job
- A dialog or popover
- A bounded upload or configuration task

Do not use a card for:

- Every page section
- A page title
- A single paragraph
- A group that can be separated by spacing, a heading, or one divider
- Every metric in a report
- Rows in a dense desktop list when a table or aligned list is clearer

Card rules:

- Use an opaque surface, a 1px border, 8px radius, and no shadow.
- Use 24px padding on desktop and 16px on mobile.
- Do not nest cards. Use a divider or raised surface for inner grouping.
- Do not lift, tilt, glow, or translate cards on hover.
- Make the full card clickable only if it has one destination. Otherwise keep explicit actions.
- History should use an aligned list or table at wider widths and stacked rows at narrow widths, not a gallery of floating cards.
- Report metrics should share one aligned group. Do not put each score in a separate rounded tile.

## 10. Data, reports, and AI output

- Label AI-generated content as generated or inferred when users could mistake it for verified fact.
- Separate source evidence from AI interpretation.
- Preserve the candidate's original answer and CV evidence when showing evaluation.
- Show score scale and meaning. A number such as `7.4/10` needs a visible label and supporting explanation.
- Do not use color as the only indicator of score, recommendation, or status.
- Avoid decorative progress bars. Use progress bars only for real completion or elapsed progress.
- Hiring recommendations require clear status text and should not look like unquestionable system truth.
- Give recruiters a place for the human decision when that workflow exists.
- Do not expose model confidence without explaining what it refers to.
- Use tables for comparison and scanning. On small screens, preserve row labels and reading order rather than forcing horizontal scrolling where possible.

## 11. Loading, empty, error, disabled, and success states

Every new screen and component must define these states before implementation.

### Loading

- Preserve the final layout to reduce layout shift.
- Use skeletons for lists, reports, and structured content.
- Use inline progress in buttons for user-triggered actions.
- A spinner is acceptable for a short, indeterminate control state or realtime connection, but it must include accessible status text.
- Tell the user what is happening: `Analyzing your CV`, not `Loading`.
- For long operations, explain that the user may wait and avoid suggesting false precision.

### Empty

- State what is empty.
- Explain why it matters or how it becomes populated.
- Provide one primary action.
- Keep the state compact. Do not place it inside a huge decorative panel.

Example: `No interview sessions yet. Upload your CV to start a text or speech interview.` Primary action: `Start an interview`.

### Error

- Put field errors beside fields and page errors near the affected content.
- Preserve context and user input.
- Explain what failed in plain language.
- Offer the most useful recovery action: `Try again`, `Reconnect`, `Choose another file`, or `Back to setup`.
- Use a toast only for transient events that do not need later reference.
- Move focus to a page-level error summary after failed submit when several fields are invalid.

### Disabled

- Keep disabled controls visible and readable.
- Explain the prerequisite in nearby helper text.
- Do not use `not-allowed` cursor or opacity as the only explanation.
- For permission restrictions, state which role can perform the action.

### Success

- Confirm the completed action next to its source.
- Use `role="status"` or an appropriate live region for asynchronous confirmation.
- State what changed and what happens next.
- Keep success visible long enough to read.
- Do not use confetti, celebratory animation, or a full-screen takeover for routine actions.

## 12. Responsive behavior

The interface must be designed and checked at 1440px, 1024px, 768px, and 390px. These are test widths, not device labels.

### 1440px

- Expanded sidebar may be 256px wide.
- Main content uses the 1280px frame within the available area.
- Use 40px page gutters.
- Multi-column setup and report layouts are allowed when columns remain readable.
- Keep page title and primary action on the same row only when neither is compressed.

### 1024px

- Default to a compact 72px sidebar or a drawer. Do not leave a 256px sidebar beside a narrow task column.
- Use 24px page gutters.
- Reduce complex grids to two columns.
- Move supporting summaries below or beside the task only if the main task keeps priority.
- Desktop navigation must remain on one line.

### 768px

- Do not show the persistent desktop sidebar.
- Use a compact app header with a menu or another accessible mobile navigation pattern.
- Use 24px page gutters.
- Collapse all main content to one column.
- Place the primary action after the fields it submits.
- Convert tables and history rows to labeled stacked rows.
- Remove sticky side panels that reduce usable width.

### 390px

- Use 16px page gutters.
- Use one column only.
- Primary buttons should usually be full width.
- Keep touch targets at least 44px.
- Allow long filenames, candidate names, session IDs, and status text to wrap or truncate with an accessible full value.
- Do not use horizontal page scrolling.
- Keep form controls at least 16px text to avoid mobile browser zoom.
- Place secondary actions below the primary action when they do not fit.
- The voice screen must keep the current question, system status, and microphone control visible without oversized decorative spacing.

### Responsive checks

At every width verify:

- No content is hidden behind sticky navigation.
- No action label wraps unexpectedly.
- Focus order matches reading order.
- Status and error messages remain next to their source.
- Text remains readable without zoom.
- Zoom to 200% does not cause loss of content or functionality.

## 13. Accessibility requirements

- Target WCAG 2.2 AA.
- Use semantic landmarks: `header`, `nav`, `main`, `aside`, and `footer` where appropriate.
- Keep one `h1` per screen and do not skip heading levels.
- Preserve the existing skip link and ensure it becomes visibly focused.
- Provide a visible 2px focus outline with at least 3:1 contrast and 2px offset.
- Do not remove focus outlines in component styles.
- Provide accessible names for every interactive control.
- Mark decorative icons `aria-hidden="true"`.
- Never communicate status by color or icon alone.
- Use `aria-live="polite"` for nonurgent async updates and `role="alert"` for blocking errors.
- Realtime voice status must be understandable without animation or audio.
- Provide text alternatives for meaningful images.
- Do not place essential copy over an image unless the scrim keeps it readable in both themes and at every crop.
- Respect `prefers-reduced-motion`.
- Support browser zoom and text resizing.
- Test with keyboard only and at least one screen reader before release.

## 14. Icons, imagery, and motion

### Icons

- Continue using the existing Lucide family until an explicit icon-system migration is approved.
- Use icons for actions, navigation, file types, state, and warnings.
- Do not add an icon when the text is already clear and the icon adds no meaning.
- Do not use `Sparkles`, abstract AI brains, robots, magic wands, or decorative status dots as default AI decoration.
- Keep icon size consistent: 16px in compact controls, 20px in standard controls, and 24px for major state illustrations.

### Imagery

- Use real product-relevant photography only on login, onboarding, or explanation surfaces where it supports trust.
- Do not use generic office photos inside active interview, history, settings, or report workflows.
- Candidate and recruiter data should use real application content, not invented promotional examples.
- Avoid text overlays on images. If required, use the approved functional scrim.

### Motion

- Default transition duration: 150ms.
- Animate color, border color, opacity, or transform only when it communicates feedback or state change.
- Do not use route entrance animation, ambient floating elements, card hover lifts, parallax, or scroll-triggered reveals.
- Continuous motion is allowed only for a real ongoing state such as voice activity, recording, connecting, or progress.
- A reduced-motion user must receive the same information in a static form.
- Do not animate layout width, height, top, or left.

## 15. Prohibited AI-generated UI patterns

Do not introduce:

- Glassmorphism, translucent cards, or backdrop blur
- Purple AI palettes, neon glow, or multiple accent colors
- Gradient text, gradient buttons, mesh backgrounds, or aurora effects
- A rounded card around every section
- Nested cards and bento grids used as a default product layout
- Three equal marketing feature cards inside the application
- More than the two approved radius values
- More than the one approved shadow level
- Pills for every label, navigation item, filter, and metadata value
- Oversized headlines that push the task below the fold
- Uppercase wide-tracked eyebrow text above every heading
- Decorative icons, sparkles, robots, magic wands, or brain symbols without functional meaning
- Decorative ambient grids, blurred orbs, crosshairs, or fake system diagrams
- Fake dashboards, fake interview scores, fake candidate names, or fake live activity
- Generic copy such as `AI-powered insights`, `Unlock potential`, `Smarter hiring`, or `Your journey starts here`
- Hover lift, tilt, magnetic buttons, animated borders, shimmer on static content, or unnecessary pulsing
- Excessive empty space intended to make ordinary product content feel premium
- Progress bars that do not represent real progress
- Color-only status indicators
- Icon-only actions without an accessible label and tooltip
- Modals when an inline disclosure or page section is clearer
- Placeholder-only form labels
- Disabled controls with no explanation
- Toasts for errors that require user action
- Default library styling that ignores Fipilot tokens and branding

## 16. Review checklist

Before approving a new or changed screen, confirm:

- [ ] The screen has one obvious primary action.
- [ ] The action label names a real Fipilot outcome.
- [ ] The layout aligns to the shared 1280px frame.
- [ ] All spacing uses the 8px scale.
- [ ] Only 8px and full radii are used.
- [ ] Only the approved overlay shadow is used, and only for a layered element.
- [ ] Green is the only primary accent.
- [ ] No glassmorphism or decorative gradient was introduced.
- [ ] Cards represent real objects or tasks and are not used for every section.
- [ ] Loading, empty, error, disabled, and success states are specified.
- [ ] Every form control has a visible connected label.
- [ ] Validation is specific, inline, and accessible.
- [ ] Keyboard navigation and focus restoration work.
- [ ] Contrast meets WCAG 2.2 AA.
- [ ] The screen works at 1440px, 1024px, 768px, and 390px.
- [ ] Reduced motion preserves all information.
- [ ] Icons have functional meaning.
- [ ] Copy uses real product terms and no invented claims or data.
- [ ] Candidate evidence, AI interpretation, and human decisions are clearly separated.
- [ ] The Fipilot name, microphone mark, mint-green accent, and Satoshi type remain recognizable.
