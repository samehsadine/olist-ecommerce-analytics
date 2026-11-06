
-- =============================================
-- GOLD LAYER - OLIST E-COMMERCE ANALYTICS
-- Monthly orders, growth and sales
-- =============================================


-- 1. Create monthly orders view
CREATE OR ALTER VIEW gold.MonthlyOrders
AS
SELECT
    YEAR(order_purchase_timestamp) AS OrderYear,
    MONTH(order_purchase_timestamp) AS OrderMonth,
    COUNT(*) AS TotalOrders
FROM silver.Orders
WHERE order_purchase_timestamp IS NOT NULL
GROUP BY
    YEAR(order_purchase_timestamp),
    MONTH(order_purchase_timestamp);

GO


-- 2. Create monthly order growth view
CREATE OR ALTER VIEW gold.MonthlyOrderGrowth
AS
WITH MonthlyOrderEvolution AS (
    SELECT
        OrderYear,
        OrderMonth,
        TotalOrders,

        LAG(TotalOrders) OVER (
            ORDER BY OrderYear, OrderMonth
        ) AS PreviousMonthOrders,

        LAG(OrderYear * 12 + OrderMonth) OVER (
            ORDER BY OrderYear, OrderMonth
        ) AS PreviousPeriod

    FROM gold.MonthlyOrders
)

SELECT
    OrderYear,
    OrderMonth,
    TotalOrders,

    -- Show previous orders only for consecutive months
    CASE
        WHEN OrderYear * 12 + OrderMonth - PreviousPeriod = 1
        THEN PreviousMonthOrders
        ELSE NULL
    END AS PreviousMonthOrders,

    -- Calculate monthly order growth percentage
    CASE
        WHEN OrderYear * 12 + OrderMonth - PreviousPeriod = 1
        THEN CAST(
            100.0 * (TotalOrders - PreviousMonthOrders)
            / NULLIF(PreviousMonthOrders, 0)
            AS DECIMAL(10,2)
        )
        ELSE NULL
    END AS MonthlyGrowthPct

FROM MonthlyOrderEvolution;

GO

-- 3. Create monthly sales and delivered order metrics
CREATE OR ALTER VIEW gold.MonthlySales
AS
SELECT
    YEAR(o.order_purchase_timestamp) AS OrderYear,
    MONTH(o.order_purchase_timestamp) AS OrderMonth,

    -- Count all orders with items
    COUNT(DISTINCT o.order_id) AS TotalOrders,

    -- Calculate total product value
    CAST(SUM(oi.price) AS DECIMAL(18,2)) AS ProductRevenue,

    -- Calculate total freight value
    CAST(SUM(oi.freight_value) AS DECIMAL(18,2)) AS FreightRevenue,

    -- Calculate total order value
    CAST(
        SUM(oi.price + oi.freight_value)
        AS DECIMAL(18,2)
    ) AS TotalOrderValue,

    -- Calculate average order value including freight
    CAST(
        SUM(oi.price + oi.freight_value)
        / NULLIF(COUNT(DISTINCT o.order_id), 0)
        AS DECIMAL(18,2)
    ) AS AverageOrderValue,

    -- Count delivered orders
    COUNT(DISTINCT CASE
        WHEN o.order_status = 'delivered'
        THEN o.order_id
    END) AS DeliveredOrders,

    -- Calculate delivered product value
    CAST(
        SUM(CASE
            WHEN o.order_status = 'delivered'
            THEN oi.price
            ELSE 0
        END)
        AS DECIMAL(18,2)
    ) AS DeliveredProductValue,

    -- Calculate delivered freight value
    CAST(
        SUM(CASE
            WHEN o.order_status = 'delivered'
            THEN oi.freight_value
            ELSE 0
        END)
        AS DECIMAL(18,2)
    ) AS DeliveredFreightValue,

    -- Calculate delivered total value
    CAST(
        SUM(CASE
            WHEN o.order_status = 'delivered'
            THEN oi.price + oi.freight_value
            ELSE 0
        END)
        AS DECIMAL(18,2)
    ) AS DeliveredTotalValue,
    CAST(
    100.0 * COUNT(DISTINCT CASE
        WHEN o.order_status = 'delivered'
        THEN o.order_id
    END)
    / NULLIF(COUNT(DISTINCT o.order_id), 0)
    AS DECIMAL(10,2)
    ) AS DeliveryRatePct
