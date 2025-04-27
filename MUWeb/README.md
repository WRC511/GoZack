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

## Notes

- This is a development server and should not be used in production
- The application uses session-based authentication for managing likes
- Product data is currently stored in-memory in the server.py file 