package config

import (
	"fmt"
	"log"
	"os"

	"github.com/joho/godotenv"
)

type EnvConfig struct {
	SERVER_PORT string
	SERVER_LINK string
	DB_URL      string

	SECRET_KEY     string
	JWT_SECRET_KEY string
}

var Cfg EnvConfig

func ReadEnvFile(envPath string) {
	if envPath == "" {
		envPath = ".env"
	}
	// load .env file
	err := godotenv.Load(envPath)
	if err != nil {
		fmt.Print("Error loading .env file")
	}

	Cfg.SERVER_LINK = os.Getenv("SERVER_LINK")
	Cfg.SERVER_PORT = os.Getenv("SERVER_PORT")
	Cfg.DB_URL = os.Getenv("DB_URL")
	Cfg.SECRET_KEY = os.Getenv("SECRET_KEY")
	Cfg.JWT_SECRET_KEY = os.Getenv("JWT_SECRET_KEY")

	if Cfg.SERVER_LINK == "" {
		Cfg.SERVER_LINK = "0.0.0.0"
	}

	if Cfg.SERVER_PORT == "" {
		Cfg.SERVER_PORT = "3000"
	}

	if Cfg.DB_URL == "" {
		log.Fatal("DB URL is not Mentioned")
	}
	if Cfg.JWT_SECRET_KEY == "" {
		log.Fatal("JWT Token not defined is not Mentioned")
	}
}

func Config(key string) string {
	return os.Getenv(key)
}
