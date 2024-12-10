-- name: CreateDriver :one
INSERT INTO drivers(id, name, phone_num, email, username,
                  profile_img, is_superuser, hashed_password, age,
                  created_at, updated_at, deleted_at, is_deleted)
VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12, $13)
RETURNING *;


-- name: GetDriverByUsername :one
SELECT * from drivers WHERE username=$1 AND is_deleted = false;

-- name: GetDriverByEmail :one
SELECT * from drivers WHERE email=$1 AND is_deleted = false;

-- name: GetDriverById :one
SELECT * from drivers WHERE id=$1 AND is_deleted = false;

-- name: GetAllDrivers :many
SELECT *
FROM
    drivers
WHERE is_deleted = false
ORDER BY
    name ASC
LIMIT $1 OFFSET $2;

-- name: GetDriverCount :one
SELECT COUNT(*) FROM drivers WHERE is_deleted=false;

-- name: UpdateDriver :exec
UPDATE drivers
SET updated_at = $2,
    name = $3,
    phone_num = $4,
    email = $5,
    username = $6,
    profile_img = $7,
    age = $8
WHERE id = $1 AND is_deleted=false
RETURNING *;

-- name: UpdateDriverPassword :exec
UPDATE drivers
SET hashed_password=$2,
    updated_at = $3
WHERE id = $1 AND is_deleted = false
RETURNING *;

-- name: DeleteDriver :exec
UPDATE drivers
SET deleted_at = $2,
    is_deleted = true,
    updated_at = $3
WHERE id = $1
RETURNING *;

-- name: HardDeleteUser :exec
DELETE FROM drivers
WHERE id = $1;