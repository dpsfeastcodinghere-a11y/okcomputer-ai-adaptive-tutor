# How to Remove Profile Selection

## Option 1: Add CSS (Easiest)

Add this line in the `<head>` section of `learning.html`:

```html
<link rel="stylesheet" href="hide_profile_modal.css">
```

## Option 2: Add JavaScript

Add this line before `</body>` in `learning.html`:

```html
<script src="skip_profile_selection.js"></script>
```

## Option 3: Manual Edit

Find line ~225 in `learning.html` and add:

```css
#onboardingStep1 { display: none !important; }
#onboardingStep2 { display: block !important; }
```

Then refresh browser with `Ctrl + F5`
