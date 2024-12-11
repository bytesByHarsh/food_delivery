-- name: CreateOrder :one
INSERT INTO driver_orders(id, driver_id, order_id,
                         restaurant_id, restaurant_name, restaurant_addr, restaurant_lat , restaurant_long,
                         customer_id, customer_addr, customer_name, customer_phone, customer_lat, customer_long,
                         status, delivery_distance, earning, tip, is_cash_payment, cash_amount,
                         created_at, assigned_at, updated_at, deleted_at, is_deleted)
VALUES ($1, $2, $3,
        $4, $5, $6, $7, $8,
        $9, $10, $11, $12, $13, $14,
        $15, $16, $17, $18, $19, $20,
        $21, $22, $23, $24, false)
RETURNING *;

-- name: GetOrderById :one
SELECT * from driver_orders WHERE id=$1 AND is_deleted = false;

-- name: GetOrderByOrderId :one
SELECT * from driver_orders WHERE order_id=$1 AND is_deleted = false;

-- name: GetOrderByDriverId :many
SELECT *
FROM
    driver_orders
WHERE
    driver_id=$1 AND is_deleted = false
ORDER BY
    updated_at DESC
LIMIT $1 OFFSET $2;

-- name: GetOrderByCustomerId :many
SELECT *
FROM
    driver_orders
WHERE
    customer_id=$1 AND is_deleted = false
ORDER BY
    updated_at DESC
LIMIT $1 OFFSET $2;

-- name: GetAllUnassignedOrder :many
SELECT *
FROM
    driver_orders
WHERE is_deleted = false AND status = 'unassigned'
ORDER BY
    updated_at DESC
LIMIT $1 OFFSET $2;

-- name: GetUnassignedOrderCount :one
SELECT COUNT(*) FROM driver_orders WHERE is_deleted=false AND status = 'unassigned';

-- name: UpdateOrderDriver :exec
UPDATE driver_orders
SET driver_id=$2,
    updated_at=$3,
    assigned_at=$4,
    status="assigned"
WHERE id = $1 AND is_deleted=false
RETURNING *;

-- name: UpdateOrderStatus :exec
UPDATE driver_orders
SET status=$2,
    updated_at=$3
WHERE id = $1 AND is_deleted=false
RETURNING *;