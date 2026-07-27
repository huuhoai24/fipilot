# Resume Upload and Interview Start UI Audit

Status: source-based audit only. No implementation changes are included.

## Scope and evidence

This audit covers the candidate resume upload and interview-start flow on:

- `/text-interview`
- `/speech-interview`
- `/text-interview/:sessionId` during initial session loading

Both setup routes render `TextInterviewPage` with a different `mode` prop:

- `/text-interview` renders `<TextInterviewPage mode="text" />`
- `/speech-interview` renders `<TextInterviewPage mode="voice" />`

Primary source files:

- `frontend/src/App.tsx`
- `frontend/src/pages/TextInterviewPage.tsx`
- `frontend/src/components/interview/InterviewExperienceIntro.tsx`
- `frontend/src/components/ui/Button.tsx`
- `frontend/src/components/ui/Input.tsx`
- `frontend/src/components/ui/Card.tsx`
- `frontend/src/components/ui/Badge.tsx`
- `frontend/src/components/layout/AppLayout.tsx`
- `frontend/src/components/layout/Sidebar.tsx`
- `frontend/src/index.css`
- `frontend/tailwind.config.js`

No UI screenshot files were found in the repository. The findings are based on the rendered structure and styles defined by the React and CSS source.

### Executive finding

The flow contains the correct functional sequence and several useful states, but the main task is visually delayed and over-framed. A candidate must pass a large promotional introduction, a second page introduction, an upload card, a full extracted-profile card, a setup card, and a duplicate sticky summary before starting an interview.

The smallest meaningful redesign is not a new flow. It is a tighter presentation of the existing flow:

```text
Current
Route intro -> scroll CTA -> setup intro -> upload card -> full profile card
-> setup card + duplicate sticky summary -> Start

Recommended
Compact page header -> Step 1: upload and review -> Step 2: configure
-> Start text interview / Start speech interview
```

Keep the routes, API calls, file validation, preference defaults, candidate profile model, and navigation behavior. Remove the promotional detour, progressively reveal the two steps, and improve state and form semantics.

## 1. Current user journey

### Route entry

The route map in `frontend/src/App.tsx` sends both new interview modes into the same setup component:

| Route | Component | Mode |
| --- | --- | --- |
| `/text-interview` | `TextInterviewPage` | `text` |
| `/speech-interview` | `TextInterviewPage` | `voice` |
| `/text-interview/:sessionId` | `TextInterviewPage` | `text` |
| `/speech-interview/:sessionId` | `SpeechInterviewPage` | Active voice session |

The shared setup is a good architectural choice. Text and speech setup remain consistent while the mode-specific copy and destination change.

### Journey sequence

1. The candidate opens `/text-interview` or `/speech-interview`.
2. `InterviewExperienceIntro` renders a large split introduction with:
   - Mode label
   - Large `Text Interview` or `Speech Interview` heading
   - Description
   - `Set up my interview` button
   - Three preparation rows
   - Pexels photography
3. The button uses `scrollIntoView` to move to `#interview-setup`.
4. A second introduction appears with `Build your interview.` and a short explanation.
5. The `Candidate Profile` card asks for a PDF or DOCX file up to 10 MB.
6. `selectResume` validates extension, MIME type, empty file, and size.
7. The candidate chooses a file.
8. A selected-file row displays the filename and size.
9. The candidate presses `Upload and Analyze`.
10. `uploadSelectedResume` sends the file through `api.uploadResume`.
11. During upload:
    - The button shows a spinner and `Analyzing...`
    - The file input and setup controls are disabled
    - A live region says `Uploading and extracting the candidate profile...`
12. On failure, an inline alert displays the API or validation message.
13. On success:
    - The button changes to `Analyzed`
    - A live status confirms that the candidate profile is ready
    - `CandidateProfilePreview` renders name, role, experience, skills, projects, work experience, education, evidence, and extraction confidence
14. The candidate configures:
    - Language
    - Experience level
    - Interview style
    - Duration
    - Question count
    - Objective
15. A sticky `Session Setup` panel duplicates the selected mode, candidate, language, level, question count, and duration.
16. The candidate presses `Start`.
17. `startInterview` calls `api.startV2Interview`.
18. On success:
    - Text navigates to `/text-interview/:sessionId`
    - Speech navigates to `/speech-interview/:sessionId`
19. On failure, a page-level error is rendered above the setup section.

### Current strengths

