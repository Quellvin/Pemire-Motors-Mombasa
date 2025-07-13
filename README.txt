# Pemire Motors Backend

## Features
- Upload car details via POST
- Store images using multer
- Serve car data via GET /cars
- MongoDB storage

## Setup
1. Run `npm install`
2. Create `public/uploads/` folder
3. Start server: `npm start`
4. MongoDB must be running (default: localhost:27017)

API:
- GET  /cars
- POST /cars (form-data: fields + images[])

Enjoy!