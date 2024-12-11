package models

import "github.com/google/uuid"

type OrderService_UpdateDriverReq struct {
	DeliveryPersonId   uuid.UUID `json:"delivery_person_id"`
	DeliveryPersonName string    `json:"delivery_person_name"`
}
