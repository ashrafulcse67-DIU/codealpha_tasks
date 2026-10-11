# Personal Portfolio Website
A responsive personal portfolio website: plain HTML, CSS and JavaScript. No framework, no build step for visitors, no dependencies.

# Run it
Open index.html in a browser, or upload the contents of Task-1/ to any static host (such as Cloudflare Pages, Netlify, or Vercel). (The Telegram contact form messaging feature requires the site to be served with backend worker support, e.g., Cloudflare Pages.)

# Before you publish (customize your details)
- Open index.html and update the D (Data) JavaScript object at the bottom with your personal info, projects, experience, certificates, gallery images, and video links.
- Replace cv-ashraful.pdf with your updated CV document.
- Place your profile photo, project thumbnails, and gallery posters inside the respective image folders.

# Structure
Task-1/               the portfolio website root
  index.html          main portfolio landing page and dynamic template engine
  cv-ashraful.pdf     professional resume / CV
  images/             profile photo, project screenshots, gallery posters
  certificates/       diu, hp, and professional certificates
  _worker.js          Cloudflare Pages worker for Telegram contact form API integration

# Customizing Content
1. Edit the personal, roles, and social links object inside index.html to reflect your professional profiles.
2. Add or update projects, client works, experience timelines, and media galleries directly within the JavaScript D object.
3. Place certificate files in their respective folders and map them inside the certs data array.

# Notes
- English and Bengali toggle translates navigation, headings, and key sections dynamically.
- Dark and light theme preferences are saved locally in the visitor's browser.
- Contact form submissions are handled securely via a Telegram bot API worker script without storing sensitive data on public servers.
