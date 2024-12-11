package router

import (
	"github.com/bytesByHarsh/food_delivery/driver_service/handler"
	"github.com/go-chi/chi"
)

func SetupRoutes(app *chi.Mux) {
	handler.Init()
	// Middleware
	v1Router := chi.NewRouter()
	v1Router.Get("/", handler.Hello)

	// Driver
	driverRouter := chi.NewRouter()
	driverRouter.Post("/register", handler.MiddlewareAuth(handler.CreateDriver))
	driverRouter.Post("/login", handler.LoginDriver)

	driverRouter.Get("/me", handler.MiddlewareAuth(handler.GetDriver))
	driverRouter.Put("/me/password", handler.MiddlewareAuth(handler.UpdateDriverPassword))
	driverRouter.Get("/{id}", handler.MiddlewareAuth(handler.GetAnotherDriver))
	driverRouter.Delete("/{id}", handler.MiddlewareAuth(handler.DbDeleteDriver))
	driverRouter.Get("/list", handler.MiddlewareAuth(handler.GetDriverList))

	// Orders
	orderRouter := chi.NewRouter()
	orderRouter.Post("/", handler.AddNewOrder)
	orderRouter.Get("/list/unassigned", handler.MiddlewareAuth(handler.GetUnassignedOrderList))
	orderRouter.Put("/{id}/accept", handler.MiddlewareAuth(handler.AcceptOrder))
	orderRouter.Put("/{id}/status", handler.MiddlewareAuth(handler.UpdateOrderStatus))

	v1Router.Mount("/drivers", driverRouter)
	v1Router.Mount("/orders", orderRouter)
	app.Mount("/v1", v1Router)
}