- Text and speech reuse the same setup logic.
- File type and size validation happen before upload.
- The upload control names accepted formats and size.
- The selected filename and size are visible.
- Upload status uses `aria-live="polite"`.
- Upload errors use `role="alert"`.
- The candidate sees extracted information before the interview starts.
- Existing preferences prefill the configuration.
- The start action is disabled until a backend candidate ID exists.
- The final route is mode-correct.

## 2. Visual hierarchy problems

### High priority

#### The primary task starts too late

`InterviewExperienceIntro` uses a minimum 520px content height plus a minimum 380px image, large padding, a large heading, preparation rows, and an image. The candidate then reaches another heading, `Build your interview.`, before seeing the file input.

Evidence:

- `InterviewExperienceIntro.tsx`, lines 62-103
- `TextInterviewPage.tsx`, lines 418-428

Impact:

- The upload action is below the fold at common laptop and mobile heights.
- Returning candidates repeatedly see onboarding content they already understand.
- The page feels like a landing page instead of a focused product workflow.

#### There are several competing starts

The route presents:

1. `Set up my interview`
2. `Build your interview.`
3. Step `1`
4. Step `2`
5. `Start`

The user has to interpret which action actually begins the interview. The first CTA only scrolls. The final CTA has the least specific label.

Impact:

- The visual emphasis is strongest on a navigation action rather than the final outcome.
- The flow has multiple apparent primary actions.

#### The extracted profile becomes the dominant section

`CandidateProfilePreview` can render every project, experience, education item, skill, technology, and evidence item. It sits between file upload and interview settings.

Evidence:

- `TextInterviewPage.tsx`, lines 71-220
- `TextInterviewPage.tsx`, lines 499-501

Impact:

- Long resumes push the interview configuration far below the success state.
- The user is told to review the result but is not given a way to correct it.
- Secondary extracted detail has more visual weight than the primary task.

#### The setup card and sticky summary repeat the same information

The `Interview Setup` form and `Session Setup` panel display the same settings at the same time.

Evidence:

- `TextInterviewPage.tsx`, lines 503-592
- `TextInterviewPage.tsx`, lines 594-632

Impact:

- The layout appears more complex without adding decision support.
- On medium widths, the summary competes with the form for space.
- Repetition makes the page feel template-driven.

### Medium priority

#### Cards create hierarchy through decoration, not task structure

The introduction, file upload, full profile preview, configuration form, and summary all use bordered rounded surfaces. The generic `Card` also adds a shadow.

Impact:

- Every region asks for equal attention.
- The meaningful transition from upload to configuration is not stronger than ordinary grouping.
- The page reads as a stack of containers rather than a guided sequence.

#### Step numbers are visually detached

The `1` and `2` indicators are spans placed at the far right of `CardHeader`. They are not part of an ordered list or the heading text.

Impact:

- The relationship between the number and task is weaker on wide cards.
- The numbers add decoration but little navigation value.
- Assistive technology receives no step structure from them.

## 3. Alignment and spacing inconsistencies

### Competing content frames

- `AppLayout` uses `max-w-[1500px]`.
- `InterviewExperienceIntro` fills that frame.
- Its internal text uses `max-w-3xl` and `max-w-2xl`.
- The setup introduction uses `max-w-4xl`.
- The configuration form switches to a content column plus a fixed `360px` sidebar.

This creates several left and right edges within one task.

### Sidebar breakpoint compresses the flow

`Sidebar` becomes visible at `md`, while `AppLayout` applies `md:ml-[18.5rem]` when expanded. At 768px, the setup is placed beside a 260px sidebar instead of using the mobile header.

Evidence:

- `Sidebar.tsx`, line 36
- `AppLayout.tsx`, lines 49 and 102-106

Impact:

- The content column can become about 470px wide at the 768px breakpoint.
- At 1024px, the `lg` two-column setup also tries to reserve 360px for the sticky summary.
- The form can become unnecessarily narrow while still using a desktop layout.

### Spacing does not follow one scale

The flow mixes:

- `gap-3` or 12px
- `gap-5` and `space-y-5` or 20px
- `p-5` or 20px
- `p-7` or 28px
- `px-7` or 28px
- `py-3.5` or 14px
- `md:pt-14` or 56px

The project guideline defines an 8px system, but this flow uses many intermediate values.

### Radius and shadow usage is inconsistent

Within this flow and its shared shell, the UI uses:

- `rounded-lg`
- `rounded-xl`
- `rounded-2xl`
- `rounded-card` at 20px
- `rounded-[24px]`
- `rounded-[28px]`
- `rounded-full`
- `shadow-lg`
- `shadow-2xl`
- Multiple arbitrary shadow values

