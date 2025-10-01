# MotoBookingServer API Documentation

This server manages moto bookings stored in a file. It supports basic authentication and lets clients create, read, update, and delete bookings using HTTP methods.

---

## Authentication

- **Type:** Basic Authentication  
- **How to Provide:** Include an HTTP header `Authorization: Basic <credentials>`  
- **Credentials:**  
  - Username: `user`  
  - Password: `pass`  
- The credentials are base64 encoded in the header. Requests without correct authentication will be denied.

---

## Supported HTTP Methods and Their Usage

### GET - Retrieve Booking(s)

- **Endpoint:** `/` (root)  
- **Query Parameters:**
  - `id` (optional): The booking ID to retrieve a specific booking.  
- **Behavior:**
  - If `id` is provided, returns the booking with that ID.  
  - If no `id` is provided, returns the full list of bookings.  
- **Response codes:**
  - `200 OK` on success  
  - `404 Not Found` if specific booking not found  
  - `400 Bad Request` if `id` is invalid  

---

### POST - Create a New Booking

- **Endpoint:** `/` (root)  
- **Body:** JSON object representing the new booking (excluding `id`).  
- **Behavior:**  
  - Adds the booking to the database with a new unique `id`.  
- **Response codes:**
  - `201 Created` on success  

---

### PUT - Replace an Existing Booking

- **Endpoint:** `/` (root)  
- **Query Parameters:**  
  - `id` (required): The booking ID to replace.  
- **Body:** JSON object representing the entire new booking data.  
- **Behavior:**  
  - Replaces the booking with the given `id` with the new data.  
- **Response codes:**
  - `200 OK` on success  
  - `400 Bad Request` if `id` missing or invalid  
  - `404 Not Found` if booking does not exist  

---

### PATCH - Update Parts of a Booking

- **Endpoint:** `/` (root)  
- **Query Parameters:**  
  - `id` (required): The booking ID to update.  
- **Body:** JSON object with fields to update.  
- **Behavior:**  
  - Updates only the provided fields of the booking with the given `id`.  
- **Response codes:**
  - `200 OK` on success  
  - `400 Bad Request` if `id` missing or invalid  
  - `404 Not Found` if booking does not exist  

---

### DELETE - Remove a Booking

- **Endpoint:** `/` (root)  
- **Query Parameters:**  
  - `id` (required): The booking ID to delete.  
- **Behavior:**
  - Deletes the booking with the given `id`.  
- **Response codes:**
  - `200 OK` on success  
  - `400 Bad Request` if `id` missing or invalid  
  - `404 Not Found` if booking does not exist  

---

## Notes

- All endpoints require Basic Authentication.  
- All request and response data use JSON format.  
- The server runs on `http://127.0.0.1:8000` by default.  
- Bookings are stored persistently in a file named `data.json`.  

---
