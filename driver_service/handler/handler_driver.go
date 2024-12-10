package handler

import (
	"crypto/sha256"
	"database/sql"
	"encoding/hex"
	"fmt"
	"net/http"
	"time"

	"github.com/bytesByHarsh/food_delivery/driver_service/config"
	"github.com/bytesByHarsh/food_delivery/driver_service/internal/database"
	"github.com/bytesByHarsh/food_delivery/driver_service/models"
	"github.com/go-chi/chi"
	"github.com/google/uuid"
)

func CreateDriver(w http.ResponseWriter, r *http.Request, driver database.Driver) {

	params := models.CreateDriverByAdminReq{}

	err := models.VerifyJson(&params, r)
	if err != nil {
		responseWithError(w, http.StatusBadRequest,
			fmt.Sprintf("Error parsing JSON: %v", err),
		)
		return
	}

	hash := HashPassword(params.Password)

	dbUser, err := apiCfg.DB.CreateDriver(r.Context(), database.CreateDriverParams{
		ID:             uuid.New(),
		CreatedAt:      time.Now().UTC(),
		UpdatedAt:      time.Now().UTC(),
		DeletedAt:      sql.NullTime{},
		IsDeleted:      false,
		Name:           params.Name,
		Email:          params.Email,
		Username:       params.Username,
		PhoneNum:       params.PhoneNum,
		ProfileImg:     "",
		Age:            params.Age,
		HashedPassword: hash,
		IsSuperuser:    false,
	})

	if err != nil {
		responseWithError(w, http.StatusBadRequest,
			fmt.Sprintf("couldn't create driver: %v", err),
		)
		return
	}

	resp := models.JSONResp{
		Status:  "success",
		Message: "Driver Created",
		Data:    models.ConvDriverToDriver(dbUser),
	}
	responseWithJson(w, http.StatusCreated, resp)
}

func GetDriver(w http.ResponseWriter, r *http.Request, driver database.Driver) {
	responseWithJson(w, http.StatusOK, models.ConvDriverToDriver(driver))
}

func GetAnotherDriver(w http.ResponseWriter, r *http.Request, driver database.Driver) {
	id := chi.URLParam(r, "id")

	uId, err := uuid.Parse(id)

	if err != nil {
		responseWithError(w, http.StatusNotFound,
			fmt.Sprintf("Couldn't parse driver id: %v", id),
		)
		return
	}

	driverDb, err := apiCfg.DB.GetDriverById(r.Context(), uId)
	if err != nil {
		responseWithError(w, http.StatusNotFound,
			fmt.Sprintf("Couldn't get driver: %v", err),
		)
		return
	}
	responseWithJson(w, http.StatusOK, models.ConvDriverToDriver(driverDb))
}

func GetUserList(w http.ResponseWriter, r *http.Request, driver database.Driver) {
	if !driver.IsSuperuser {
		responseWithError(w, http.StatusUnauthorized,
			"Access Denied",
		)
		return
	}

	page, items_per_page, err := parsePaginatedReq(r)
	if err != nil {
		responseWithError(w, http.StatusBadRequest,
			fmt.Sprintf("incorrect data: %v", err),
		)
		return
	}

	dbUserList, err := apiCfg.DB.GetAllDrivers(r.Context(), database.GetAllDriversParams{
		Limit:  int32(items_per_page),
		Offset: int32((page - 1) * items_per_page),
	})

	if err != nil {
		responseWithError(w, http.StatusBadRequest,
			fmt.Sprintf("couldn't get driver list: %v", err),
		)
		return
	}

	total_count, err := apiCfg.DB.GetDriverCount(r.Context())
	if err != nil {
		responseWithError(w, http.StatusBadRequest,
			fmt.Sprintf("couldn't get driver list: %v", err),
		)
		return
	}

	resp := models.PaginatedListResp[models.Driver]{
		Data:         models.CreateUserListResp(dbUserList),
		Page:         page,
		ItemsPerPage: items_per_page,
		TotalCount:   int(total_count),
	}
	resp.UpdateHasMore()
	responseWithJson(w, http.StatusOK, resp)
}

func UpdateDriverPassword(w http.ResponseWriter, r *http.Request, driver database.Driver) {
	params := models.UpdatePasswordReq{}

	err := models.VerifyJson(&params, r)
	if err != nil {
		responseWithError(w, http.StatusBadRequest,
			fmt.Sprintf("Error parsing JSON: %v", err),
		)
		return
	}

	err = apiCfg.DB.UpdateDriverPassword(r.Context(), database.UpdateDriverPasswordParams{
		ID:             driver.ID,
		UpdatedAt:      time.Now().UTC(),
		HashedPassword: HashPassword(params.Password),
	})

	if err != nil {
		responseWithError(w, 400,
			fmt.Sprintf("couldn't update driver password: %v", err),
		)
		return
	}

	resp := models.JSONResp{
		Status:  "success",
		Message: "User Password Updated",
		Data:    nil,
	}
	responseWithJson(w, http.StatusAccepted, resp)
}

func DbDeleteUser(w http.ResponseWriter, r *http.Request, driver database.Driver) {
	if !driver.IsSuperuser {
		responseWithError(w, http.StatusUnauthorized,
			"Proper Authentication Required",
		)
		return
	}

	id := chi.URLParam(r, "id")

	uId, err := uuid.Parse(id)

	if err != nil {
		responseWithError(w, http.StatusNotFound,
			fmt.Sprintf("Couldn't parse driver id: %v", id),
		)
		return
	}

	err = apiCfg.DB.HardDeleteUser(r.Context(), uId)

	if err != nil {
		responseWithError(w, 400,
			fmt.Sprintf("couldn't permanently delete driver: %v", err),
		)
		return
	}

	resp := models.JSONResp{
		Status:  "success",
		Message: "User Deleted Permanently",
		Data:    nil,
	}
	responseWithJson(w, http.StatusAccepted, resp)
}

func HashPassword(password string) string {
	// bytes, err := bcrypt.GenerateFromPassword([]byte(password), 14)
	// return string(bytes), err
	// Concatenate the secret and password
	combined := config.Cfg.SECRET_KEY + password
	hash := sha256.New()
	hash.Write([]byte(combined))
	hashedBytes := hash.Sum(nil)
	return hex.EncodeToString(hashedBytes)
}
