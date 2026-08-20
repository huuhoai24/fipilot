# Interview Experience Dialog Specification

## Source and placement

Directly observed on `https://www.hackerrank.com/mock-interviews/all-roles/recruiter` on 2026-08-19. In the AI Fluency clone this is the first setup step opened by `Try for free`, before resume upload and device checks.

Reference screenshots: `interview-experience-desktop.png`, `interview-experience-custom-desktop.png`, `interview-experience-tablet.png`, and `interview-experience-mobile.png`.

## Structure and text

- Modal title: `Choose Your Mock Interview Experience`
- Subtitle: `Start with popular ready-made roles or build your own based on a specific job description.`
- Software Engineer — `DSA, system design, coding patterns, and problem-solving`
- Frontend Developer — `React, Angular, Vue, and problem-solving`
- Backend Developer — `Node, Python, Java, and problem-solving`
- AI Engineer — `Machine Learning, Deep Learning, Generative AI, LLMs, and problem-solving`
- Forward Deployed Engineer — `AWS, Azure, and problem-solving`
- + Custom Role — `Paste a job description for a tailored interview`
- Footer actions: `Cancel` and `Continue`.

## Desktop measurements

The backdrop is `rgba(18,20,24,.85)`. The dialog is 640x650 at x400/y125 in a 1440x900 viewport, white, 12px radius, 24px outer padding, and `overflow: hidden auto`. Content is 552px wide at x444. The title is 24px/36px, weight 700, color `rgb(74,75,83)`, with 8px bottom margin. Subtitle is 12px/18px with 16px bottom margin.

The card grid is 552x372, three 173.328px columns, two rows, and 16px gap. Each card is 178px tall with 24px padding and 12px radius. Standard cards use a 1px solid `rgb(235,235,243)` border; Custom Role uses a dashed border. Card headings are 14px/24px weight 700 and descriptions are 12px/20px.

Selected cards use `rgb(246,246,255)` and a 2px `rgb(35,88,219)` outline. Continue is disabled (`rgb(193,194,214)`) until a valid role is selected, then green `rgb(19,129,58)`. Buttons are 40px tall, 8px radius, 14px/20px, with 20px horizontal padding.

## Custom Role state

Selecting Custom Role appends a textarea below the grid. Placeholder: `Paste your job description here and we'll create a tailored interview...`. It is 537x202 desktop, 10px 12px padding, 1px `rgb(144,145,168)` border, 8px radius, 14px type, and does not resize. Helper text is `Minimum 100 characters required`, 12px/20px. Continue remains disabled below 100 characters. The textarea extends below the initial viewport and is reached with native modal scrolling.

## Responsive behavior

At 768x900 the dialog is 614.39x650 at x76.8. The grid switches to one 511.39px column, six 178px rows, 16px gap, and scrolls within the modal. At 390x844 the dialog is 312x650 at x39/y97, content is 224px wide after padding, and the grid is one 209px column. Its footer follows the long grid in the scroll area rather than remaining sticky; the observed scroll range was 828px.

## Interaction contract

Card wrappers are focusable `role=button` controls and activate with pointer or Space. Choosing a built-in card enables Continue. Back from Upload Resume returns to this step with no role selected in the observed flow. Cancel closes setup. Continue advances to Upload Resume and does not navigate.
