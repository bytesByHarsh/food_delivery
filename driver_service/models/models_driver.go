package models

import (
	"time"

	"github.com/bytesByHarsh/food_delivery/driver_service/internal/database"
	"github.com/google/uuid"
)

type CreateDriverByAdminReq struct {
	Username string `json:"username" validate:"required"`
	Email    string `json:"email" validate:"required"`
	Name     string `json:"name" validate:"required"`
	Password string `json:"password" validate:"required"`
	PhoneNum string `json:"phone_num" validate:"required"`
	Age      int32  `json:"age" validate:"required"`
}

type UpdateDriverReq struct {
	Username   string `json:"username" validate:"required"`
	Email      string `json:"email" validate:"required"`
	Name       string `json:"name" validate:"required"`
	PhoneNum   string `json:"phone_num" validate:"required"`
	ProfileImg string `json:"profile_img" validate:"required"`
}

type UpdatePasswordReq struct {
	Password string `json:"password" validate:"required"`
}

type GetDriverListReq struct {
	Page         int `json:"page"`
	ItemsPerPage int `json:"items_per_page"`
}

type Driver struct {
	ID          uuid.UUID `json:"id"`
	CreatedAt   time.Time `json:"created_at"`
	UpdatedAt   time.Time `json:"updated_at"`
	Name        string    `json:"name"`
	PhoneNum    string    `json:"phone_number"`
	Email       string    `json:"email"`
	Username    string    `json:"username"`
	ProfileImg  string    `json:"profile_img"`
	Role        int32     `json:"role"`
	IsSuperUser bool      `json:"is_superuser"`
	Age         int32     `json:"age"`
}

func ConvDriverToDriver(dbDriver database.Driver) Driver {
	return Driver{
		ID:          dbDriver.ID,
		CreatedAt:   dbDriver.CreatedAt,
		UpdatedAt:   dbDriver.UpdatedAt,
		Name:        dbDriver.Name,
		PhoneNum:    dbDriver.PhoneNum,
		Email:       dbDriver.Email,
		Username:    dbDriver.Username,
		ProfileImg:  dbDriver.ProfileImg,
		Age:         dbDriver.Age,
		IsSuperUser: dbDriver.IsSuperuser,
	}
}

func CreateUserListResp(dbDriverList []database.Driver) []Driver {
	userList := []Driver{}
	for _, dbDriver := range dbDriverList {
		userList = append(userList, ConvDriverToDriver(dbDriver))
	}
	return userList
}
