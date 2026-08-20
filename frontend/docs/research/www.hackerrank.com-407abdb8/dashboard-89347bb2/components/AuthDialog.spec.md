# AuthDialog Specification (Login / Signup Popup)

## Overview
- **Target file:** `src/components/sites/www.hackerrank.com-407abdb8/dashboard-89347bb2/AuthDialog.tsx`
- **Screenshots:**
  - `docs/design-references/www.hackerrank.com-407abdb8/dashboard-89347bb2/auth-popup-login-desktop-1440.png`
  - `docs/design-references/www.hackerrank.com-407abdb8/dashboard-89347bb2/auth-popup-signup-desktop-1440.png`
  - `docs/design-references/www.hackerrank.com-407abdb8/dashboard-89347bb2/auth-popup-signup-mobile-390.png`
  - `docs/design-references/www.hackerrank.com-407abdb8/dashboard-89347bb2/auth-popup-login-mobile-390.png`
- **Interaction model:** click-driven (modal dialog). Opened by header "Log In" (login mode) / "Sign Up" (signup mode) buttons. Two modes switchable via footer link. Radix-style dialog behavior.
- **Customization (user-requested):** social login buttons (Google / LinkedIn / GitHub) and the "or" divider are **removed**. Only email-based login and signup remain. The `orDivider`, `GoogleIcon`, `LinkedInIcon`, `GitHubIcon` were deleted from the component and `shared/icons.tsx`.

## DOM Structure
```
<div role="dialog" class="dialog">            fixed, centered, z-990, bg #FFF, radius 12px
  <div class="authBox">                        padding 48px (32px mobile)
    <div class="headerRow">                    flex space-between
      <div class="titles">                     flex column
        <h1>Welcome Back!</h1>                 login mode
        <h1>Login to your account</h1>
        -- or (signup mode) --
        <h1>Join us</h1>
        <h1>Create a HackerRank account</h1>
      </div>
      <button aria-label="Close">40x40 X button</button>
    </div>
    <h4 class="subtitle">                      14px/400/20px, margin-top 8px
      "It's nice to see you again. Ready to code?" (login)
      "Be part of a 30 million-strong community of developers" (signup)
    </h4>
    <form class="form">                        margin-top 16px, flex column, gap 16px
      [LOGIN] input username | input password | submit "Log In" | row(remember + forgot)
      [SIGNUP] input name | input email | input password | row(tos checkbox + text) | submit "Sign up"
    </form>
    <div class="footerRow">                    centered, margin 32px top / 16px bottom
      <h4 class="hr-body-lg">"Don't have an account?" <a>Sign up</a></h4>   (login mode)
      <h4 class="hr-body-lg">"Already have an account?" <a>Log in</a></h4>   (signup mode)
    </div>
  </div>
</div>
```
> **Removed (user customization):** the entire `<div class="socialSection">` (or divider + Google + LinkedIn + GitHub) that sat between `</form>` and the footer row.

## Computed Styles (exact values from getComputedStyle)

### Dialog container (div[role=dialog])
- position: fixed; z-index: 990
- Centered: left 50%, top 50%, transform: translate(-50%, -50%)
- width: 548px (desktop ≥768); maxWidth 548px; height auto; minHeight 120px
- Mobile (<768px): width: min(548px, 80vw) (verified: 500vw→400px, 390vw→312px); maxHeight: 95%; padding 32px
- maxHeight: calc(100% - 128px) (desktop)
- border-radius: 12px; border: 0; background: #FFFFFF
- font-family: Satoshi, "Open Sans", OpenSans, arial, helvetica, sans-serif
- Enter animation: 0.15s cubic-bezier(0.16, 1, 0.3, 1); keyframes: from opacity 0, translateY(-20px) scale(0.96) → opacity 1, none

### Overlay (backdrop)
- position: fixed; inset: 0; z-index: 989
- background: rgba(18, 20, 24, 0.85)
- Animation: fade-in opacity 0 → 1, 0.15s cubic-bezier(0.16, 1, 0.3, 1)

### Header row (.headerRow)
- display: flex; justify-content: space-between; align-items: center (stretch)

### Titles (h1.hr-title-lg)
- font-size: 24px; font-weight: 700; line-height: 36px; color: #121418
- Two h1 stacked vertically (flex column, gap 0)

### Close button
- width: 40px; height: 40px; min-width: 40px; min-height: 40px
- border-radius: 8px; border: 1px solid #9091A8 (rgb 144,145,168); background: transparent
- color: #121418; display: inline-flex; justify-content/align-items center
- X icon: 20px, stroke currentColor, stroke-width 1.5, viewBox 24: `m6 6 12 12M18 6 6 18`
- transition: color/backgroundColor/borderColor 0.2s ease-in-out

### Subtitle (h4)
- font-size: 14px; font-weight: 400; line-height: 20px; color: #121418
- margin-top: 8px

### Form
- margin-top: 16px; display: flex; flex-direction: column; gap: 16px

### Inputs (.input)
- width: 100% (452px in 548px dialog); height: 40px; padding: 10px 12px
- border-radius: 8px; border: 1px solid #9091A8
- background: #FFFFFF; color: #1F202A; font-size: 14px
- Focus & hover: border-color: #63646F (no box-shadow, no outline)
- Placeholder: color #63646F, font-size 14px, font-weight 500
- caret-color: #1F202A

