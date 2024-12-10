package handler

import (
	"database/sql"
	"fmt"
	"net/http"
	"time"

	"github.com/bytesByHarsh/food_delivery/driver_service/internal/database"
	"github.com/bytesByHarsh/food_delivery/driver_service/models"
	"github.com/google/uuid"
)

func AddNewOrder(w http.ResponseWriter, r *http.Request) {

	params := models.CreateOrderReq{}

	err := models.VerifyJson(&params, r)
	if err != nil {
		responseWithError(w, http.StatusBadRequest,
			fmt.Sprintf("Error parsing JSON: %v", err),
		)
		return
	}

	dbOrder, err := apiCfg.DB.CreateOrder(r.Context(), database.CreateOrderParams{
		ID:               uuid.New(),
		CreatedAt:        time.Now().UTC(),
		UpdatedAt:        time.Now().UTC(),
		DeletedAt:        sql.NullTime{},
		DriverID:         params.DriverID,
		OrderID:          params.OrderID,
		RestaurantID:     params.RestaurantID,
		RestaurantName:   params.RestaurantName,
		RestaurantAddr:   params.RestaurantAddr,
		RestaurantLat:    params.RestaurantLat,
		RestaurantLong:   params.RestaurantLong,
		CustomerID:       params.CustomerID,
		CustomerAddr:     params.CustomerAddr,
		CustomerName:     params.CustomerName,
		CustomerPhone:    params.CustomerPhone,
		CustomerLat:      params.CustomerLat,
		CustomerLong:     params.CustomerLong,
		DeliveryDistance: params.DeliveryDistance,
		Earning:          params.Earning,
		Tip:              params.Tip,
		IsCashPayment:    params.IsCashPayment,
		CashAmount:       params.CashAmount,
		Status:           database.OrderStatusUnassigned,
	})

	if err != nil {
		responseWithError(w, http.StatusBadRequest,
			fmt.Sprintf("couldn't create order: %v", err),
		)
		return
	}

	resp := models.JSONResp{
		Status:  "success",
		Message: "Driver Created",
		Data:    models.ConvOrderToOrder(dbOrder),
	}
	responseWithJson(w, http.StatusCreated, resp)
}
