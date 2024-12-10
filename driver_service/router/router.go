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

	v1Router.Mount("/drivers", driverRouter)
	app.Mount("/v1", v1Router)
}
