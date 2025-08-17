# Confession Webpage

A simple interactive confession webpage where users can respond to a question with "Yes" or "No". The "No" button changes its text when clicked and the "Yes" button leads to a confirmation page.

## Features

- Interactive buttons with responsive behavior
- "Yes" button redirects to a confirmation page
- "No" button changes its text sequentially when clicked
- "Yes" button increases in size with each "No" click
- Stylish design with centered content and theme colors

## File Structure

```
.
├── index.html           # Main confession page
├── yes-index.html       # Confirmation page for "Yes" response
├── styles.css           # Main stylesheet
├── yes_styles.css       # Styles for the confirmation page
├── script.js            # Interactive functionality
└── Imgs/                # Image assets
    ├── VM1fcpu2bKs1e2Kdbj.webp
    └── 9XY4f3FgFTT4QlaYqa.webp
```

## How It Works

1. The main page (`index.html`) displays a question with "Yes" and "No" buttons
2. Clicking "Yes" redirects to `yes-index.html` with a confirmation message
3. Clicking "No" cycles through different messages and increases the size of the "Yes" button
4. Styling is handled through CSS files with a consistent color scheme (reds and pinks for the theme)

## Customization

- Modify the question in `index.html` by changing the text inside the `<h1>` tag
- Update the messages for the "No" button by editing the `no_messages` array in `script.js`
- Change colors by modifying the CSS variables and color values in `styles.css` and `yes_styles.css`
- Replace images by updating the `src` attributes in the `<img>` tags with your own image paths

## Dependencies

- No external dependencies, uses plain HTML, CSS, and JavaScript
- Font: "楷体" (KaiTi) with sans-serif fallback

## Usage

Simply open `index.html` in a web browser to use the confession page.
