# Kountifi-tasks

1. **Added PostgreSQL Integration**:
   - SQLAlchemy for ORM
   - Proper database session management
   - Table creation on startup

2. **Separated Concerns**:
   - Database models in `models.py`
   - Pydantic schemas in `schemas.py`
   - Database operations in `crud.py`

3. **Background Tasks with DB**:
   - Pass the database session to background tasks
   - Proper session handling in async context


To test this, you'll need to:
1. Have PostgreSQL running
2. Create the database
3. Run the application (uvicorn main:app --reload --port $APP_PORT )
4. test the endpoints in The Postman 
    - POST http://localhost:APP_PORT/upload
    - POST http://localhost:APP_PORT/process
    - GET http://localhost:APP_PORT/status/your-job-id


## Additional Recommendations

1. Install required packages:
```bash
pip install -r requirements.txt

