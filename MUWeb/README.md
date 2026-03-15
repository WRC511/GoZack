# Underwear E-commerce Web Application

A Flask-based web application for browsing and managing an underwear e-commerce store. This application allows users to view products, search for items, like/unlike products, and manage their favorites.

## Features

- Browse a catalog of underwear products
- Search functionality to find specific items
- View detailed product information
- Like/unlike products
- View your liked items
- Responsive design

## Project Structure

```
.
├── server.py          # Main Flask application
├── templates/         # HTML templates
│   ├── layout.html    # Base template
│   ├── homepage.html  # Homepage template
│   ├── search.html    # Search results template
│   ├── view.html      # Product detail template
│   └── likes.html     # Liked items template
└── static/           # Static files (CSS, JS, images)
```

## Setup and Installation

1. Make sure you have Python 3.x installed on your system
2. Install the required dependencies:
   ```bash
   pip install flask
   ```

## Running the Application

1. Navigate to the project directory
2. Run the Flask application:
   ```bash
   python3 server.py
   ```
3. Open your web browser and visit `http://127.0.0.1:5000`

## API Endpoints

- `GET /` - Homepage
- `GET /api/popular-items` - Get popular items
- `GET /search` - Search for items
- `GET /view/<int:item_id>` - View item details
- `POST /like/<int:item_id>` - Like an item
- `GET /mylikes` - View liked items
- `POST /unlike/<int:item_id>` - Unlike an item

## Development

The application uses:
- Flask for the backend
- HTML/CSS for the frontend
- JavaScript for dynamic functionality

## Publishing on GitHub Pages

GitHub Pages only serves **static files** (HTML, CSS, JS). It does not run Python or Flask, so the live site uses a static version of the app.

**What was added for GitHub Pages:**

- **`index.html`** – Homepage (required by GitHub for the root URL)
- **`search.html`**, **`view.html`**, **`likes.html`** – Static versions of search, product detail, and likes
- **`static/products.json`** – Product data for the static site
- **`static/script-pages.js`** – Logic for the static site (loads JSON, uses `localStorage` for likes)

**How to publish:**

1. Push your repo to GitHub (including the new files above).
2. In the repo: **Settings → Pages**.
3. Under **Build and deployment**, set **Source** to **Deploy from a branch**.
4. Choose branch **main** (or your default branch) and folder **/ (root)**.
5. Save. After a minute or two, the site will be at `https://<username>.github.io/<repo-name>/`.

**Note:** On GitHub Pages, “My Likes” is stored in your browser only (`localStorage`), not on a server. The Flask app (run locally with `python3 server.py`) still uses server-side sessions for likes.

## Notes

- This is a development server and should not be used in production
- The application uses session-based authentication for managing likes (Flask); the GitHub Pages version uses `localStorage`
- Product data is stored in-memory in `server.py` and in `static/products.json` for the static site