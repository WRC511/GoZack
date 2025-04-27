from flask import Flask, render_template, jsonify, request, session, redirect
import os  # Import the 'os' module

app = Flask(__name__)
app.secret_key = os.urandom(24)  # Generate a random secret key

# Sample dataset (list of dictionaries)
underwear_items = [
    {
        "id": 1,
        "title": "Calvin Klein Cotton Stretch Boxer Briefs",
        "image": "https://xcdn.next.co.uk/common/items/default/default/itemimages/3_4Ratio/product/lge/146764s3.jpg?im=Resize,width=750",
        "description": "Designer boxer brief reinvented in extra-soft cotton stretch fabric. Wicking that keeps you cool and dry. Finctional fly, supportive pouch and longer leg line creates a supportive fit.",
        "price": "$29.99",
        "rating": 4.8,
        "likes": 0,
        "sizes": ["S", "M", "L", "XL"],
        "similar_items": ["Nike Dri-Fit Boxer Briefs", "Under Armour Performance Boxer Briefs"],
    },
    {
        "id": 2,
        "title": "Dragonfly Men's Bikram yoga shorts Mike",
        "image": "https://dragonflybrand.com/cdn/shop/products/mike-mens-shorts-dragonfly-xs-grey-752360.jpg?v=1745567964&width=1080",
        "description": "Made without any waistband or seams at the back so they do not cut in anywhere and feel like a second skin. The comfortable 4-way stretch fabric with Lycra adapts to your body, holds perfectly, sticks to the body like a second skin and does not restrict movement.",
        "price": "$67.00",
        "rating": 4.7,
        "likes": 0,
        "sizes": ["S", "M", "L"],
        "similar_items": ["Nike Pro Men's Dri-FIT Fitness Shorts", "Lululemon Men's Align Shorts"],
    },
    {
        "id": 3,
        "title": "Nike Dri-FIT Essential Micro Jockstrap",
        "image": "https://static.nike.com/a/images/t_PDP_1728_v1/f_auto,q_auto:eco/c3a99552-c7ae-4e89-afeb-e8d818d4302c/Nk++Esntl+MICRO+JOCK+STRAP+3PK.png",
        "description": "Stretch microfiber fabric delivers optimal flexibility that enhances your freedom of movement. Move with confidence while staying dry thanks to sweat-wicking technology. For workouts and daily wear.",
        "price": "$45.00",
        "rating": 4.6,
        "likes": 0,
        "sizes": ["S", "M", "L", "XL"],
        "similar_items": ["Under Armour Compression Shorts", "Calvin Klein Cotton Boxer Briefs"],
    },
    {
        "id": 4,
        "title": "2(X)ist Sport Brief",
        "image": "https://2xist.com/cdn/shop/products/021312_10001_S_93336d5f-ec0d-4448-acb4-ee8fa8fbd470.jpg?format=pjpg&v=1597605973&width=1680",
        "description": "Breathable fit and soft-stretch cotton fabric. Performance support for sports and high-intensity activities. Low rise waistband. Original Contour Pouch for added support.",
        "price": "$24.50",
        "rating": 4.8,
        "likes": 0,
        "sizes": ["S", "M", "L", "XL"],
        "similar_items": ["Calvin Klein Modern Air Sports Brief", "Garofali Split Brief"],
    },
    {
        "id": 5,
        "title": "Mack Weldon 24/7 Woven Boxers",
        "image": "https://cdn.shopify.com/s/files/1/0078/6825/2273/files/2024_Q3_PDP_247WovenBoxer_BrokeStripe_4818_bfa0c3f0-ae28-45ab-a4be-34b5b4813da8.jpg?v=1739550332&width=900",
        "description": "Soft and weightless fabric. Designed for all-day comfort. Anti-sag four-panel construction that maintains shape under your pants. Moisture-wicking technology. Hidden button fly.",
        "price": "$34.00",
        "rating": 4.9,
        "likes": 0,
        "sizes": ["S", "M", "L"],
        "similar_items": ["Calvin Klein Cotton Boxers", "Banana Republic Cotton Boxers"],
    },
    {
        "id": 6,
        "title": "Calvin Klein Sculpt Sport Briefs",
        "image": "https://calvinklein.scene7.com/is/image/CalvinKlein/61903857_001_alternate4?wid=680&qlt=80%2C0&resMode=sharp2&op_usm=0.9%2C1.0%2C8%2C0&iccEmbed=0&fmt=webp",
        "description": "Iconic waistband. Lightweight cotton blend. Feature packed with moisture wicking, quick-dry fabric. Odor resistant properties to keep you going day and night.",
        "price": "$36.00",
        "rating": 4.7,
        "likes": 0,
        "sizes": ["S", "M", "L", "XL"],
        "similar_items": ["Garofali Split Briefs", "2(X)ist Sport Brief"],
    },
    {
        "id": 7,
        "title": "Calvin Klein Micro Jockstrap",
        "image": "https://calvinklein.scene7.com/is/image/CalvinKlein/61904053_001_alternate3?wid=680&qlt=80%2C0&resMode=sharp2&op_usm=0.9%2C1.0%2C8%2C0&iccEmbed=0&fmt=webp",
        "description": "Classic jockstrap fit with a supportive contoured pouch. Wicking finish keeps you cool and dry. Signature Calvin Klein waistband. Made from extra-soft cotton stretch material for enhanced comfort.",
        "price": "$30.00",
        "rating": 4.5,
        "likes": 0,
        "sizes": ["S", "M", "L", "XL"],
        "similar_items": ["Nike Dri-Fit Essential Micro Jockstrap", "Under Armour Compression Shorts"],
    },
    {
        "id": 8,
        "title": "Garofali Split Briefs",
        "image": "https://www.garofali.com/cdn/shop/files/0059-T.jpg?v=1718037319&width=1080",
        "description": "Sleek and comfortable split-cut design with breathable fabric. Designed for minimizing friction while maximizing the exposure of the hips. Ultra-soft modal fabric allows optimal movement and fit.",
        "price": "$28.00",
        "rating": 4.8,
        "likes": 0,
        "sizes": ["S", "M", "L"],
        "similar_items": ["Calvin Klein Modern Cotton Stretch Sport Briefs", "2(X)ist Sport Brief"],
    },
    {
        "id": 9,
        "title": "Under Armour Performance Cotton Boxerjock",
        "image": "https://underarmour.scene7.com/is/image/Underarmour/V5-1383889-100_FC?rp=standard-0pad%7CpdpMainDesktop&scl=1&fmt=jpg&qlt=85&resMode=sharp2&cache=on%2Con&bgc=F0F0F0&wid=566&hei=708&size=566%2C708",
        "description": "Ultra-soft Charged Cotton fabric with 4-way stretch. Support pouch with fly opening. Wicking pulls sweat away from the skin and dries fast.",
        "price": "$42.00",
        "rating": 4.9,
        "likes": 0,
        "sizes": ["S", "M", "L", "XL"],
        "similar_items": ["Nike Dri-FIT ReLuxe Boxer Briefs", "Mack Weldon AIRKNIT Briefs"],
    },
    {
        "id": 10,
        "title": "Nike Dri-FIT ReLuxe Boxer Briefs",
        "image": "https://static.nike.com/a/images/t_PDP_1728_v1/f_auto,q_auto:eco/20adc876-c59c-40a0-b0b1-525d2a05dc58/DRI+FIT+RELUXE.png",
        "description": "Premium extra-soft fabric for superior closeness and stretch. Dri-FIT technology keeps you cool and dry. Horizontal fly offers convenient access. Fla seems that feel smooth against your skin.",
        "price": "$30.00",
        "rating": 4.8,
        "likes": 0,
        "sizes": ["S", "M", "L", "XL"],
        "similar_items": ["Under Armour Performance Cotton Boxerjock", "Mack Weldon AIRKNIT Briefs"],
    },
    {
        "id": 11,
        "title": "Mack Weldon AIRKNIT Briefs",
        "image": "https://cdn.shopify.com/s/files/1/0078/6825/2273/files/Airknitx_Perf_Brief_THUMBNAIL_03_93152732-e62e-466a-96bb-7d7b4a1e2bd6.jpg?v=1738184913&width=900",
        "description": "Unique design that targets extra airflow. Moisture-wicking and odor-fighting. Supportive flyless puch. No-roll waistband. Performance-ready from workdays to workouts.",
        "price": "$30.00",
        "rating": 4.9,
        "likes": 0,
        "sizes": ["S", "M", "L"],
        "similar_items": ["Nike Dri-FIT ReLuxe Boxer Briefs", "Under Armour Performance Cotton Boxerjock"],
    },
    {
        "id": 12,
        "title": "Calvin Klein Modal Boxer Briefs",
        "image": "https://calvinklein.scene7.com/is/image/CalvinKlein/61904198_610_alternate3?wid=1728&qlt=80%2C0&resMode=sharp2&op_usm=0.9%2C1.0%2C8%2C0&iccEmbed=0&fmt=webp",
        "description": "Designer boxer brief made with ultra soft modal fabric. Stretch blend for breathable enhanced comfort. Moisture wicking finish. Supportive contoured pouch.",
        "price": "$28.00",
        "rating": 4.9,
        "likes": 0,
        "sizes": ["S", "M", "L", "XL"],
        "similar_items": ["Nike Dri-Fit Boxer Briefs", "Under Armour Performance Boxer Briefs"],
    },
]

