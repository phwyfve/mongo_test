# React File Management WebApp

## 🚀 Setup Instructions

### 1. Install Dependencies
```bash
cd webapp
npm install
```

### 2. Start Development Server
```bash
# Make sure your FastAPI server is running first:
# In the main directory: uvicorn main:app --reload

# Then start React (from webapp directory):
npm start
```

The React app will start on http://localhost:3000 and proxy API calls to your FastAPI server on http://localhost:8000.

## 🎯 Features

### ✅ Authentication
- **Single Email Field**: Just enter email, password is hardcoded as "password123"
- **Login**: Authenticate existing users
- **Register**: Create new users (works even if user exists)
- **Auto-redirect**: Authenticated users go to files, unauthenticated go to login
- **Session Management**: Token stored in sessionStorage, cleared on logout

### ✅ Protected File Management
- **JWT Protection**: All file routes require valid authentication
- **File List**: Displays mock file data for authenticated users
- **CRUD Operations**: Upload, Edit, Delete (all mocked but return proper responses)
- **Automatic Logout**: Invalid tokens redirect to login page

### ✅ Protected API Routes
- `GET /api/files` - List user files (protected)
- `POST /api/files/upload` - Upload file (protected) 
- `PUT /api/files/{id}` - Update file (protected)
- `DELETE /api/files/{id}` - Delete file (protected)

## 📱 User Flow

1. **Visit App**: Redirected to login if not authenticated
2. **Login/Register**: Enter email, click Login or Register
3. **File Management**: View files, perform operations
4. **Logout**: Clears session, redirects to login

## 🛠️ Technical Details

- **React 18** with React Router for navigation
- **Axios** for API calls with automatic JWT headers
- **sessionStorage** for token persistence (cleared on tab close)
- **Proxy** configured to forward API calls to FastAPI backend
- **Context API** for global authentication state
- **Protected Routes** that check authentication before rendering

## 🧪 Testing

Try these scenarios:
- Login with existing user: `outrunner@live.fr`
- Register new user: any new email
- Test protected routes without authentication (should redirect to login)
- Logout and verify you can't access files without re-authenticating

---

**Perfect foundation for a production file management system!** 🎉
