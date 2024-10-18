# Inventory Management API

This is a simple **Inventory Management API** built using Python and SQLite to manage items and categories in a retail shop's inventory. It allows unauthenticated users to view categories and items, while authenticated users can add, update, and delete items.

## Project Overview

The API supports the following operations:

- **GET**: Retrieve all categories or a list of items (or an individual item by its ID).
- **POST**: Add a new category or item to the inventory.
- **PUT**: Update an existing item by its ID.
- **DELETE**: Remove an item by its ID.

## Prerequisites and Dependencies

1. **Python 3.7+**
2. **SQLite3**: This API uses SQLite as the database, which typically comes pre-installed with Python.
3. **`requests` Python library**: Used for testing the API endpoints.
4. **`unittest` Python library**: Standard library for running unit tests.
5. **POSTMAN**

## Step-by-Step Setup

1. **Set Up the Database**:
   Initialize the SQLite database by running:

   ```
   python models.py
   ```

   This will create the `inventory.db` file and set up the tables required for categories and items.

2. **Run the API**:
   Start the server by running:

   ```
   python main.py
   ```

   The server will start on `localhost:8000`. You can now interact with the API.

## How to Run the Application

Once the API is running, you can access it at the following endpoints using tools like **Postman**.

### Endpoints

1. **GET /categories**
   - **Description**: Retrieve all categories.
   - **Response**: JSON list of categories.
   - **Example**:
     ```
    GET http://localhost:8000/categories
     ```

2. **GET /items** or **GET /items/{id}**
   - **Description**: Retrieve all items or a specific item by ID.
   - **Example**:
     ```
    GET http://localhost:8000/items/1
     ```

3. **POST /categories**
   - **Description**: Add a new category.
   - **Request Body**:
     ```json
     {
       "name": "New Category"
     }
     ```

4. **POST /items**
   - **Description**: Add a new item to the inventory.
   - **Request Body**:
     ```json
     {
       "category_id": 1,
       "name": "Item Name",
       "description": "Item Description",
       "price": 10.99
     }
     ```

5. **PUT /items/{id}**
   - **Description**: Update an existing item by its ID.
   - **Request Body**:
     ```json
     {
       "category_id": 1,
       "name": "Updated Name",
       "description": "Updated Description",
       "price": 15.99
     }
     ```

6. **DELETE /items/{id}**
   - **Description**: Delete an item by its ID.
   - **Example**:
     ```
    DELETE http://localhost:8000/items/1
     ```


## How to Run the Tests

Unit tests are written to test the API functionality using the `unittest` library and mock HTTP requests using `requests`.

### Running the Tests

To run the unit tests, simply run the following command in the project root:

```
python -m unittest tests/test_api.py
```

This will execute the test cases for both successful and failing API calls. If everything is set up correctly, you should see the results of the test cases.

### Test Structure

The tests include:
1. **Positive Tests**: Check valid scenarios where API requests should return the expected results.
2. **Negative Tests**: Check how the API behaves with invalid inputs or incorrect URLs.

Example test cases include:
- Checking if valid GET requests return status `200 OK`.
- Checking if requests with invalid item IDs return `404 Not Found`.

## Potential Error Messages

- **400 Bad Request**: Invalid data provided in the request body or missing headers.
- **404 Not Found**: The requested resource (category or item) does not exist.
- **409 Conflict**: Duplicate entry or integrity constraint violation (e.g., item or category already exists).
- **500 Internal Server Error**: Server encountered an error while processing the request.


## Debuging Error