Impact:

- Large, soft shapes make ordinary form sections feel promotional.
- The page lacks a stable distinction between controls, content sections, and overlays.

### Action alignment changes by section

- The introduction CTA is left-aligned.
- The upload action is aligned to the right of the file input on desktop.
- The final start action is bottom-right.
- At narrow widths, the upload action becomes full width but `Start` does not explicitly do so.

The user has to scan different areas for the next action at each step.

### Candidate profile subsections are not internally consistent

Projects, experience, and education include accent icons. Skills and skill evidence do not. Some groups use divided rows, some use a list, and others use stacked paragraphs.

Impact:

- Similar data receives different presentation.
- Icons create uneven alignment without improving comprehension.

## 4. Typography problems

### The introduction heading is oversized for a task screen

`InterviewExperienceIntro` uses `clamp(3rem, 6vw, 5.6rem)`, or roughly 48px to 90px. The following `Build your interview.` heading is 36px to 48px, while card titles are 16px.

Impact:

- The largest type describes the route mode, which is already known from navigation.
- The actual upload and configuration tasks look subordinate.
- The hierarchy jumps abruptly from marketing display type to compact form text.

### Required helper text is too small and too faint

Accepted file formats, file guidance, setup guidance, filename size, and profile metadata frequently use `text-xs text-text-faint`.

The current light `text-faint` token is `#7c8982`, approximately 3.24:1 against the page background. It does not meet 4.5:1 for small required text.

Impact:

- Important upload constraints can be difficult to read.
- Users with low vision may miss the information needed to avoid an error.

### Case style is inconsistent

Examples:

- `Candidate Profile`
- `Extracted Candidate Profile`
- `Interview Setup`
- `Session Setup`
- `Experience Level`
- `Question Count`
- `Skill Evidence`
- `Upload and Analyze`

These use title case, while most product instructions use sentence case. The session summary also forces the language code to uppercase while nearby values use ordinary text or capitalization.

### Repeated uppercase micro-headings add visual noise

Candidate profile sections use 12px uppercase headings for skills, projects, experience, education, and evidence.

Impact:

- The profile resembles a generic dashboard inspection panel.
- Small uppercase text has reduced word shape and is harder to scan.

### Some labels are vague or misleading

- `Candidate Profile` is the upload step, not yet a profile.
- `Start` does not state whether it starts a text or speech interview.
- `Objective` does not explain what to enter or whether it is optional.
- `Duration` does not expose the unit in the label.
- `Review before starting` promises review, but the extracted data is not editable.
- `Analyzed` describes a completed backend operation but not the usable result.

Better labels include:

- `Upload your CV`
- `Upload and analyze`
- `Start text interview`
- `Start speech interview`
- `Duration (minutes)`
- `Interview objective (optional)`
- `CV analyzed`

## 5. Accessibility problems

### Form labels are not programmatically connected

Only `Resume file` passes `htmlFor` and has a matching `id`. The labels for language, experience level, interview style, duration, question count, and objective do not.

Evidence:

- `TextInterviewPage.tsx`, lines 439-448
- `TextInterviewPage.tsx`, lines 514-579
- `Input.tsx`, `Label`

Impact:

- Clicking most labels does not focus the field.
- Screen readers cannot reliably associate label text with controls.

### The setup form lacks group semantics

The settings are visually grouped but not placed in a `fieldset` with a `legend`, and the two visual steps are not an ordered structure.

Impact:

- The relationship among the setup controls is less clear to assistive technology.
- The visual step numbers do not communicate sequence semantically.

### Page-level errors are not announced

The shared `error` block at `TextInterviewPage.tsx`, lines 411-415, is a styled `div` without `role="alert"` or a live region. It is also rendered above the setup content, far from the `Start` button that may have caused it.

Impact:

- A failed start may not be announced.
- Keyboard and screen-reader users may not know where the new message appeared.

### Session loading shows the wrong interface

When `/text-interview/:sessionId` loads, `state` is initially null. The component starts the fetch in an effect, but the null-state render still displays `InterviewExperienceIntro` and the complete new-interview setup.

Evidence:

- `TextInterviewPage.tsx`, lines 262-282
- `TextInterviewPage.tsx`, lines 389-418

Impact:

- Users may see and focus controls for starting a new interview while an existing one is loading.
- The page lacks a correct loading announcement and stable focus target.

