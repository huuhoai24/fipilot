# Observed Behaviors

## Verified states

- Desktop 1440px: primary navigation links and the interview-preview controls are visible.
- Tablet 768px: only compact header controls and the profile control are exposed; primary navigation links are absent from the accessibility tree.
- Mobile 390px: a leading menu button and HackerRank logo are exposed in addition to compact header controls and profile control.
- Profile menu: clicking `Drop Down Menu Trigger` opened menu items: Profile, Leaderboard, Settings, Plans, Bookmarks, Submissions, Administration, and Logout.
- Start gate: activating `Try for free` opened an `Audio & Camera Settings` modal.
- Device-settings modal: the observed controls were microphone selector (Built-in Audio Analog Stereo), microphone level meter, speaker selector (Built-in Audio Analog Stereo), Test Speakers, camera selector (Integrated Webcam), Cancel, and Start Interview.
- Start action: Start Interview was issued with user authorization. Immediately afterwards, browser-CDP snapshot and tab-list requests exceeded their 30-second timeouts, so no subsequent interview state is asserted.

## Controls not activated

- `Try for free` was activated with explicit user authorization and opened the Audio & Camera Settings modal.
- The moon-icon theme control was not clicked because it changes a user preference.
- `Mute microphone` and `Disable video` were not clicked because they change live session/device state.
- Navigation links and menu destinations were not followed because navigation was out of scope.

## Scroll and animation

- At the 1440px × 1000px inspected viewport, `document.documentElement.scrollHeight` was 1000px. No scroll-triggered state was directly observed.
- Observed button transitions: header icon buttons use `color 0.2s ease-in-out, backgroundColor 0.2s ease-in-out, borderColor 0.2s ease-in-out`; CTA has the same transition; microphone/video controls use `0.1s ease-in-out`.
