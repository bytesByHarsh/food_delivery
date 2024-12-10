package db

import (
	"context"
	"database/sql"
	"log"
	"time"

	"github.com/bytesByHarsh/food_delivery/driver_service/config"
	"github.com/bytesByHarsh/food_delivery/driver_service/handler"
	"github.com/bytesByHarsh/food_delivery/driver_service/internal/database"
	"github.com/google/uuid"

	_ "github.com/lib/pq"
)

var DB *database.Queries

func ConnectDb() error {
	dbConn, err := sql.Open("postgres", config.Cfg.DB_URL)
	if err != nil {
		log.Fatal("Can't connect to database:", err)
	}
	DB = database.New(dbConn)

	handler.UpdateDB(DB)

	InitDb()

	return nil
}

func InitDb() {
	adminDetails := database.CreateDriverParams{
		ID:             uuid.New(),
		CreatedAt:      time.Now().UTC(),
		UpdatedAt:      time.Now().UTC(),
		DeletedAt:      sql.NullTime{},
		IsDeleted:      false,
		Name:           "Admin User",
		Email:          "admin@admin.com",
		PhoneNum:       "+919879879",
		ProfileImg:     "",
		Username:       "admin",
		IsSuperuser:    true,
		HashedPassword: handler.HashPassword("123"),
	}
	_, err := DB.GetDriverByUsername(context.Background(), adminDetails.Username)
	if err == nil {
		// Admin user already created
		return
	}

	_, err = DB.CreateDriver(context.Background(), adminDetails)
	if err != nil {
		log.Fatalln("Not Able to create admin credentials: ", err)
	}

}
