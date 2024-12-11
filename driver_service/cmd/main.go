package main

import (
	"fmt"
	"log"
	"net/http"

	"github.com/bytesByHarsh/food_delivery/driver_service/api"
	"github.com/bytesByHarsh/food_delivery/driver_service/config"
	db "github.com/bytesByHarsh/food_delivery/driver_service/database"
	"github.com/bytesByHarsh/food_delivery/driver_service/router"
	"github.com/go-chi/chi"
	"github.com/go-chi/chi/middleware"
	"github.com/go-chi/cors"
	httpSwagger "github.com/swaggo/http-swagger"
)

//	@contact.name	Harsh Mittal
//	@contact.url
//	@contact.email	harshmittal2210@gmail.com

func main() {
	config.ReadEnvFile(".env")

	serverAddr := fmt.Sprintf("%v:%v", config.Cfg.SERVER_LINK, config.Cfg.SERVER_PORT)

	db.ConnectDb()

	app := chi.NewRouter()
	app.Use(cors.Handler(cors.Options{
		AllowedOrigins:   []string{"https://*", "http://*"},
		AllowedMethods:   []string{"GET", "POST", "PUT", "DELETE", "OPTIONS"},
		AllowedHeaders:   []string{"*"},
		ExposedHeaders:   []string{"Link"},
		AllowCredentials: true,
		MaxAge:           300,
	}))
	app.Use(middleware.RequestID)
	app.Use(middleware.Logger)
	app.Use(middleware.Recoverer)

	// Swagger
	api.SwaggerInfo.Title = "My Information Server"
	api.SwaggerInfo.Version = "0.0.1"
	api.SwaggerInfo.BasePath = "/v1"
	api.SwaggerInfo.Schemes = []string{"http", "https"}
	api.SwaggerInfo.Description = ` Backend Service for Driver API

`

	app.Get("/swagger/*", httpSwagger.Handler(
		httpSwagger.URL("/swagger/doc.json"), // The url pointing to API definition"
	))

	router.SetupRoutes(app)
	log.Printf("Server Starting on Address: %v", serverAddr)
	err := http.ListenAndServe(serverAddr, app)
	if err != nil {
		log.Fatal(err)
	}
}
