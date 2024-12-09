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

	app.Mount("/v1", v1Router)
}