FROM silver.Orders AS o

INNER JOIN silver.OrdersItems AS oi
    ON o.order_id = oi.order_id

WHERE o.order_purchase_timestamp IS NOT NULL

GROUP BY
    YEAR(o.order_purchase_timestamp),
    MONTH(o.order_purchase_timestamp);

GO

-- 4. Create delivery performance KPIs
CREATE OR ALTER VIEW gold.DeliveryPerformance
AS
WITH DeliveryStatus AS (
    SELECT
        CASE
            WHEN order_delivered_customer_date >
                 order_estimated_delivery_date
            THEN 1
            ELSE 0
        END AS IsLate
    FROM silver.Orders
    WHERE order_status = 'delivered'
      AND order_delivered_customer_date IS NOT NULL
      AND order_estimated_delivery_date IS NOT NULL
)
SELECT
    COUNT(*) AS TotalDeliveredOrders,
    SUM(IsLate) AS LateOrders,
    COUNT(*) - SUM(IsLate) AS OnTimeOrders,

    -- Calculate late delivery percentage
    CAST(
        100.0 * SUM(IsLate) / NULLIF(COUNT(*), 0)
        AS DECIMAL(10,2)
    ) AS LateDeliveryRatePct,

    -- Calculate on-time delivery percentage
    CAST(
        100.0 * (COUNT(*) - SUM(IsLate)) / NULLIF(COUNT(*), 0)
        AS DECIMAL(10,2)
    ) AS OnTimeDeliveryRatePct

FROM DeliveryStatus;

GO

-- 5. Create monthly delivery performance view
CREATE OR ALTER VIEW gold.MonthlyDeliveryPerformance
AS
SELECT
    YEAR(order_purchase_timestamp) AS OrderYear,
    MONTH(order_purchase_timestamp) AS OrderMonth,

    -- Count delivered orders
    COUNT(*) AS TotalDeliveredOrders,

    -- Count late deliveries
    SUM(CASE
        WHEN order_delivered_customer_date >
             order_estimated_delivery_date
        THEN 1
        ELSE 0
    END) AS LateOrders,

    -- Calculate late delivery percentage
    CAST(
        100.0 * SUM(CASE
            WHEN order_delivered_customer_date >
                 order_estimated_delivery_date
            THEN 1
            ELSE 0
        END)
        / NULLIF(COUNT(*), 0)
        AS DECIMAL(10,2)
    ) AS LateDeliveryRatePct

FROM silver.Orders

WHERE order_status = 'delivered'
  AND order_purchase_timestamp IS NOT NULL
  AND order_delivered_customer_date IS NOT NULL
  AND order_estimated_delivery_date IS NOT NULL

GROUP BY
    YEAR(order_purchase_timestamp),
    MONTH(order_purchase_timestamp);

GO

-- 6. Create customer satisfaction KPIs
CREATE OR ALTER VIEW gold.CustomerSatisfaction
AS
SELECT
    COUNT(*) AS TotalReviews,

    -- Calculate average review score
    CAST(
        AVG(CAST(review_score AS DECIMAL(10,2)))
        AS DECIMAL(10,2)
    ) AS AverageReviewScore,

    -- Count positive reviews
    SUM(CASE
        WHEN review_score >= 4 THEN 1
        ELSE 0
    END) AS PositiveReviews,

    -- Count negative reviews
    SUM(CASE
        WHEN review_score <= 2 THEN 1
        ELSE 0
    END) AS NegativeReviews,

    -- Calculate positive review percentage
    CAST(
        100.0 * SUM(CASE
            WHEN review_score >= 4 THEN 1
            ELSE 0
        END) / NULLIF(COUNT(*), 0)
        AS DECIMAL(10,2)
    ) AS PositiveReviewRatePct

