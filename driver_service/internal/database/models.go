// Code generated by sqlc. DO NOT EDIT.
// versions:
//   sqlc v1.27.0

package database

import (
	"database/sql"
	"database/sql/driver"
	"fmt"
	"time"

	"github.com/google/uuid"
)

type OrderStatus string

const (
	OrderStatusAssigned   OrderStatus = "assigned"
	OrderStatusInProgress OrderStatus = "in-progress"
	OrderStatusCompleted  OrderStatus = "completed"
	OrderStatusCancelled  OrderStatus = "cancelled"
	OrderStatusUnassigned OrderStatus = "unassigned"
)

func (e *OrderStatus) Scan(src interface{}) error {
	switch s := src.(type) {
	case []byte:
		*e = OrderStatus(s)
	case string:
		*e = OrderStatus(s)
	default:
		return fmt.Errorf("unsupported scan type for OrderStatus: %T", src)
	}
	return nil
}

type NullOrderStatus struct {
	OrderStatus OrderStatus
	Valid       bool // Valid is true if OrderStatus is not NULL
}

// Scan implements the Scanner interface.
func (ns *NullOrderStatus) Scan(value interface{}) error {
	if value == nil {
		ns.OrderStatus, ns.Valid = "", false
		return nil
	}
	ns.Valid = true
	return ns.OrderStatus.Scan(value)
}

// Value implements the driver Valuer interface.
func (ns NullOrderStatus) Value() (driver.Value, error) {
	if !ns.Valid {
		return nil, nil
	}
	return string(ns.OrderStatus), nil
}

type Driver struct {
	ID             uuid.UUID
	Name           string
	PhoneNum       string
	Email          string
	Username       string
	ProfileImg     string
	IsSuperuser    bool
	HashedPassword string
	Age            int32
	CreatedAt      time.Time
	UpdatedAt      time.Time
	DeletedAt      sql.NullTime
	IsDeleted      bool
}

type DriverOrder struct {
	ID               uuid.UUID
	DriverID         uuid.NullUUID
	OrderID          uuid.UUID
	RestaurantID     uuid.UUID
	RestaurantName   string
	RestaurantAddr   string
	RestaurantLat    string
	RestaurantLong   string
	CustomerID       uuid.UUID
	CustomerAddr     string
	CustomerName     string
	CustomerPhone    string
	CustomerLat      string
	CustomerLong     string
	Status           OrderStatus
	DeliveryDistance float64
	Earning          float64
	Tip              int32
	IsCashPayment    bool
	CashAmount       float64
	CreatedAt        time.Time
	AssignedAt       time.Time
	UpdatedAt        time.Time
	DeletedAt        sql.NullTime
	IsDeleted        bool
}