### JavaScript smooth scrolling ignores reduced-motion preference

`InterviewExperienceIntro` always calls `scrollIntoView({ behavior: 'smooth' })`.

The global CSS reduces CSS animation and transition duration, but it does not alter this JavaScript behavior.

Impact:

- Users who request reduced motion still receive an animated viewport movement.

### Disabled state is not fully explained at the action

The `Start` button is disabled until `candidateId` exists. The sticky summary says `CV required`, but there is no message directly connected to the disabled action.

Impact:

- A user reaching the button may not understand why it cannot be used.
- Disabled controls are not focusable, so they cannot expose an explanation through focus.

### Starting state is not clearly announced

During `startInterview`, the button changes its icon to a spinner but keeps the label `Start`. The form has no `aria-busy`, and there is no live status such as `Starting text interview`.

Impact:

- The state change is primarily visual.
- The user receives no clear confirmation that the request is in progress.

### Select affordance is reduced

The shared `Select` applies `appearance-none` but does not render a replacement chevron.

Impact:

- The control can look like a text input.
- Users may have less visual indication that a choice list is available.

### Review is not actionable

The success message says `Review it before starting the interview`, but `CandidateProfilePreview` has no edit, correction, replace, or confirmation control.

Impact:

- Users can identify extraction mistakes but cannot resolve them within the promised workflow.
- This is both a trust and usability issue for AI-derived data.

### Accessibility strengths to retain

- Native file input
- Native select, number input, and textarea elements
- Connected label and description for the resume input
- Live upload status
- Alert role for upload errors
- Text labels inside buttons
- Meaningful image alt text
- Global visible focus style
- Existing CSS reduced-motion fallback

## 6. Missing loading, error, empty, and success states

| Area | Current coverage | Missing or incomplete state |
| --- | --- | --- |
| Initial route | Empty status says no profile is loaded | The setup should have a clear progressive state instead of showing all later content as an inactive full form |
| Existing session load | Fetch logic exists | Dedicated loading UI is missing; the new-interview flow appears while loading |
| File selection | Valid file shows name and size | No explicit `Choose another file` or clear reset action |
| Client validation | PDF, DOCX, MIME, zero-byte, and 10 MB errors exist | Error should be connected to the file input with `aria-describedby` and `aria-invalid` |
| Upload loading | Spinner, changing label, and live status exist | No longer-operation guidance, cancel option, or structured extraction progress |
| Upload error | Inline alert exists and implicit retry is possible | No explicit `Try again` or `Choose another file` action; generic backend text may not be recoverable |
| Upload success | Success text and full profile preview exist | No compact summary, replace-CV action, correction path, or explanation of confidence |
| Partial extraction | Empty profile sections are silently omitted | No warning for missing name, low confidence, unreadable sections, or partial extraction |
| Configuration empty | Preference defaults populate fields | `Objective` has no optional marker, helper text, or example; a blank objective has no explicit meaning |
| Configuration validation | Native `min` and `max` exist for duration; `min` exists for question count | No inline validation messages, error summary, question-count maximum, or invalid-value state |
| Disabled start | Button is disabled without a candidate ID | No adjacent explanation connected to the action |
| Start loading | Spinner replaces the arrow | Label remains `Start`; no `aria-busy`, live status, or duplicate-submit explanation |
| Start error | Page-level message exists | It is not announced and appears far from the form action |
| Start success | Navigation to the correct active route occurs | No additional success screen is needed if navigation is immediate and reliable |
| Offline or timeout | Generic catch path exists | No tailored connection message, retained retry action, or timeout guidance |

### Highest-risk missing states

1. Existing-session loading
2. Partial or low-confidence CV extraction
3. Replace or correct an analyzed CV
4. Start-interview loading and error announcement
5. Inline field validation

## 7. Components that can be reused

### `TextInterviewPage`

Reuse:

- Shared text and speech setup
- Route-mode behavior
- Preference loading
- File selection state
- Upload API call
- Start API call
- Mode-correct navigation

Do not split text and speech setup into separate pages unless their required fields genuinely diverge.

### File validation helpers

Reuse:

- `validateResumeFile`
- `formatFileSize`
- Accepted extension and MIME constants

These are clear, product-specific rules and should remain a single source of truth.

### `CandidateProfilePreview` data mapping

Reuse:

- Education normalization
- Conditional section rendering
- Skill evidence filtering
- Candidate profile field coverage

The data transformation is useful. The presentation should be reduced and the function should be extracted from `TextInterviewPage.tsx` if it becomes shared by recruiter or report surfaces.