FROM silver.OrderReviews;

GO

-- 7. Create delivery satisfaction analysis
CREATE OR ALTER VIEW gold.DeliverySatisfaction
AS
WITH OrderReviewScores AS (
    -- Calculate one average review score per order
    SELECT
        order_id,
        AVG(CAST(review_score AS DECIMAL(10,2))) AS AverageOrderReviewScore
    FROM silver.OrderReviews
    GROUP BY order_id
)
SELECT
    CASE
        WHEN o.order_delivered_customer_date >
             o.order_estimated_delivery_date
        THEN 'Late Delivery'
        ELSE 'On-time Delivery'
    END AS DeliveryStatus,

    COUNT(*) AS TotalOrders,

    -- Calculate average customer satisfaction
    CAST(
        AVG(r.AverageOrderReviewScore)
        AS DECIMAL(10,2)
    ) AS AverageReviewScore,

    -- Count orders with negative reviews
    SUM(CASE
        WHEN r.AverageOrderReviewScore < 3
        THEN 1
        ELSE 0
    END) AS NegativeReviewOrders,

    -- Calculate negative review percentage
    CAST(
        100.0 * SUM(CASE
            WHEN r.AverageOrderReviewScore < 3
            THEN 1
            ELSE 0
        END)
        / NULLIF(COUNT(*), 0)
        AS DECIMAL(10,2)
    ) AS NegativeReviewRatePct

FROM silver.Orders AS o

INNER JOIN OrderReviewScores AS r
    ON o.order_id = r.order_id

WHERE o.order_status = 'delivered'
  AND o.order_delivered_customer_date IS NOT NULL
  AND o.order_estimated_delivery_date IS NOT NULL

GROUP BY
    CASE
        WHEN o.order_delivered_customer_date >
             o.order_estimated_delivery_date
        THEN 'Late Delivery'
        ELSE 'On-time Delivery'
    END;

GO

-- 8. Create product category sales analysis
CREATE OR ALTER VIEW gold.ProductCategorySales
AS
SELECT
    COALESCE(
        t.product_category_name_english,
        p.product_category_name,
        'Unknown'
    ) AS ProductCategory,

    -- Count sold items
    COUNT(*) AS TotalItemsSold,

    -- Count distinct orders
    COUNT(DISTINCT oi.order_id) AS TotalOrders,

    -- Calculate product revenue
    CAST(
        SUM(oi.price)
        AS DECIMAL(18,2)
    ) AS ProductRevenue,

    -- Calculate average item price
    CAST(
        AVG(CAST(oi.price AS DECIMAL(18,2)))
        AS DECIMAL(18,2)
    ) AS AverageItemPrice

FROM silver.OrdersItems AS oi

INNER JOIN silver.Products AS p
    ON oi.product_id = p.product_id

LEFT JOIN silver.CategoryTranslateName AS t
    ON p.product_category_name = t.product_category_name

GROUP BY
    COALESCE(
        t.product_category_name_english,
        p.product_category_name,
        'Unknown'
    );

GO

-- 9. Create geographic sales analysis by customer state
CREATE OR ALTER VIEW gold.SalesByState
AS
SELECT
    c.customer_state AS CustomerState,

    -- Count distinct orders
    COUNT(DISTINCT o.order_id) AS TotalOrders,

    -- Calculate product value
    CAST(
        SUM(oi.price)
        AS DECIMAL(18,2)
    ) AS ProductRevenue,

    -- Calculate freight value
    CAST(
        SUM(oi.freight_value)
        AS DECIMAL(18,2)
    ) AS FreightRevenue,

    -- Calculate total order value
    CAST(
        SUM(oi.price + oi.freight_value)
        AS DECIMAL(18,2)
    ) AS TotalOrderValue

FROM silver.Orders AS o

INNER JOIN silver.Customers AS c
    ON o.customer_id = c.customer_id

