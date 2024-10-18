import json
from http.server import BaseHTTPRequestHandler
from models import initialize_db
import sqlite3
from utils import validate_item_data, validate_category_data

initialize_db()

class MyHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/categories':
            self.handle_get_categories()
        elif self.path.startswith('/items'):
            item_id = self.path.split('/')[-1]
            if item_id.isdigit():
                self.handle_get_items(item_id)
            else:
                self.handle_get_items()
        else:
            self.send_response(404)
            self.end_headers()

    def do_POST(self):
        if self.path == '/categories':
            self.handle_post_category()
        elif self.path == '/items':
            self.handle_post_item()
        else:
            self.send_response(404)
            self.end_headers()
            
    def do_PUT(self):
        if self.path.startswith('/items/'):
            self.handle_put_item()
        else:
            self.send_response(404)
            self.end_headers()        
            
    def do_DELETE(self):
        if self.path.startswith('/items/'):
            self.handle_delete_item()
        else:
            self.send_response(404)
            self.end_headers()
            

    def handle_get_categories(self):
        conn = sqlite3.connect('inventory.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM Category')
        categories = cursor.fetchall()
        conn.close()
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps([{'id': c[0], 'name': c[1]} for c in categories]).encode('utf-8'))

    def handle_get_items(self, item_id=None):
        conn = sqlite3.connect('inventory.db')
        cursor = conn.cursor()

        if item_id:
            cursor.execute('SELECT * FROM Item WHERE id = ?', (item_id,))
            item = cursor.fetchone()

            if item is None:
                self.send_response(404)
                self.end_headers()
                self.wfile.write(b"Item not found")
            else:
                self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            item_details = {
                'id': item[0],
                'category_id': item[1],
                'name': item[2],
                'description': item[3],
                'price': item[4],
                'created_at': item[5]
            }
            self.wfile.write(json.dumps(item_details).encode('utf-8'))
        else:
            cursor.execute('SELECT * FROM Item')
            items = cursor.fetchall()
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps([{
                'id': i[0],
                'category_id': i[1],
                'name': i[2],
                'description': i[3],
                'price': i[4],
                'created_at': i[5]
            } for i in items]).encode('utf-8'))

        conn.close()

    def handle_post_category(self):
        length = self.headers.get('Content-Length')
        
        # If Content-Length is not provided or 0, return an error
        if not length:
            self.send_response(400)
            self.end_headers()
            self.wfile.write(b"Content-Length header is missing or empty")
            return
        
        # Try to read the body based on the length
        try:
            length = int(length)
            post_data = self.rfile.read(length)
            
            # Check if data is empty
            if not post_data:
                self.send_response(400)
                self.end_headers()
                self.wfile.write(b"Request body is empty")
                return

            # Decode and parse the JSON
            category_data = json.loads(post_data.decode('utf-8'))
            
        except (ValueError, json.JSONDecodeError):
            self.send_response(400)
            self.end_headers()
            self.wfile.write(b"Invalid JSON format")
            return

        # Validate the parsed category data
        if not validate_category_data(category_data):
            self.send_response(400)
            self.end_headers()
            self.wfile.write(b"Invalid category data")
            return

        # Proceed with inserting the category into the database
        conn = sqlite3.connect('inventory.db')
        cursor = conn.cursor()
        try:
            cursor.execute('INSERT INTO Category (name) VALUES (?)', (category_data['name'],))
            conn.commit()
            self.send_response(201)
            self.end_headers()
        except sqlite3.IntegrityError:
            self.send_response(409)
            self.end_headers()
            self.wfile.write(b"Category already exists")
        finally:
            conn.close()

    def handle_post_item(self):
        length = self.headers.get('Content-Length')

        if not length:
            self.send_response(400)
            self.end_headers()
            self.wfile.write(b"Content-Length header is missing or empty")
            return

        try:
            # Convert length to an integer and read the body based on the length
            length = int(length)
            post_data = self.rfile.read(length)

            # Check if data is empty
            if not post_data:
                self.send_response(400)
                self.end_headers()
                self.wfile.write(b"Request body is empty")
                return

            # Decode and parse the JSON
            item_data = json.loads(post_data.decode('utf-8'))

        except (ValueError, json.JSONDecodeError):
            self.send_response(400)
            self.end_headers()
            self.wfile.write(b"Invalid JSON format")
            return

        # Validate the parsed item data
        if not validate_item_data(item_data):
            self.send_response(400)
            self.end_headers()
            self.wfile.write(b"Invalid item data")
            return

        # Proceed with inserting the item into the database
        conn = sqlite3.connect('inventory.db')
        cursor = conn.cursor()
        try:
            cursor.execute('''INSERT INTO Item (category_id, name, description, price) VALUES (?, ?, ?, ?)''', 
                        (item_data['category_id'], item_data['name'], item_data['description'], item_data['price']))
            conn.commit()
            self.send_response(201)
            self.end_headers()
        except sqlite3.IntegrityError:
            self.send_response(409)
            self.end_headers()
            self.wfile.write(b"Item already exists or invalid category_id")
        finally:
            conn.close()

    def handle_put_item(self):
    # Extract the item ID from the URL
        item_id = self.path.split('/')[-1]  # Assuming the path is like /items/1

        # Check if item_id is valid (is it an integer?)
        if not item_id.isdigit():
            self.send_response(400)
            self.end_headers()
            self.wfile.write(b"Invalid item ID")
            return

        length = self.headers.get('Content-Length')

        if not length:
            self.send_response(400)
            self.end_headers()
            self.wfile.write(b"Content-Length header is missing or empty")
            return

        try:
            length = int(length)
            post_data = self.rfile.read(length)

            if not post_data:
                self.send_response(400)
                self.end_headers()
                self.wfile.write(b"Request body is empty")
                return

            item_data = json.loads(post_data.decode('utf-8'))

        except (ValueError, json.JSONDecodeError):
            self.send_response(400)
            self.end_headers()
            self.wfile.write(b"Invalid JSON format")
            return

        if not validate_item_data(item_data):
            self.send_response(400)
            self.end_headers()
            self.wfile.write(b"Invalid item data")
            return

        conn = sqlite3.connect('inventory.db')
        cursor = conn.cursor()
        try:
            cursor.execute('''UPDATE Item SET category_id = ?, name = ?, description = ?, price = ? WHERE id = ?''', 
                    (item_data['category_id'], item_data['name'], item_data['description'], item_data['price'], item_id))
            if cursor.rowcount == 0:
                self.send_response(404)  # Item not found
                self.end_headers()
                self.wfile.write(b"Item not found")
            else:
                conn.commit()
                self.send_response(200)  # Success
                self.end_headers()
        except sqlite3.IntegrityError:
            self.send_response(409)
            self.end_headers()
            self.wfile.write(b"Invalid category_id or item already exists")
        finally:
            conn.close()
            
    def handle_delete_item(self):
    # Extract the item ID from the URL
        item_id = self.path.split('/')[-1]

        # Check if item_id is valid
        if not item_id.isdigit():
            self.send_response(400)
            self.end_headers()
            self.wfile.write(b"Invalid item ID")
            return

        conn = sqlite3.connect('inventory.db')
        cursor = conn.cursor()
        try:
            cursor.execute('DELETE FROM Item WHERE id = ?', (item_id,))
            if cursor.rowcount == 0:
                self.send_response(404)  # Item not found
                self.end_headers()
                self.wfile.write(b"Item not found")
            else:
                conn.commit()
                self.send_response(204)  # No content, successful deletion
                self.end_headers()
        except sqlite3.Error as e:
            self.send_response(500)
            self.end_headers()
            self.wfile.write(b"Internal server error")
        finally:
            conn.close()