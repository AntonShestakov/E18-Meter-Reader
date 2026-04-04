-- Flyway initial migration for E18 Meter Reader
-- Creates core tables: users, apartments, meters, user_roles, readings

CREATE TABLE users (
    id BIGINT PRIMARY KEY,
    username VARCHAR(255),
    full_name VARCHAR(255) NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    is_active BOOLEAN NOT NULL DEFAULT true
);

CREATE TABLE apartments (
    id BIGSERIAL PRIMARY KEY,
    number VARCHAR(32) NOT NULL,
    floor INTEGER,
    notes TEXT
);

CREATE TABLE meters (
    id BIGSERIAL PRIMARY KEY,
    apartment_id BIGINT NOT NULL REFERENCES apartments(id) ON DELETE CASCADE,
    meter_number VARCHAR(128) NOT NULL,
    installed_at DATE,
    is_active BOOLEAN NOT NULL DEFAULT true
);

CREATE TABLE user_roles (
    id BIGSERIAL PRIMARY KEY,
    user_id BIGINT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    role VARCHAR(32) NOT NULL CHECK (role IN ('administrator', 'grayhound', 'tenant')),
    apartment_id BIGINT REFERENCES apartments(id) ON DELETE SET NULL,
    valid_from DATE NOT NULL,
    valid_to DATE,
    assigned_by BIGINT REFERENCES users(id) ON DELETE SET NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE readings (
    id BIGSERIAL PRIMARY KEY,
    meter_id BIGINT NOT NULL REFERENCES meters(id) ON DELETE CASCADE,
    value NUMERIC(10,2) NOT NULL,
    read_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    submitted_by BIGINT NOT NULL REFERENCES users(id),
    source VARCHAR(32) NOT NULL CHECK (source IN ('numeric', 'photo')),
    photo_file_id VARCHAR(255),
    notes TEXT
);