INNER JOIN silver.OrdersItems AS oi
    ON o.order_id = oi.order_id

GROUP BY
    c.customer_state;

GO

-- 10. Create geographic sales analysis by customer city
CREATE OR ALTER VIEW gold.SalesByCity
AS
SELECT
    c.customer_city AS CustomerCity,
    c.customer_state AS CustomerState,

    -- Count distinct orders
    COUNT(DISTINCT o.order_id) AS TotalOrders,

    -- Calculate product value
    CAST(
        SUM(oi.price)
        AS DECIMAL(18,2)
    ) AS ProductRevenue,

    -- Calculate freight value
    CAST(
        SUM(oi.freight_value)
        AS DECIMAL(18,2)
    ) AS FreightRevenue,

    -- Calculate total order value
    CAST(
        SUM(oi.price + oi.freight_value)
        AS DECIMAL(18,2)
    ) AS TotalOrderValue

FROM silver.Orders AS o

INNER JOIN silver.Customers AS c
    ON o.customer_id = c.customer_id

INNER JOIN silver.OrdersItems AS oi
    ON o.order_id = oi.order_id

GROUP BY
    c.customer_city,
    c.customer_state;

GO

-- 11. Create payment methods analysis
CREATE OR ALTER VIEW gold.PaymentMethods
AS
SELECT
    payment_type AS PaymentMethod,

    -- Count payment records
    COUNT(*) AS TotalPayments,

    -- Count distinct orders
    COUNT(DISTINCT order_id) AS TotalOrders,

    -- Calculate total payment value
    CAST(
        SUM(payment_value)
        AS DECIMAL(18,2)
    ) AS TotalPaymentValue,

    -- Calculate payment method percentage
    CAST(
        100.0 * COUNT(*) / NULLIF(SUM(COUNT(*)) OVER (), 0)
        AS DECIMAL(10,2)
    ) AS PaymentPercentage

FROM silver.OrdersPayments

GROUP BY payment_type;

GO

-- 12. Create payment installments analysis
CREATE OR ALTER VIEW gold.PaymentInstallments
AS
SELECT
    payment_installments AS InstallmentCount,

    -- Count payment records
    COUNT(*) AS TotalPayments,

    -- Count distinct orders
    COUNT(DISTINCT order_id) AS TotalOrders,

    -- Calculate total payment value
    CAST(
        SUM(payment_value)
        AS DECIMAL(18,2)
    ) AS TotalPaymentValue,

    -- Calculate payment percentage
    CAST(
        100.0 * COUNT(*)
        / NULLIF(SUM(COUNT(*)) OVER (), 0)
        AS DECIMAL(10,2)
    ) AS PaymentPercentage

FROM silver.OrdersPayments

GROUP BY payment_installments;



GO

-- 13. Create customer repeat purchase analysis
CREATE OR ALTER VIEW gold.CustomerRetention
AS
WITH CustomerOrders AS (
    -- Count distinct orders for each unique customer
    SELECT
        c.customer_unique_id AS CustomerUniqueId,
        COUNT(DISTINCT o.order_id) AS TotalOrders
    FROM silver.Customers AS c
    INNER JOIN silver.Orders AS o
        ON c.customer_id = o.customer_id
    WHERE c.customer_unique_id IS NOT NULL
    GROUP BY c.customer_unique_id
)
SELECT
    COUNT(*) AS TotalCustomers,

    -- Count customers with one order
    SUM(CASE
        WHEN TotalOrders = 1 THEN 1
        ELSE 0
    END) AS OneTimeCustomers,

    -- Count customers with multiple orders
    SUM(CASE
        WHEN TotalOrders > 1 THEN 1
        ELSE 0
    END) AS RepeatCustomers,

    -- Calculate repeat customer percentage
    CAST(
        100.0 * SUM(CASE
            WHEN TotalOrders > 1 THEN 1
            ELSE 0
        END) / NULLIF(COUNT(*), 0)
        AS DECIMAL(10,2)
    ) AS RepeatCustomerRatePct

FROM CustomerOrders;