-- +goose Up
CREATE TYPE order_status AS ENUM (
    'assigned',
    'in-progress',
    'completed',
    'cancelled',
    'unassigned'
);

CREATE TABLE driver_orders (
    id UUID PRIMARY KEY,
    driver_id UUID,
    order_id UUID NOT NULL,

    restaurant_id   UUID NOT NULL,
    restaurant_name VARCHAR(100) NOT NULL,
    restaurant_addr TEXT NOT NULL,
    restaurant_lat  DECIMAL(9, 6) NOT NULL,
    restaurant_long DECIMAL(9, 6) NOT NULL,

    customer_id UUID    NOT NULL,
    customer_addr       TEXT NOT NULL,
    customer_name       VARCHAR(100) NOT NULL,
    customer_phone      VARCHAR(15) NOT NULL,
    customer_lat        DECIMAL(9, 6) NOT NULL,
    customer_long       DECIMAL(9, 6) NOT NULL,

    status              order_status NOT NULL DEFAULT 'unassigned',
    delivery_distance   FLOAT NOT NULL,
    earning             FLOAT NOT NULL,
    tip                 INTEGER NOT NULL DEFAULT 0,
    is_cash_payment     BOOLEAN NOT NULL DEFAULT FALSE,
    cash_amount         FLOAT NOT NULL DEFAULT 0,

    created_at          TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    assigned_at         TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at          TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    deleted_at          TIMESTAMPTZ DEFAULT NULL,
    is_deleted          BOOLEAN NOT NULL DEFAULT FALSE,

    CONSTRAINT fk_driver_id FOREIGN KEY (driver_id) REFERENCES drivers (id)
);


-- +goose Down
DROP TABLE driver_orders;
DROP TYPE order_status;