### Submit button (primary, disabled)
- width: 100%; height: 48px; padding: 16px 20px
- border-radius: 8px; border: none
- disabled: background: #C1C2D6; color: #FFFFFF
- enabled: background: #13813A; color: #FFFFFF; hover: #0E612C
- font-size: 14px; font-weight: 700; line-height: 20px

### Remember me row
- display: flex; justify-content: space-between; align-items: center
- Checkbox: width/height 20px; border-radius: 4px; border: 1px solid #9091A8; background: #F7F8FD
  - checked: background #121418; border-color #121418; white check icon 16px `m19 7.188-9.625 9.625L5 12.438` stroke 1.5
- Label: font-size 14px; font-weight 400; line-height 20px; color: #4A4B53; cursor pointer

### Forgot password? link
- font-size: 14px; font-weight: 500; line-height: 20px; color: #2358DB; cursor: pointer

### Signup TOS row
- display: flex; align-items: center; gap: 8px (hr-gap-0.5 = 8px)
- Same checkbox as above; h5 text: 14px/400/20px #121418
- Links "Terms of Service" and "Privacy Policy": 14px/500 #2358DB, target _blank

### "or" divider
- font-size: 14px; font-weight: 400; line-height: 20px; color: #121418
- margin-top: 32px; position: relative; display flex; centered
- ::before / ::after: content ""; position absolute; top 9.5px; width 210px; height 1px; border-top 1px solid #EBEBF3
  - ::before left: 0; ::after right: 0 (mirror)
- **Removed (user customization):** the divider and all social buttons were deleted from the clone.

### Social buttons
- Base: height 48px; padding 16px 20px; border-radius 8px; border 1px solid #9091A8; background transparent
- font-size: 14px; font-weight 700; line-height 20px; color: #121418
- Icon gutter: margin-right 4px (icon 20-21px)
- Google: width 100% (452px); margin: 16px 0
- LinkedIn / GitHub row: display flex; gap 16px; each width 218px (flex 1)
  - Mobile (<768px): each width 100% (stacked)
- Hover: background #F7F8FD? (not extracted — use border-color #63646F + bg #EBEBF3 light; keep simple: same as login header buttons pattern: hover background-color #63646F is for login button; for secondary buttons use hover bg #EBEBF3 — verify in QA)
- **Removed (user customization):** these styles are no longer used in the clone.

### Footer row
- display: flex; justify-content: center; align-items: center
- margin: 32px 0 16px
- h4 text: 16px; font-weight 400; line-height 24px; color #121418
- Link ("Sign up" / "Log in"): font-size 16px; font-weight 500; line-height 24px; color #2358DB; cursor pointer

## States & Behaviors

### Open
- Header "Log In" → opens dialog in login mode; "Sign Up" → signup mode
- Autofocus first input (username / Full Name)
- Enter animation 0.15s cubic-bezier(0.16,1,0.3,1): dialog translateY(-20px) scale(0.96) → identity; overlay fade 0→1

### Mode switch
- Login footer link "Sign up" → swaps to signup mode (headings, form, footer text)
- Signup footer link "Log in" → swaps to login mode
- No route change (href="#" in dialog)

### Close
- X button, Escape key, click on backdrop → close
- Overlay fade-out 0.15s

### Submit buttons
- Disabled while required fields empty; enabled when filled (client-side mock)
- No real auth (out of scope)

### Remember me / TOS checkbox
- Toggle checked state: unchecked → bg #F7F8FD/border #9091A8; checked → bg/border #121418 + white check

## Assets
- No raster images. Icons as React components (add to `src/components/sites/www.hackerrank.com-407abdb8/shared/icons.tsx`):
  - `CloseIcon`: stroke currentColor, stroke-width 1.5, viewBox 24, path `m6 6 12 12M18 6 6 18`
  - `CheckIcon`: stroke currentColor, stroke-width 1.5, viewBox 24, path `m19 7.188-9.625 9.625L5 12.438`

## Text Content (verbatim)
Login mode:
- "Welcome Back!" / "Login to your account"
- "It's nice to see you again. Ready to code?"
- Inputs: "Your username or email", "Your password"
- Button: "Log In"
- "Remember me" / "Forgot password?"
- "Don't have an account?" + "Sign up"

Signup mode:
- "Join us" / "Create a HackerRank account"
- "Be part of a 30 million-strong community of developers"
- Inputs: "Full Name", "Email", "Your password"
- "I agree to HackerRank's" + "Terms of Service" + " and " + "Privacy Policy" + "."
- Button: "Sign up"
- "Already have an account?" + "Log in"

## Responsive Behavior
- **Desktop (1440px):** dialog 548px wide, padding 48px; inputs 452px
- **Tablet (768px):** identical to desktop (548px dialog; 768×80%=614 > 548 → 548)
- **Mobile (390px):** dialog width min(548px, 80vw) = 312px, padding 32px, maxHeight 95%
- **Breakpoint:** ~768px (width 548→min(548px,80vw), padding 48→32, maxHeight calc(100%-128px) → 95%); no <576px rule (80vw covers it)
- **Note:** social buttons (and their stacking at <768px) no longer exist in the clone.