### `Button`

Reuse:

- Variant API
- Size API
- Native button props
- Ref forwarding

Improve its visual tokens and loading contract rather than introducing route-specific buttons.

### `Input`, `Select`, `Label`, and `Textarea`

Reuse:

- Native elements
- Shared focus and color styling
- Ref forwarding

Extend them with field IDs, errors, helper text, and described-by support at the form-field level.

### `Badge`

Reuse sparingly for:

- Extraction status
- A short confidence status when explained
- Semantic interview state

Do not use a badge for every skill or metadata value in the setup flow.

### `AppLayout`

Reuse:

- Protected shell
- Main landmark
- Skip link
- Shared content area

Its responsive sidebar breakpoint and decorative layers need separate simplification, but the shell itself should remain shared.

## 8. Components that should be simplified

### `InterviewExperienceIntro`

Current role:

- Marketing hero
- Route title
- Preparation explainer
- Scroll navigation
- Photography block

Recommended role:

- Compact page header with mode title and one sentence

Remove from the setup route:

- Large Pexels image
- Gradient scrim
- Minimum 520px height
- Three preparation rows
- `Set up my interview` scroll CTA
- Fade-in animation

If the visual introduction is valuable for first-time onboarding, move it to a dedicated onboarding context rather than showing it on every new interview.

### `CandidateProfilePreview`

Current role:

- Full extracted CV inspection

Recommended default:

- Compact analyzed-CV summary containing:
  - Name
  - Current or recent role
  - Years of experience
  - Top five skills
  - Plain-language extraction status
  - `View extracted details`
  - `Replace CV`

Keep projects, full work history, education, and evidence inside an accessible disclosure or a separate review view.

### `Card`

Current role:

- Default wrapper for almost every section
- Adds 20px radius, border, hairline, and shadow

Recommended role:

- Opaque bordered container for a distinct object or task

Remove the default shadow and reduce the radius. Upload and configuration can share one sequential surface or use simple sections separated by a divider.

### `Session Setup`

Current role:

- Sticky duplicate of every visible form value

Recommended role:

- Remove it, or reduce it to one compact confirmation line directly above the primary action:

`Text interview, English, senior level, 10 questions, 30 minutes`

Do not reserve a 360px column for values the user can already see.

### Step number spans

Replace decorative circles with semantic headings:

- `1. Upload and review your CV`
- `2. Configure your interview`

Use an ordered list only if the steps remain simultaneously visible. If step 2 is progressively revealed, ordinary headings are sufficient.

### Skill and technology badges

Show only the most useful skills in the default summary. Use a short list or `5 more` disclosure for the rest. A large field of pills makes the profile visually noisy.

## 9. Places where the UI looks generic or AI-generated

### Split hero with stock photography

`InterviewExperienceIntro` combines:

- Oversized display heading
- Small accent eyebrow
- Generic professional Pexels image
- Dark image scrim
- Rounded 28px container
- Large shadow
- Generic preparation rows

This is a recognizable SaaS landing-page pattern. It is not specific to uploading a CV or starting an interview.

### Decorative AI iconography

The preparation list uses `Sparkles` for `Choose your target`. It does not communicate a distinct action or state.

### Rounded-container repetition

The page uses large rounded containers for the hero, upload task, extracted profile, form, summary, file row, and helper note. The number of containers makes the interface look generated from a component-library template.

### Excessive softness and elevation

Large radii, multiple shadows, glass panels in the app shell, an ambient grid, and a blurred accent orb combine into an AI-SaaS visual style. These treatments reduce the seriousness of a candidate assessment product.

Relevant shell evidence:

- `AppLayout.tsx`, ambient grid and blurred accent orb
- `Sidebar.tsx`, `.glass-panel`, 24px radius, and large shadow
- `index.css`, `.ambient-grid` and `.glass-panel`

### Template-like step treatment

The numbered header badges, equal card headers, and duplicate summary column resemble a generated multi-step form template. The real workflow is only two steps and does not need that much framing.

### Generic copy

The following copy is plausible but not highly specific:

- `Build your interview.`
- `Choose your target`
- `Review before starting`
- `Tune the session to the role you are preparing for.`
- `Set up my interview`

More direct product copy would name the actual operation, required input, and outcome.

### Confidence presented as a decorative badge

`92% confidence` or another extracted value appears as a green success badge without explaining:

- What the confidence measures
- Whether the candidate needs to act
- What threshold counts as low confidence
- Which fields are uncertain

