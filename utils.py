def validate_item_data(data):
    required_fields = ['category_id', 'name', 'price']
    for field in required_fields:
        if field not in data:
            return False
    return isinstance(data['price'], (float, int)) and isinstance(data['category_id'], int)

def validate_category_data(data):
    return 'name' in data and isinstance(data['name'], str)
