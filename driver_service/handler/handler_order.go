package handler

import (
	"database/sql"
	"fmt"
	"net/http"
	"time"

	"github.com/bytesByHarsh/food_delivery/driver_service/internal/database"
	"github.com/bytesByHarsh/food_delivery/driver_service/models"
	"github.com/go-chi/chi"
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

func GetUnassignedOrderList(w http.ResponseWriter, r *http.Request, driver database.Driver) {
	page, items_per_page, err := parsePaginatedReq(r)
	if err != nil {
		responseWithError(w, http.StatusBadRequest,
			fmt.Sprintf("incorrect data: %v", err),
		)
		return
	}

	dbDriverOrderList, err := apiCfg.DB.GetAllUnassignedOrder(r.Context(), database.GetAllUnassignedOrderParams{
		Limit:  int32(items_per_page),
		Offset: int32((page - 1) * items_per_page),
	})

	if err != nil {
		responseWithError(w, http.StatusBadRequest,
			fmt.Sprintf("couldn't get order list: %v", err),
		)
		return
	}

	total_count, err := apiCfg.DB.GetUnassignedOrderCount(r.Context())
	if err != nil {
		responseWithError(w, http.StatusBadRequest,
			fmt.Sprintf("couldn't get driver list: %v", err),
		)
		return
	}

	resp := models.PaginatedListResp[models.DriverOrder]{
		Data:         models.CreateDriverOrderListResp(dbDriverOrderList),
		Page:         page,
		ItemsPerPage: items_per_page,
		TotalCount:   int(total_count),
	}
	resp.UpdateHasMore()
	responseWithJson(w, http.StatusOK, resp)
}

func AcceptOrder(w http.ResponseWriter, r *http.Request, driver database.Driver) {
	id := chi.URLParam(r, "id")
	orderId, err := uuid.Parse(id)

	if err != nil {
		responseWithError(w, http.StatusNotFound,
			fmt.Sprintf("Couldn't parse order id: %v", id),
		)
		return
	}

	dbOrder, err := apiCfg.DB.GetOrderById(r.Context(), driver.ID)

	if err != nil {
		responseWithError(w, http.StatusNotFound,
			fmt.Sprintf("Order Not Found: %v", id),
		)
		return
	}

	if dbOrder.DriverID.Valid {
		responseWithError(w, http.StatusForbidden,
			fmt.Sprintln("Order Already Assigned"),
		)
		return
	}

	driverId := uuid.NullUUID{
		Valid: true,
		UUID:  driver.ID,
	}

	err = apiCfg.DB.UpdateOrderDriver(r.Context(), database.UpdateOrderDriverParams{
		ID:         orderId,
		DriverID:   driverId,
		UpdatedAt:  time.Now().UTC(),
		AssignedAt: time.Now().UTC(),
	})

	if err != nil {
		responseWithError(w, http.StatusBadRequest,
			fmt.Sprintf("couldn't assign driver: %v", err),
		)
		return
	}

	resp := models.JSONResp{
		Status:  "success",
		Message: "Driver Assigned to order",
		Data:    nil,
	}
	responseWithJson(w, http.StatusAccepted, resp)
}

func UpdateOrderStatus(w http.ResponseWriter, r *http.Request, driver database.Driver) {
	id := chi.URLParam(r, "id")
	orderId, err := uuid.Parse(id)

	if err != nil {
		responseWithError(w, http.StatusNotFound,
			fmt.Sprintf("Couldn't parse order id: %v", id),
		)
		return
	}

	params := models.UpdateOrderStatusReq{}
	err = models.VerifyJson(&params, r)
	if err != nil {
		responseWithError(w, http.StatusBadRequest,
			fmt.Sprintf("Error parsing JSON: %v", err),
		)
		return
	}

	status := database.OrderStatusAssigned
	switch params.Status {
	case models.OrderStatusOnTheWay, models.OrderStatusReached, models.OrderStatusReturned:
		status = database.OrderStatusInProgress
	case models.OrderStatusDelivered:
		status = database.OrderStatusCompleted
	case models.OrderStatusCancelled:
		status = database.OrderStatusCancelled
	}

	err = apiCfg.DB.UpdateOrderStatus(r.Context(), database.UpdateOrderStatusParams{
		ID:        orderId,
		Status:    status,
		UpdatedAt: time.Now().UTC(),
	})

	if err != nil {
		responseWithError(w, http.StatusBadRequest,
			fmt.Sprintf("couldn't update driver order status: %v", err),
		)
		return
	}
}