This makes AI output appear more authoritative than the interface can justify.

## 10. The smallest redesign that meaningfully improves the experience

### Scope

Keep:

- Existing routes
- Existing APIs
- Existing interview configuration fields
- Existing preference defaults
- Existing file validation
- Existing candidate profile model
- Existing mode-specific navigation
- Existing shared UI primitives after token cleanup

Do not add:

- A new wizard library
- New backend endpoints
- Drag-and-drop as a requirement
- A separate text and speech setup implementation
- A new design system
- Additional onboarding screens

### Recommended page structure

```text
Text interview / Speech interview
One sentence explaining the mode

1. Upload and review your CV
   [Native file input] [Upload and analyze]
   Accepted files and size
   Loading, error, or success status in one stable region

   After success:
   [Name, role, experience, top skills]
   [View extracted details] [Replace CV]

2. Configure your interview
   [Language] [Experience level]
   [Interview style] [Duration]
   [Question count]
   [Interview objective, optional]

   Text interview, English, senior level, 10 questions, 30 minutes
   [Start text interview]
```

For speech mode, the final label becomes `Start speech interview`.

### Five changes with the highest value

#### 1. Replace the hero with a compact page header

Render the mode title and one short description immediately above the upload step. Remove the scroll CTA and photography from this product route.

Result:

- The file input becomes visible much earlier.
- Returning users can act immediately.
- The page has one real primary action per state.

#### 2. Make the existing two steps progressive

Show step 1 first. Reveal or activate step 2 after a profile is successfully extracted.

Do not hide progress without explanation. Before success, show a short statement where step 2 will appear:

`Upload and analyze your CV to configure the interview.`

Result:

- The disabled state has a reason.
- The sequence is obvious.
- The page does not show a large inactive form before its prerequisite.

#### 3. Collapse the extracted profile by default

After upload, show only the fields needed to confirm the correct CV was processed. Put all evidence and history behind `View extracted details`.

Add `Replace CV`. If editing extracted fields is not supported, say so plainly:

`If this profile is incorrect, replace the CV before starting.`

Result:

- Success is clear without pushing the form down.
- AI-derived content becomes reviewable and recoverable.

#### 4. Remove the sticky duplicate summary

Replace the 360px `Session Setup` panel with one compact sentence above the final action.

Result:

- More width for the form at 1024px.
- Less repetition.
- The start action stays close to the settings it submits.

#### 5. Complete the state and accessibility contract

Within the existing component structure:

- Give every field an `id` and connected label.
- Add helper and error IDs through `aria-describedby`.
- Add inline validation messages.
- Use a dedicated existing-session loading view.
- Give the page-level start error `role="alert"` and move focus to it.
- Use `aria-busy` during upload and start.
- Change the loading label to `Starting text interview` or `Starting speech interview`.
- Respect reduced motion before smooth scrolling, or remove the scroll behavior with the hero.
- Explain low-confidence or partial extraction.
- Add explicit `Try again` and `Replace CV` actions.

### Responsive minimum

- At 1440px, keep the form within a consistent readable frame. Do not stretch the upload card to 1500px.
- At 1024px, use one main column or a balanced two-column field grid. Do not reserve 360px for the summary.
- At 768px, switch to the mobile app shell rather than the expanded 260px sidebar.
- At 390px, use one column, 16px gutters, and full-width primary actions.

### Expected outcome

This redesign preserves nearly all application logic while:

- Moving the first meaningful action above the fold
- Reducing five major visual regions to two task steps
- Replacing multiple apparent starts with one state-appropriate primary action
- Making AI extraction easier to trust and recover from
- Removing duplicated settings
- Fixing the most important form and loading accessibility gaps
- Making the flow feel like InterviewOS instead of a generic AI SaaS template

### Acceptance criteria

- The resume input is visible without using a scroll CTA at common desktop heights.
- The page shows one obvious primary action in each state.
- Step 2 is unavailable with a visible reason until CV analysis succeeds.
- A successfully analyzed CV can be replaced.
- Detailed extracted profile data does not push configuration far down the page by default.
- The final button says `Start text interview` or `Start speech interview`.
- All form labels are programmatically connected.
- Upload and start loading states are announced.
- Upload and start errors include an explicit recovery action.
- Loading `/text-interview/:sessionId` never displays the new-interview setup.
- The layout works at 1440px, 1024px, 768px, and 390px.
- No route, API, backend model, or interview-state behavior changes are required.
