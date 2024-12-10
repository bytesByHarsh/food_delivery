package handler

import (
	"errors"
	"fmt"
	"net/http"
	"strconv"
	"strings"
	"time"

	"github.com/bytesByHarsh/food_delivery/driver_service/internal/database"
	"github.com/bytesByHarsh/food_delivery/driver_service/models"
)

type authHandler func(http.ResponseWriter, *http.Request, database.Driver)

// LoginDriver godoc
//
//	@Summary		Login Driver
//	@Description	get login token
//	@Tags			Authentication
//	@Accept			json
//	@Produce		json
//	@Param			login	body		models.AuthReq	true	"Login Body"
//	@Success		201		{object}	models.AuthResp
//	@Failure		400		{object}	models.JSONerrResponse
//	@Router			/drivers/login [post]
func LoginDriver(w http.ResponseWriter, r *http.Request) {

	params := models.AuthReq{}
	err := models.VerifyJson(&params, r)

	if err != nil {
		responseWithError(w, http.StatusBadRequest,
			fmt.Sprintf("Error parsing JSON: %v", err),
		)
		return
	}

	driver, err := apiCfg.DB.GetDriverByUsername(r.Context(), params.Username)
	if err != nil {
		responseWithError(w, http.StatusNotFound,
			fmt.Sprintf("Couldn't get driver: %v", err),
		)
		return
	}

	if !checkPassword(driver.HashedPassword, params.Password) {
		responseWithError(w, http.StatusBadRequest,
			"wrong password",
		)
		return
	}

	expirationTime := time.Now().UTC().Add(8 * time.Hour) //Valid for 8hrs
	// expirationTime := time.Now().UTC().Add(time.Second)
	var expirationTimeStr string = strconv.FormatUint(uint64(expirationTime.Unix()), 10)
	claims := map[string]interface{}{
		"username":     driver.Username,
		"is_superuser": driver.IsSuperuser,
		"time":         expirationTimeStr,
	}

	_, tokenString, err := apiCfg.AuthToken.Encode(claims)
	if err != nil {
		responseWithError(w, http.StatusBadRequest,
			"token not generated",
		)
		return
	}

	// resp := models.JSONResp{
	// 	Status:  "success",
	// 	Message: "Driver Logged In",
	// 	Data:    models.AuthResp{Token: tokenString},
	// }
	cookie := http.Cookie{
		Name:  "access_token",
		Value: tokenString,
		// MaxAge:   8 * 60 * 60,
		Secure:   false,
		SameSite: http.SameSiteLaxMode,
		Path:     "/",
		HttpOnly: true,
	}
	http.SetCookie(w, &cookie)
	responseWithJson(w, 201, models.AuthResp{Token: tokenString})

}

func getTokenFromHeader(headers http.Header) (string, error) {
	value := headers.Get("Authorization")
	if value == "" {
		return "", errors.New("no authentication Info Found")
	}

	values := strings.Split(value, " ")
	if len(values) != 2 {
		return "", errors.New("malformed auth header")
	}

	if values[0] != "Bearer" {
		return "", errors.New("malformed first part of auth header")
	}

	return values[1], nil
}

func MiddlewareAuth(handler authHandler) http.HandlerFunc {
	return func(w http.ResponseWriter, r *http.Request) {
		// Get the JWT token from the cookie
		var tokenInCookie bool = false
		var tokenStr string = ""
		c, err := r.Cookie("access_token")
		if err != nil {
			if err != http.ErrNoCookie {
				responseWithError(w, http.StatusBadRequest, "Bad request")
				return
			}
		} else {
			tokenInCookie = true
			tokenStr = c.Value
		}

		if !tokenInCookie {
			tokenStr, err = getTokenFromHeader(r.Header)
			if err != nil {
				responseWithError(w, http.StatusUnauthorized, "Driver Not Authenticated")
				return
			}
		}

		token, err := apiCfg.AuthToken.Decode(tokenStr)
		if err != nil {
			responseWithError(w, http.StatusBadRequest, "incorrect token")
			return
		}
		claims, err := token.AsMap(r.Context())
		if err != nil {
			responseWithError(w, http.StatusBadRequest, "incorrect token")
			return
		}

		username, _ := claims["username"].(string)
		timeStr, _ := claims["time"].(string)

		expTime, _ := strconv.Atoi(timeStr)
		if uint64(time.Now().UTC().Unix()) > uint64(expTime) {
			responseWithError(w, http.StatusUnauthorized, "token timeout")
			return
		}

		driver, err := apiCfg.DB.GetDriverByUsername(r.Context(), username)
		if err != nil {
			responseWithError(w, http.StatusNotFound,
				fmt.Sprintf("Couldn't get driver: %v", err),
			)
			return
		}

		handler(w, r, driver)
	}
}

func checkPassword(hashPass, inputPass string) bool {
	return HashPassword(inputPass) == hashPass
}
