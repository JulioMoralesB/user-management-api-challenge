# User Management API - Bug Report

### Bug #1: Duplicate Email Returns 500 Instead of 409
**Environment**: dev, prod  
**Endpoint**: POST /users  
**Description**: 
- **Expected behavior (from spec)**: When attempting to create a user with an email that already exists, the API should return HTTP 409 (Conflict) with an error message indicating duplicate email
- **Actual behavior**: Returns HTTP 500 (Internal Server Error) with generic "Internal server error" message
- **Steps to reproduce**: 
  1. Create a user with email "test@example.com"
  2. Attempt to create another user with the same email "test@example.com"
  3. Observe status code is 500 instead of 409

### Bug #2: Invalid Email Format During Creation Returns 500 Instead of 400
**Environment**: dev, prod  
**Endpoint**: POST /users  
**Description**: 
- **Expected behavior (from spec)**: When creating a user with an invalid email format (e.g., "not-an-email"), should return HTTP 400 (Bad Request)
- **Actual behavior**: Returns HTTP 500 (Internal Server Error)
- **Steps to reproduce**: 
  1. Send POST /users with payload: `{"name": "Test", "email": "not-an-email", "age": 30}`
  2. Observe status code is 500 instead of 400

### Bug #3: Invalid Email Path Parameter Returns 200 Instead of 400/404
**Environment**: dev, prod  
**Endpoint**: GET /users/{email}  
**Description**: 
- **Expected behavior (from spec)**: When requesting a user with an invalid email format in the path (e.g., `/users/not-an-email`), should return either HTTP 400 (invalid format) or 404 (not found)
- **Actual behavior**: Returns HTTP 200 with the response body
- **Steps to reproduce**: 
  1. Send GET /users/not-an-email
  2. Observe status code is 200 instead of 400 or 404

### Bug #4: GET Non-Existent User Returns 500 Instead of 404
**Environment**: dev, prod  
**Endpoint**: GET /users/{email}  
**Description**: 
- **Expected behavior (from spec)**: When requesting a user that does not exist, should return HTTP 404 (Not Found)
- **Actual behavior**: Returns HTTP 500 (Internal Server Error) with "Internal server error" message
- **Steps to reproduce**: 
  1. Send GET /users/nonexistent@example.com (where user doesn't exist)
  2. Observe status code is 500 instead of 404

### Bug #5: DELETE Endpoint Does Not Validate Authentication Header
**Environment**: dev (prod not tested)  
**Endpoint**: DELETE /users/{email}  
**Description**: 
- **Expected behavior (from spec)**: DELETE endpoint requires "Authentication" header with value "mysecrettoken". Missing or invalid tokens should return HTTP 401 (Unauthorized)
- **Actual behavior**: DELETE succeeds with status 204 regardless of whether Authentication header is present, missing, or contains invalid token
- **Steps to reproduce**: 
  1. Create a user with email "test@example.com"
  2. Send DELETE /users/test@example.com without Authentication header
  3. Observe status code is 204 (successful) instead of 401
  4. Send DELETE /users/test@example.com with Authentication: "wrongtoken"
  5. Observe status code is 204 (successful) instead of 401