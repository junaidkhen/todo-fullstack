# Database Migration Required

The backend Task model has been updated with new fields:
- `priority` (string): Low, Medium, or High
- `category` (string): Work, Personal, Health, Shopping, Finance, Other
- `due_date` (datetime): Task due date

## How to Update the Database

Since we're using SQLModel, the easiest way is to drop and recreate the database:

### Option 1: Drop existing database (simplest for development)

```bash
cd backend
# Delete the existing database file (if using SQLite)
rm -f *.db

# Start the server - it will create a new database with the updated schema
python3 -m uvicorn main:app --reload
```

### Option 2: Manual migration

If you want to keep existing data, you can manually add the columns:

```sql
ALTER TABLE tasks ADD COLUMN priority VARCHAR(20) DEFAULT 'Medium';
ALTER TABLE tasks ADD COLUMN category VARCHAR(50);
ALTER TABLE tasks ADD COLUMN due_date TIMESTAMP;
```

After updating the database, restart both the backend and frontend servers.