@app.route('/')
def index():
    return render_template('homepage.html', popular_items=sorted(underwear_items, key=lambda x: x['likes'], reverse=True)[:3])

@app.route('/api/popular-items')
def get_popular_items():
    return jsonify(sorted(underwear_items, key=lambda x: x['likes'], reverse=True)[:3])

@app.route('/search')
def search():
    query = request.args.get('q', '').strip().lower()
    if not query:
        return render_template('search.html', search_query=query, results=[])

    # Filter items based on title, description, rating, or price
    filtered_items = []
    for item in underwear_items:
        if (
            query in item['title'].lower() or
            query in item['description'].lower() or
            query in str(item['sizes']).lower() or
            query in item['price'].lower()
        ):
            filtered_items.append(item)

    return render_template('search.html', search_query=query, results=filtered_items)


@app.route('/view/<int:item_id>')
def view_item(item_id):
    item = next((item for item in underwear_items if item["id"] == item_id), None)
    if item:
        return render_template('view.html', item=item)
    else:
        return "Item not found", 404

@app.route('/like/<int:item_id>', methods=['POST'])
def like_item(item_id):
    if 'liked_items' not in session:
        session['liked_items'] = []

    if item_id not in session['liked_items']:
        session['liked_items'].append(item_id)

        for item in underwear_items:
            if item['id'] == item_id:
                item['likes'] += 1
                session.modified = True  # Inform Flask that the session has been modified
                return jsonify({"success": True, "likes": item['likes']})
        return jsonify({"success": False, "error": "Item not found"})
    else:
         return jsonify({"success": False, "error": "Item already liked"})

@app.route('/mylikes')
def my_likes():
    liked_item_ids = session.get('liked_items', [])
    liked_items = [item for item in underwear_items if item['id'] in liked_item_ids]
    return render_template('likes.html', results=liked_items)

@app.route('/unlike/<int:item_id>', methods=['POST'])
def unlike_item(item_id):
    if 'liked_items' in session:
        if item_id in session['liked_items']:
            session['liked_items'].remove(item_id)
            session.modified = True  # Inform Flask that the session has been modified

            # Decrement the like count for the item
            for item in underwear_items:
                if item['id'] == item_id:
                    item['likes'] = max(0, item['likes'] - 1)  # Ensure likes don't go below 0
                    break

    return redirect('/mylikes')


if __name__ == '__main__':
    app.run(debug=True)
