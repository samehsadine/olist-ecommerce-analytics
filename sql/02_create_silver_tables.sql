
-- Create the Silver schema if it does not exist
IF SCHEMA_ID('silver') IS NULL
BEGIN
    EXEC('CREATE SCHEMA silver');
END;

-- Table Orders
IF OBJECT_ID('silver.Orders', 'U') IS NULL
BEGIN
    CREATE TABLE silver.Orders
    (
        order_id VARCHAR(32) NOT NULL PRIMARY KEY,
        customer_id VARCHAR(32) NOT NULL,
        order_status VARCHAR(20),

        order_purchase_timestamp DATETIME2,
        order_approved_at DATETIME2,
        order_delivered_carrier_date DATETIME2,
        order_delivered_customer_date DATETIME2,
        order_estimated_delivery_date DATETIME2,

        anomalie_livraison BIT
    );
END;



-- Table Customers
IF OBJECT_ID('silver.Customers', 'U') IS NULL
BEGIN
    CREATE TABLE silver.Customers
    (
        customer_id VARCHAR(32) NOT NULL PRIMARY KEY,
        customer_unique_id VARCHAR(32) NOT NULL,
        customer_zip_code_prefix VARCHAR(5) NOT NULL,
        customer_city NVARCHAR(100) NOT NULL,
        customer_state CHAR(2) NOT NULL
    );
END;

-- Table Orders_items
IF OBJECT_ID('silver.OrdersItems', 'U') IS NULL
BEGIN
    CREATE TABLE silver.OrdersItems
    (
        order_id VARCHAR(32) NOT NULL,
        order_item_id INT NOT NULL,
        product_id VARCHAR(32) NOT NULL,
        seller_id NVARCHAR(32) NOT NULL,
        shipping_limit_date DATETIME2,
        price decimal(10,2),
        freight_value decimal(10,2),
        CONSTRAINT PK_OrdersItems 
            PRIMARY KEY (order_id, order_item_id)
    );
END;

-- Table Orders_payments
IF OBJECT_ID('silver.OrdersPayments', 'U') IS NULL
BEGIN
    CREATE TABLE silver.OrdersPayments
    (
        order_id VARCHAR(32) NOT NULL,
        payment_sequential INT NOT NULL,
        payment_type VARCHAR(32) NOT NULL,
        payment_installments INT NOT NULL,
        payment_value decimal(10,2),
        
        -- Anomaly flags
        anomalie_montant BIT NOT NULL,
        anomalie_versement BIT NOT NULL,
        anomalie_type_paiement BIT NOT NULL,

        CONSTRAINT PK_OrdersPayments 
            PRIMARY KEY (order_id, payment_sequential)
    );
END;

-- Table Sellers
IF OBJECT_ID('silver.Sellers', 'U') IS NULL
BEGIN
    CREATE TABLE silver.Sellers
    (
        seller_id VARCHAR(32) NOT NULL PRIMARY KEY,
        seller_zip_code_prefix VARCHAR(5) NOT NULL,
        seller_city VARCHAR(100) NOT NULL,
        seller_state VARCHAR(3) NOT NULL,

       

    );
END;

-- Table Sellers
IF OBJECT_ID('silver.Geolocation', 'U') IS NULL
BEGIN
    CREATE TABLE silver.Geolocation
    (
        geolocation_id INT IDENTITY(1,1) PRIMARY KEY,
        geolocation_zip_code_prefix VARCHAR(5) NOT NULL,
        geolocation_lat FLOAT NOT NULL,
        geolocation_lng FLOAT NOT NULL,
        geolocation_city VARCHAR(100) NOT NULL,
        geolocation_state VARCHAR(2) NOT NULL,

         anomalie_geolocation BIT NOT NULL,

    );
END;

-- Table Products
IF OBJECT_ID('silver.Products', 'U') IS NULL
BEGIN
    CREATE TABLE silver.Products
    (
        product_id VARCHAR(32) PRIMARY KEY,
        product_category_name VARCHAR(100) NULL,
        product_name_lenght INT NULL,
        product_description_lenght INT NULL,
        product_photos_qty INT NULL,
        product_weight_g Decimal (12,2) NULL,
        product_length_cm Decimal (10,2) NULL,
        product_height_cm Decimal (10,2) NULL,
        product_width_cm Decimal (10,2) NULL,

        anomalies_poids BIT NOT NULL,
        anomalies_categorie BIT NOT NULL,
    );
END;

-- Table CategoryTranslateName
IF OBJECT_ID('silver.CategoryTranslateName', 'U') IS NULL
BEGIN
    CREATE TABLE silver.CategoryTranslateName
    (
        category_translate_name_id INT IDENTITY(1,1) PRIMARY KEY,
        product_category_name VARCHAR(50) NULL UNIQUE,
        product_category_name_english VARCHAR(50) NULL
        
    );
END;
-- Table OrderReviews
IF OBJECT_ID('silver.OrderReviews', 'U') IS NULL
BEGIN
    CREATE TABLE silver.OrderReviews
    (
        review_id VARCHAR(32) NOT NULL,
        order_id VARCHAR(32) NOT NULL,
        review_score INT NOT NULL,
        review_comment_title NVARCHAR(MAX) NULL,
        review_comment_message NVARCHAR(MAX) NULL,
        review_creation_date DATETIME2 NOT NULL,
        review_answer_timestamp DATETIME2 NOT NULL,

        CONSTRAINT PK_OrderReviews
            PRIMARY KEY (review_id, order_id)
    );
END;