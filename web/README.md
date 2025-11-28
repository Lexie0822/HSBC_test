# Property Portal – Next.js Frontend

This directory contains a minimal Next.js (App Router) portal that brings together two
independent applications:

1. **Property Estimator** – a client for the Python FastAPI backend that allows users to
   input property details and obtain a price estimate.
2. **Property Market Analysis** – a client for the Java/Spring Boot backend that displays
   aggregate statistics about the housing market.

The project uses the App Router introduced in Next.js 13.  A shared layout implements
navigation between applications and sets up a consistent look and feel.  Each application
lives under its own route (`/property-estimator` and `/property-analysis`) and is
implemented as a client component when interactivity is needed.

> **Note:**  This skeleton is intended to illustrate the structure and does not include
> complete error handling or production styling.  It uses Tailwind CSS for rapid UI
  development.  See the tasks document for suggestions on how to extend it with client
  validation, charts and additional views.

## Prerequisites

* Node.js 18 or higher
* `npm` or `pnpm`

## Install and run locally

```sh
cd web
npm install
npm run dev
```

The development server will start on <http://localhost:3000> by default.

## Project Structure

```
web/
├── app/
│   ├── layout.tsx             # Root layout with navigation
│   ├── page.tsx               # Landing page
│   ├── property‑estimator/
│   │   └── page.tsx          # Property estimator application
│   └── property‑analysis/
│       └── page.tsx          # Property market analysis application
├── components/               # Shared components (navbar, etc.)
├── styles/                   # Global styles and Tailwind configuration
└── package.json              # Project metadata and dependencies
```
