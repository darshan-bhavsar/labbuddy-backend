# LabBuddy - Pathology Lab Management System

A comprehensive FastAPI-based system for managing pathology lab operations, patient data, and hospital communications.

## Features

### Core Functionality
- **Hospital Management**: Add, update, and manage hospital partnerships
- **Patient Management**: Comprehensive patient data with medical claim tracking
- **Test Management**: Master test catalog with lab-specific test offerings
- **Report Management**: End-to-end report lifecycle tracking
- **Notification System**: Real-time notifications for status changes
- **File Upload**: Secure report file storage with S3 integration

### User Roles
- **Lab Admin**: Full system access, can manage labs, hospitals, and users
- **Lab Staff**: Can manage patients, reports, and test results
- **Lab Boy**: Can update report collection and delivery status
- **Hospital User**: Can view reports and patient data for their hospital
- **Patient**: Can view their own reports and data

## Tech Stack

- **Backend**: FastAPI, SQLAlchemy, PostgreSQL
- **Authentication**: JWT with role-based access control
- **File Storage**: AWS S3 integration
- **Database Migrations**: Alembic
- **Notifications**: Email service integration ready

## Project Structure

```
labbuddy-backend/
├── app/
│   ├── main.py              # FastAPI application entry point
│   ├── config.py            # Configuration settings
│   ├── database.py          # Database connection and session
│   ├── models/              # SQLAlchemy models
│   │   ├── user.py
│   │   ├── lab.py
│   │   ├── hospital.py
│   │   ├── patient.py
│   │   ├── test.py
│   │   ├── report.py
│   │   └── notification.py
│   ├── schemas/             # Pydantic schemas for validation
│   ├── routers/             # API route handlers
│   ├── services/            # Business logic services
│   └── utils/               # Authentication and security utilities
├── alembic/                 # Database migrations
├── requirements.txt
└── README.md
```

## Setup Instructions

### 1. Environment Setup

```bash
# Clone the repository
git clone <repository-url>
cd labbuddy-backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Database Setup

```bash
# Install PostgreSQL and create database
createdb labbuddy_db

# Copy environment file
cp env.example .env

# Edit .env with your database credentials
# DATABASE_URL=postgresql://username:password@localhost:5432/labbuddy_db
```

### 3. Database Migrations

```bash
# Initialize Alembic (if not already done)
alembic init alembic

# Create initial migration
alembic revision --autogenerate -m "Initial migration"

# Apply migrations
alembic upgrade head
```

### 4. Run the Application

```bash
# Development server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Or use the main.py directly
python app/main.py
```

The API will be available at:
- **API**: http://localhost:8000
- **Documentation**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health

## API Endpoints

### Authentication
- `POST /api/v1/auth/register` - Register new user
- `POST /api/v1/auth/login` - Login and get token
- `GET /api/v1/auth/me` - Get current user info

### Labs
- `POST /api/v1/labs/` - Create lab (Lab Admin only)
- `GET /api/v1/labs/` - List all labs
- `GET /api/v1/labs/{lab_id}` - Get specific lab
- `PUT /api/v1/labs/{lab_id}` - Update lab
- `DELETE /api/v1/labs/{lab_id}` - Delete lab

### Hospitals
- `POST /api/v1/hospitals/` - Create hospital
- `GET /api/v1/hospitals/` - List hospitals
- `GET /api/v1/hospitals/{hospital_id}` - Get specific hospital
- `PUT /api/v1/hospitals/{hospital_id}` - Update hospital
- `DELETE /api/v1/hospitals/{hospital_id}` - Delete hospital

### Patients
- `POST /api/v1/patients/` - Create patient
- `GET /api/v1/patients/` - List patients
- `GET /api/v1/patients/{patient_id}` - Get specific patient
- `PUT /api/v1/patients/{patient_id}` - Update patient
- `DELETE /api/v1/patients/{patient_id}` - Delete patient

### Reports
- `POST /api/v1/reports/` - Create report booking
- `GET /api/v1/reports/` - List reports
- `GET /api/v1/reports/{report_id}` - Get specific report
- `PUT /api/v1/reports/{report_id}` - Update report status
- `POST /api/v1/reports/{report_id}/upload` - Upload report file
- `GET /api/v1/reports/{report_id}/files` - Get report files

### Tests
- `GET /api/v1/tests/master` - List master tests
- `POST /api/v1/tests/lab` - Add test to lab
- `GET /api/v1/tests/lab/{lab_id}` - Get lab's available tests
- `PUT /api/v1/tests/lab/{lab_test_id}` - Update lab test
- `DELETE /api/v1/tests/lab/{lab_test_id}` - Remove test from lab

## Configuration

### Environment Variables

```env
# Database
DATABASE_URL=postgresql://username:password@localhost:5432/labbuddy_db

# JWT
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# AWS S3 (for file uploads)
AWS_ACCESS_KEY_ID=your-aws-access-key
AWS_SECRET_ACCESS_KEY=your-aws-secret-key
AWS_BUCKET_NAME=your-bucket-name
AWS_REGION=us-east-1

# Email (for notifications)
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your-email@gmail.com
SMTP_PASSWORD=your-app-password

# Redis (for Celery)
REDIS_URL=redis://localhost:6379/0

# App Settings
APP_NAME=LabBuddy
DEBUG=True
```

## Development

### Adding New Features

1. **Models**: Add new SQLAlchemy models in `app/models/`
2. **Schemas**: Add Pydantic schemas in `app/schemas/`
3. **Routes**: Add API routes in `app/routers/`
4. **Services**: Add business logic in `app/services/`
5. **Migrations**: Generate and apply database migrations

### Database Migrations

```bash
# Create new migration
alembic revision --autogenerate -m "Description of changes"

# Apply migrations
alembic upgrade head

# Rollback migration
alembic downgrade -1
```

## Security Considerations

- JWT tokens for authentication
- Role-based access control
- Password hashing with bcrypt
- File upload validation
- CORS configuration for production
- Environment variable management

## Future Enhancements

- [ ] Email notification service integration
- [ ] SMS notifications
- [ ] Advanced analytics dashboard
- [ ] Billing and payment integration
- [ ] Mobile app API endpoints
- [ ] Real-time notifications with WebSockets
- [ ] Advanced reporting and analytics
- [ ] Multi-tenant architecture
- [ ] API rate limiting
- [ ] Comprehensive logging and monitoring

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License.
