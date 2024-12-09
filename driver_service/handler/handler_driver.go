package handler

import (
	"crypto/sha256"
	"encoding/hex"

	"github.com/bytesByHarsh/food_delivery/driver_service/config"
)

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
