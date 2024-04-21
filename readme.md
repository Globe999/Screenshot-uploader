# Flask File Upload Application

This is a simple Flask application that allows for file uploads.

## Features

- File upload with basic API key authentication.
- Only allows certain file types to be uploaded: txt, pdf, png, jpg, jpeg, gif.
- Files are saved in an `uploads` directory.
- Uploaded files can be accessed via the `/i/<filename>` route.
- The server listens on port 6500.

## Environment Variables

The application uses the following environment variables:

- `SECRET_KEY`: The secret key for the Flask application. This is used for session management.
- `API_KEY`: The API key for authenticating file upload requests.

These environment variables should be set in a `.env` file in the same directory as your application.

## Running the Application

To run the application, use the following command:

```bash
python app.py