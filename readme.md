# Avinash Gembali — Portfolio

A personal developer portfolio built with **Angular 17**, **Tailwind CSS**, **Angular Animations**, and **EmailJS** for the contact form. Single-page application with smooth scroll, intersection-observer animations, and a working mail integration.

---

## Tech Stack

| Layer | Technology |
|---|---|
| Framework | Angular 17 (standalone components) |
| Styling | Tailwind CSS 3 + custom CSS |
| Animations | Angular Animations (`@angular/animations`) + CSS Intersection Observer |
| Contact form | EmailJS (`@emailjs/browser`) |
| Carousel | Swiper.js |
| Font | Poppins (Google Fonts) |
| Language | TypeScript 5.4 |

---

## Prerequisites

Make sure the following are installed before you begin:

- [Node.js](https://nodejs.org/) v18 or later
- [npm](https://www.npmjs.com/) v9 or later (comes with Node)
- Angular CLI v17

```bash
npm install -g @angular/cli@17
```

---

## Clone & Install

```bash
git clone https://github.com/your-username/AvinashPortfolio.git
cd AvinashPortfolio/frontend
npm install
```

---

## Environment Setup (EmailJS keys)

The project uses an environment file to keep API keys out of source code.

1. Copy the example file:

```bash
cp src/environments/environment.example.ts src/environments/environment.ts
```

2. Open `src/environments/environment.ts` and fill in your own EmailJS credentials:

```typescript
export const environment = {
  emailjs: {
    serviceId:  'YOUR_SERVICE_ID',   // e.g. service_abc123
    templateId: 'YOUR_TEMPLATE_ID', // e.g. template_xyz789
    publicKey:  'YOUR_PUBLIC_KEY',  // e.g. xxxxxxxxxxxxxxx
  },
};
```

> **Never commit** the real `environment.ts` — add it to `.gitignore`.

---

## EmailJS Setup (step-by-step)

[EmailJS](https://www.emailjs.com/) lets you send emails directly from the browser with no backend needed.

### 1 — Create a free account

Go to [https://www.emailjs.com](https://www.emailjs.com) and sign up. The free plan allows **200 emails/month**.

### 2 — Add an Email Service

- In the EmailJS dashboard go to **Email Services → Add New Service**.
- Choose your email provider (Gmail, Outlook, etc.) and connect your account.
- Copy the **Service ID** (looks like `service_xxxxxxx`).

### 3 — Create an Email Template

- Go to **Email Templates → Create New Template**.
- Design your template using these variables that the portfolio sends:

| Template variable | Maps to |
|---|---|
| `{{from_name}}` | Sender's name from the form |
| `{{subject}}` | Message subject |
| `{{message}}` | Message body |
| `{{to_email}}` | Your email address |
| `{{reply_to}}` | Sender's email address |

- Save and copy the **Template ID** (looks like `template_xxxxxxx`).

### 4 — Get your Public Key

- Go to **Account → General** (or the API Keys section).
- Copy your **Public Key**.

### 5 — Paste into environment.ts

```typescript
export const environment = {
  emailjs: {
    serviceId:  'service_xxxxxxx',
    templateId: 'template_xxxxxxx',
    publicKey:  'xxxxxxxxxxxxxxx',
  },
};
```

How the contact component uses it (`src/app/components/contact/contact.component.ts`):

```typescript
import emailjs from '@emailjs/browser';
import { environment } from '../../../environments/environment';

constructor() {
  emailjs.init(environment.emailjs.publicKey);
}

async onSubmit() {
  await emailjs.send(
    environment.emailjs.serviceId,
    environment.emailjs.templateId,
    {
      from_name:  this.form.name,
      from_email: this.form.email,
      subject:    this.form.subject,
      message:    this.form.message,
      to_email:   'your@email.com',
      reply_to:   this.form.email,
    }
  );
}
```

---

## Angular Animations Setup

Angular Animations are already wired in this project. Here is how it was done so you can replicate it in any Angular 17 app.

### 1 — Install the package

```bash
npm install @angular/animations
```

### 2 — Provide animations in `app.config.ts`

```typescript
import { provideAnimations } from '@angular/platform-browser/animations';
import { provideRouter, withViewTransitions } from '@angular/router';

export const appConfig: ApplicationConfig = {
  providers: [
    provideRouter(routes, withViewTransitions()),  // native View Transitions API on route change
    provideAnimations(),                           // enables Angular animation engine
  ]
};
```

### 3 — Scroll animations via Intersection Observer

Rather than Angular `trigger()` / `state()` declarations, this project uses a lightweight CSS + Intersection Observer pattern added to each component's `ngOnInit`:

```typescript
import { Component, ElementRef, OnInit } from '@angular/core';

export class YourComponent implements OnInit {
  constructor(private el: ElementRef) {}

  ngOnInit() {
    const observer = new IntersectionObserver(
      entries => entries.forEach(e =>
        e.isIntersecting && e.target.classList.add('visible')
      ),
      { threshold: 0.15 }
    );
    setTimeout(() => {
      this.el.nativeElement
        .querySelectorAll('.animate-on-scroll')
        .forEach((el: Element) => observer.observe(el));
    }, 100);
  }
}
```

Add the class to any element in your template:

```html
<div class="animate-on-scroll">Fades in when scrolled into view</div>
```

The animation CSS is defined globally in `src/styles.css`:

```css
.animate-on-scroll {
  opacity: 0;
  transform: translateY(30px);
  transition: opacity 0.6s ease, transform 0.6s ease;
}
.animate-on-scroll.visible {
  opacity: 1;
  transform: translateY(0);
}
```

---

## Tailwind CSS Setup

Tailwind is already configured. For reference, here is how it was added:

```bash
npm install -D tailwindcss postcss autoprefixer
npx tailwindcss init
```

`tailwind.config.js`:

```js
module.exports = {
  content: ['./src/**/*.{html,ts}'],
  theme: {
    extend: {
      colors: {
        primary: '#f97316',   // orange accent used throughout
        dark: '#1a1a2e',
        darker: '#0f0f1a',
      },
      fontFamily: {
        sans: ['Poppins', 'sans-serif'],
      },
    },
  },
  plugins: [],
};
```

`src/styles.css` starts with:

```css
@tailwind base;
@tailwind components;
@tailwind utilities;
```

---

## Run Locally

```bash
cd frontend
ng serve
```

Open [http://localhost:4200](http://localhost:4200) in your browser.

---

## Build for Production

```bash
ng build
```

Output is placed in `dist/frontend/browser/`. Deploy that folder to any static host — Vercel, Netlify, GitHub Pages, Firebase Hosting, etc.

---

## Project Structure

```
AvinashPortfolio/
└── frontend/
    ├── src/
    │   ├── app/
    │   │   ├── components/
    │   │   │   ├── navbar/
    │   │   │   ├── hero/
    │   │   │   ├── about/
    │   │   │   ├── resume/
    │   │   │   ├── domains/
    │   │   │   ├── skills/
    │   │   │   ├── projects/
    │   │   │   ├── hire-me/
    │   │   │   ├── contact/       ← EmailJS integration lives here
    │   │   │   └── footer/
    │   │   ├── pages/
    │   │   │   └── home/          ← assembles all section components
    │   │   ├── services/
    │   │   │   └── portfolio.service.ts  ← all content data (skills, projects, etc.)
    │   │   ├── app.config.ts      ← provideAnimations, provideRouter
    │   │   └── app.routes.ts
    │   ├── environments/
    │   │   ├── environment.example.ts   ← template (safe to commit)
    │   │   └── environment.ts           ← your real keys (do NOT commit)
    │   ├── assets/
    │   │   ├── images/            ← profile pic, project screenshots
    │   │   └── Gembali_Avinash_Resume.pdf
    │   ├── styles.css             ← Tailwind directives + animate-on-scroll
    │   └── index.html             ← Poppins font import
    ├── tailwind.config.js
    ├── angular.json
    └── package.json
```

---

## Customising the Content

All portfolio data (name, skills, experience, projects) is centralised in one file:

```
frontend/src/app/services/portfolio.service.ts
```

Edit the arrays in that service to update your own information — no need to touch individual component templates.

---

## Personalising Your Details

Before deploying, update the following:

| File | What to change |
|---|---|
| `src/index.html` | Page `<title>` and meta description |
| `src/app/services/portfolio.service.ts` | Name, skills, experience, projects |
| `src/app/components/contact/contact.component.ts` | Your phone and email in `contactCards` |
| `src/assets/images/` | Replace `profilepic.png` and project screenshots |
| `src/assets/Gembali_Avinash_Resume.pdf` | Replace with your own resume PDF |

---

## License

MIT — free to fork and personalise.
