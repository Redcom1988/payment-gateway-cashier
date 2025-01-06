INSERT INTO employees (username, contact_num, address, password, role) 
VALUES 
    ('admin', '1234567890', 'tangerang selatan', 'admin', 'admin'), 
    ('ramayasa', '1234567890', 'jimbaran', 'qwerty', 'employee'), 
    ('monk', '1234567890', 'denpasar', '12345', 'employee'),
    ('ariep', '1234567890', 'buleleng', 'abcde', 'employee');

INSERT INTO products (product_name, product_cat, product_subcat, cost_price, vendor_stock, vendor)
VALUES
    -- Dairy Products from Major Suppliers
    ('Kraft Cheddar Cheese Slices', 'Fridge', 'Dairy', 100.00, 233, 'Kraft Foods'),
    ('Premium Greek Yogurt', 'Fridge', 'Dairy', 65.50, 150, 'Chobani'),
    ('Organic Whole Milk 1L', 'Fridge', 'Dairy', 45.75, 180, 'Organic Valley'),
    ('Natural Butter Block', 'Fridge', 'Dairy', 85.25, 120, 'Land O Lakes'),
    ('Fresh Mozzarella Ball', 'Fridge', 'Dairy', 72.50, 90, 'BelGioioso'),
    ('Probiotic Yogurt Drink', 'Fridge', 'Dairy', 38.99, 200, 'Yakult'),

    -- Snacks from Various Manufacturers
    ('Premium Mixed Nuts', 'Snacks', 'Nuts', 180.50, 100, 'Planters'),
    ('Classic Potato Chips', 'Snacks', 'Chips', 35.25, 250, 'Lays'),
    ('Dark Chocolate Bar', 'Snacks', 'Chocolate', 55.00, 175, 'Lindt'),
    ('Whole Grain Crackers', 'Snacks', 'Crackers', 42.75, 150, 'Nabisco'),
    ('Trail Mix Supreme', 'Snacks', 'Nuts', 95.50, 120, 'Nature Valley'),
    ('Rice Crackers Asian Style', 'Snacks', 'Crackers', 28.99, 200, 'Rice Company'),

    -- Beverages from Major Brands
    ('Cold Brew Coffee 1L', 'Beverages', 'Coffee', 75.50, 100, 'Starbucks'),
    ('Natural Orange Juice', 'Beverages', 'Juice', 45.25, 150, 'Tropicana'),
    ('Sparkling Mineral Water', 'Beverages', 'Water', 25.75, 300, 'San Pellegrino'),
    ('Green Tea Bags 100pk', 'Beverages', 'Tea', 65.00, 120, 'Twinings'),
    ('Premium Cola 2L', 'Beverages', 'Soft Drinks', 35.50, 200, 'Coca-Cola'),
    ('Energy Drink 250ml', 'Beverages', 'Energy Drinks', 42.99, 180, 'Red Bull'),

    -- Dry Goods from Various Suppliers
    ('Jasmine Rice 5kg', 'Dry', 'Grains', 125.50, 100, 'Asian Basics'),
    ('Organic Pasta', 'Dry', 'Pasta', 38.75, 200, 'Barilla'),
    ('Premium Cereal', 'Dry', 'Breakfast', 72.25, 150, 'Kelloggs'),
    ('All-Purpose Flour', 'Dry', 'Baking', 45.50, 180, 'Gold Medal'),
    ('Organic Quinoa', 'Dry', 'Grains', 85.99, 90, 'Bobs Red Mill'),
    ('Black Peppercorns', 'Dry', 'Spices', 55.25, 120, 'McCormick'),

    -- Fresh Produce from Local and International Suppliers
    ('Organic Bananas', 'Fresh', 'Fruits', 35.50, 200, 'Dole'),
    ('Premium Tomatoes', 'Fresh', 'Vegetables', 42.75, 150, 'Nature Fresh'),
    ('Baby Spinach', 'Fresh', 'Vegetables', 28.99, 100, 'Earthbound Farm'),
    ('Red Apples', 'Fresh', 'Fruits', 55.50, 180, 'Washington Apples'),
    ('Organic Carrots', 'Fresh', 'Vegetables', 32.25, 160, 'Organic Valley'),
    ('Fresh Strawberries', 'Fresh', 'Fruits', 65.99, 90, 'Driscolls'),

    -- Frozen Foods from Major Brands
    ('Premium Ice Cream', 'Frozen', 'Desserts', 85.50, 100, 'Häagen-Dazs'),
    ('Frozen Mixed Vegetables', 'Frozen', 'Vegetables', 45.25, 150, 'Birds Eye'),
    ('Frozen Pizza', 'Frozen', 'Ready Meals', 75.99, 120, 'DiGiorno'),
    ('Ice Cream Sandwiches', 'Frozen', 'Desserts', 62.50, 130, 'Blue Bell'),
    ('Frozen Chicken Breast', 'Frozen', 'Poultry', 95.75, 100, 'Tyson'),
    ('Premium Fish Fillets', 'Frozen', 'Seafood', 125.99, 80, 'Gortons'),

    -- Condiments from Various Manufacturers
    ('Extra Virgin Olive Oil', 'Condiments', 'Oils', 150.50, 100, 'Bertolli'),
    ('Premium Soy Sauce', 'Condiments', 'Sauces', 45.75, 150, 'Kikkoman'),
    ('Dijon Mustard', 'Condiments', 'Sauces', 35.99, 120, 'Grey Poupon'),
    ('Hot Sauce', 'Condiments', 'Sauces', 28.50, 200, 'Tabasco'),
    ('Mayonnaise', 'Condiments', 'Sauces', 42.25, 150, 'Hellmanns'),
    ('BBQ Sauce', 'Condiments', 'Sauces', 38.99, 180, 'Sweet Baby Rays'),

    -- International Foods
    ('Japanese Ramen', 'Dry', 'Pasta', 32.50, 250, 'Nissin'),
    ('Thai Curry Paste', 'Condiments', 'Sauces', 45.75, 100, 'Thai Kitchen'),
    ('Indian Basmati Rice', 'Dry', 'Grains', 85.99, 120, 'Tilda'),
    ('Mexican Salsa', 'Condiments', 'Sauces', 38.50, 150, 'Old El Paso'),
    ('Italian Pesto', 'Condiments', 'Sauces', 65.25, 90, 'Barilla'),
    ('Korean Kimchi', 'Fridge', 'Vegetables', 55.99, 80, 'Seoul Kitchen'),

    -- Organic and Health Foods
    ('Organic Honey', 'Condiments', 'Sweeteners', 95.50, 100, 'Natures Way'),
    ('Almond Milk', 'Fridge', 'Dairy Alternatives', 45.75, 150, 'Blue Diamond'),
    ('Coconut Water', 'Beverages', 'Health Drinks', 38.99, 180, 'Vita Coco'),
    ('Protein Bars', 'Snacks', 'Health Foods', 72.50, 200, 'Quest'),
    ('Chia Seeds', 'Dry', 'Superfoods', 65.25, 120, 'Bobs Red Mill'),
    ('Kombucha', 'Beverages', 'Health Drinks', 55.99, 90, 'GTs Living Foods');