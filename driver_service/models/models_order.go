package models

import (
	"time"

	"github.com/bytesByHarsh/food_delivery/driver_service/internal/database"
	"github.com/google/uuid"
)

type CreateOrderReq struct {
	OrderID          uuid.UUID `json:"order_id" validate:"required"`
	RestaurantID     uuid.UUID `json:"restaurant_id" validate:"required"`
	RestaurantName   string    `json:"restaurant_name" validate:"required"`
	RestaurantAddr   string    `json:"restaurant_addr" validate:"required"`
	RestaurantLat    string    `json:"restaurant_lat" validate:"required"`
	RestaurantLong   string    `json:"restaurant_long" validate:"required"`
	CustomerID       uuid.UUID `json:"customer_id" validate:"required"`
	CustomerAddr     string    `json:"customer_addr" validate:"required"`
	CustomerName     string    `json:"customer_name" validate:"required"`
	CustomerPhone    string    `json:"customer_phone" validate:"required"`
	CustomerLat      string    `json:"customer_lat" validate:"required"`
	CustomerLong     string    `json:"customer_long" validate:"required"`
	DeliveryDistance float64   `json:"delivery_dist" validate:"required"`
	Earning          float64   `json:"earning" validate:"required"`
	Tip              int32     `json:"tip" validate:"required"`
	IsCashPayment    bool      `json:"is_cash_payment" validate:"required"`
	CashAmount       float64   `json:"cash_amount" validate:"required"`
}

type Order struct {
	Id               uuid.UUID            `json:"id"`
	DriverID         uuid.NullUUID        `json:"driver_id"`
	OrderID          uuid.UUID            `json:"order_id"`
	RestaurantID     uuid.UUID            `json:"restaurant_id"`
	RestaurantName   string               `json:"restaurant_name"`
	RestaurantAddr   string               `json:"restaurant_addr"`
	RestaurantLat    string               `json:"restaurant_lat"`
	RestaurantLong   string               `json:"restaurant_long"`
	CustomerID       uuid.UUID            `json:"customer_id"`
	CustomerAddr     string               `json:"customer_addr"`
	CustomerName     string               `json:"customer_name"`
	CustomerPhone    string               `json:"customer_phone"`
	CustomerLat      string               `json:"customer_lat"`
	CustomerLong     string               `json:"customer_long"`
	DeliveryDistance float64              `json:"delivery_dist"`
	Earning          float64              `json:"earning"`
	Tip              int32                `json:"tip"`
	IsCashPayment    bool                 `json:"is_cash_payment"`
	CashAmount       float64              `json:"cash_amount"`
	Status           database.OrderStatus `json:"status"`
	CreatedAt        time.Time            `json:"created_at"`
	AssignedAt       time.Time            `json:"assigned_at"`
	UpdatedAt        time.Time            `json:"updated_at"`
}

func ConvOrderToOrder(dbOrder database.DriverOrder) Order {
	return Order{
		Id:               dbOrder.ID,
		CreatedAt:        dbOrder.CreatedAt,
		UpdatedAt:        dbOrder.UpdatedAt,
		AssignedAt:       dbOrder.AssignedAt,
		DriverID:         dbOrder.DriverID,
		OrderID:          dbOrder.OrderID,
		RestaurantID:     dbOrder.RestaurantID,
		RestaurantName:   dbOrder.RestaurantName,
		RestaurantAddr:   dbOrder.RestaurantAddr,
		RestaurantLat:    dbOrder.RestaurantLat,
		RestaurantLong:   dbOrder.RestaurantLong,
		CustomerID:       dbOrder.CustomerID,
		CustomerAddr:     dbOrder.CustomerAddr,
		CustomerName:     dbOrder.CustomerName,
		CustomerPhone:    dbOrder.CustomerPhone,
		CustomerLat:      dbOrder.CustomerLat,
		CustomerLong:     dbOrder.CustomerLong,
		DeliveryDistance: dbOrder.DeliveryDistance,
		Earning:          dbOrder.Earning,
		Tip:              dbOrder.Tip,
		IsCashPayment:    dbOrder.IsCashPayment,
		CashAmount:       dbOrder.CashAmount,
		Status:           dbOrder.Status,
	}
}

func CreateOrderListResp(dbDriverOrderList []database.DriverOrder) []Order {
	orderList := []Order{}
	for _, dbDriverOrder := range dbDriverOrderList {
		orderList = append(orderList, ConvOrderToOrder(dbDriverOrder))
	}
	return orderList
}

type DriverOrder struct {
	Id               uuid.UUID `json:"id"`
	OrderID          uuid.UUID `json:"order_id"`
	RestaurantID     uuid.UUID `json:"restaurant_id"`
	RestaurantName   string    `json:"restaurant_name"`
	RestaurantAddr   string    `json:"restaurant_addr"`
	RestaurantLat    string    `json:"restaurant_lat"`
	RestaurantLong   string    `json:"restaurant_long"`
	DeliveryDistance float64   `json:"delivery_dist"`
	Earning          float64   `json:"earning"`
	Tip              int32     `json:"tip"`
	IsCashPayment    bool      `json:"is_cash_payment"`
	CashAmount       float64   `json:"cash_amount"`
	CreatedAt        time.Time `json:"created_at"`
}

func ConvDriverOrderToDriverOrder(dbOrder database.DriverOrder) DriverOrder {
	return DriverOrder{
		Id:               dbOrder.ID,
		CreatedAt:        dbOrder.CreatedAt,
		OrderID:          dbOrder.OrderID,
		RestaurantID:     dbOrder.RestaurantID,
		RestaurantName:   dbOrder.RestaurantName,
		RestaurantAddr:   dbOrder.RestaurantAddr,
		RestaurantLat:    dbOrder.RestaurantLat,
		RestaurantLong:   dbOrder.RestaurantLong,
		DeliveryDistance: dbOrder.DeliveryDistance,
		Earning:          dbOrder.Earning,
		Tip:              dbOrder.Tip,
		IsCashPayment:    dbOrder.IsCashPayment,
		CashAmount:       dbOrder.CashAmount,
	}
}

func CreateDriverOrderListResp(dbDriverOrderList []database.DriverOrder) []DriverOrder {
	orderList := []DriverOrder{}
	for _, dbDriverOrder := range dbDriverOrderList {
		orderList = append(orderList, ConvDriverOrderToDriverOrder(dbDriverOrder))
	}
	return orderList
}

type DriverOrderStatus string

const (
	OrderStatusOnTheWay  DriverOrderStatus = "on_the_way"
	OrderStatusReached   DriverOrderStatus = "reached"
	OrderStatusDelivered DriverOrderStatus = "delivered"
	OrderStatusReturned  DriverOrderStatus = "returned"
	OrderStatusCancelled DriverOrderStatus = "canceled"
)

type UpdateOrderStatusReq struct {
	Status DriverOrderStatus `json:"status"`
}
