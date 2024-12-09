package models

import (
	"encoding/json"
	"net/http"

	"github.com/go-playground/validator/v10"
)

var Validate *validator.Validate

type JSONResp struct {
	Status  string      `json:"status"`
	Message string      `json:"message"`
	Data    interface{} `json:"data"`
}

type JSONerrResponse struct {
	Error string `json:"error"`
}

func VerifyJson(data interface{}, r *http.Request) error {

	if err := json.NewDecoder(r.Body).Decode(data); err != nil {
		return err
	}

	// Validate the struct
	if err := Validate.Struct(data); err != nil {
		return err
	}

	return nil
}

// PaginatedListResp[T]
// @Description Paginates List Response
type PaginatedListResp[T any] struct {
	Data         []T  `json:"data"`
	TotalCount   int  `json:"total_count"`
	HasMore      bool `json:"has_more"`
	Page         int  `json:"page"`
	ItemsPerPage int  `json:"items_per_page"`
}

func (l PaginatedListResp[T]) UpdateHasMore() {
	l.HasMore = (l.Page * l.ItemsPerPage) < l.TotalCount
}
