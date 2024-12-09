package handler

import (
	"errors"
	"log"
	"net/http"
	"strconv"

	"github.com/bytesByHarsh/food_delivery/driver_service/config"
	"github.com/bytesByHarsh/food_delivery/driver_service/internal/database"
	"github.com/bytesByHarsh/food_delivery/driver_service/models"
	"github.com/go-chi/jwtauth"
	"github.com/go-playground/validator/v10"
)

type apiConfig struct {
	DB        *database.Queries
	AuthToken *jwtauth.JWTAuth
}

var apiCfg apiConfig

func UpdateDB(db *database.Queries) {
	if db == nil {
		log.Fatal("Empty DB pointer Received")
	}
	apiCfg.DB = db
}

func Init() {
	models.Validate = validator.New()

	apiCfg.AuthToken = jwtauth.New("HS256", []byte(config.Cfg.JWT_SECRET_KEY), nil)

	claims := map[string]interface{}{
		"id": "123456789",
	}
	// For confirming that tokens are generating
	_, _, err := apiCfg.AuthToken.Encode(claims)
	if err != nil {
		log.Fatalf("Token not generated: %v", err)
	}
	// log.Printf("Dummy Token: %v", tokenString)
}

// Hello godoc
//
//	@Summary		Hello API
//	@Description	get string by ID
//	@Tags			Ping
//	@Produce		json
//	@Success		200	{object}	models.JSONResp
//	@Router			/ [get]
func Hello(w http.ResponseWriter, r *http.Request) {
	resp := models.JSONResp{
		Status:  "success",
		Message: "Hello i'm not ok!",
		Data:    nil,
	}
	responseWithJson(w, 201, resp)
}

func parsePaginatedReq(r *http.Request) (int, int, error) {
	pageStr := r.URL.Query().Get("page")
	items_per_pageStr := r.URL.Query().Get("items_per_page")
	if pageStr == "" || items_per_pageStr == "" {
		return 0, 0, errors.New("wrong query give")
	}

	page, err := strconv.Atoi(pageStr)
	if err != nil {
		return 0, 0, err
	}
	items_per_page, err := strconv.Atoi(items_per_pageStr)
	if err != nil {
		return 0, 0, err
	}
	return page, items_per_page, err
}
