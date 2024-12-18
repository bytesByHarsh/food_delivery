package handler

import (
	"bytes"
	"database/sql"
	"encoding/json"
	"fmt"
	"net/http"
	"time"

	"github.com/bytesByHarsh/food_delivery/driver_service/config"
	"github.com/bytesByHarsh/food_delivery/driver_service/internal/database"
	"github.com/bytesByHarsh/food_delivery/driver_service/models"
	"github.com/go-chi/chi"
	"github.com/google/uuid"
)

// AddNewOrder godoc
//
//	@Summary		Add New Order
//	@Description	create new order
//	@Tags			Orders
//	@Accept			json
//	@Produce		json
//	@Param			user	body		models.CreateOrderReq	true	"Order Body"
//	@Success		201		{object}	models.Order
//	@Failure		400		{object}	models.JSONerrResponse
//	@Router			/orders [post]
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
		DriverID:         uuid.NullUUID{},
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

// GetUnassignedOrderList godoc
//
//	@Summary		Get Unassigned Order
//	@Description	get order list
//	@Tags			Orders
//	@Accept			json
//	@Produce		json
//	@Param			page			query		int32	true	"Page Number"
//	@Param			items_per_page	query		int32	true	"Items Per Page"
//	@Success		201				{object}	models.Order
//	@Failure		400				{object}	models.JSONerrResponse
//	@Router			/orders/list/unassigned [get]
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

// AcceptOrder godoc
//
//	@Summary		Accept Order
//	@Description	accept order by driver
//	@Tags			Orders
//	@Accept			json
//	@Produce		json
//	@Param			id	path		string	true	"id"
//	@Success		200	{object}	models.JSONResp
//	@Failure		400	{object}	models.JSONerrResponse
//	@Router			/orders/{id}/accept [put]
func AcceptOrder(w http.ResponseWriter, r *http.Request, driver database.Driver) {
	id := chi.URLParam(r, "id")
	driverOrderId, err := uuid.Parse(id)

	if err != nil {
		responseWithError(w, http.StatusNotFound,
			fmt.Sprintf("Couldn't parse order id: %v", id),
		)
		return
	}

	dbOrder, err := apiCfg.DB.GetOrderById(r.Context(), driverOrderId)

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
		ID:         driverOrderId,
		DriverID:   driverId,
		UpdatedAt:  time.Now().UTC(),
		AssignedAt: time.Now().UTC(),
		Status:     database.OrderStatusAssigned,
	})

	if err != nil {
		responseWithError(w, http.StatusBadRequest,
			fmt.Sprintf("couldn't assign driver: %v", err),
		)
		return
	}

	// Update status to Order Service
	url := config.Cfg.ORDER_API_BASE + fmt.Sprintf("/orders/assign/%v", dbOrder.OrderID)
	payload := models.OrderService_UpdateDriverReq{
		DeliveryPersonName: driver.Name,
		DeliveryPersonId:   driver.ID,
	}

	payloadBytes, err := json.Marshal(payload)
	if err != nil {
		fmt.Printf("Error marshaling payload: %v\n", err)
		return
	}
	sendHTTPReq(http.MethodPut, url, bytes.NewBuffer(payloadBytes))

	resp := models.JSONResp{
		Status:  "success",
		Message: "Driver Assigned to order",
		Data:    nil,
	}
	responseWithJson(w, http.StatusAccepted, resp)
}

// UpdateOrderStatus godoc
//
//	@Summary		Update Order Status
//	@Description	update order status
//	@Tags			Orders
//	@Accept			json
//	@Produce		json
//	@Param			id		path		string						true	"ID"
//	@Param			status	body		models.UpdateOrderStatusReq	true	"status Body"
//	@Success		200		{object}	models.JSONResp
//	@Failure		400		{object}	models.JSONerrResponse
//	@Router			/orders/{id}/status [put]
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
	default:
		responseWithError(w, http.StatusBadRequest,
			fmt.Sprintf("Unidentified Status: %v", params.Status),
		)
		return
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

	resp := models.JSONResp{
		Status:  "success",
		Message: "Order Status Updated",
		Data:    nil,
	}
	responseWithJson(w, http.StatusAccepted, resp)
}
