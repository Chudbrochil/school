// Anthony Galczak - agalczak@cnm.edu
// CIS 2237 - Program 6 - Reminders

package com.cis2237.reminders.galczakp6;

import android.content.ContentValues;
import android.content.Context;
import android.database.Cursor;
import android.database.SQLException;
import android.database.sqlite.SQLiteDatabase;
import android.database.sqlite.SQLiteOpenHelper;
import android.support.design.widget.Snackbar;
import android.util.Log;
import android.view.View;

/**
 * Created by EQUUS on 11/10/2016.
 */
public class RemindersDbAdapter {

    //these are the column names
    public static final String COL_ID = "_id";
    public static final String COL_CONTENT = "content";
    public static final String COL_IMPORTANT = "important";
    //these are the corresponding indices
    public static final int INDEX_ID = 0;
    public static final int INDEX_CONTENT = INDEX_ID + 1;
    public static final int INDEX_IMPORTANT = INDEX_ID + 2;
    //used for logging
    private static final String TAG = "RemindersDbAdapter";
    private DatabaseHelper dbHelper;
    private SQLiteDatabase db;
    private static final String DATABASE_NAME = "dba_remdrs";
    private static final String TABLE_NAME = "tbl_remdrs";
    private static final int DATABASE_VERSION = 1;
    //SQL statement used to create the database
    private final Context mCtx;
    private static final String DATABASE_CREATE =
            "CREATE TABLE if not exists " + TABLE_NAME + " ( " +
                    COL_ID + " INTEGER PRIMARY KEY autoincrement, " +
                    COL_CONTENT + " TEXT, " +
                    COL_IMPORTANT + " INTEGER );";


    public RemindersDbAdapter(Context ctx) {
        this.mCtx = ctx;
    }
    //open the database
    public void open() throws SQLException {
        dbHelper = new DatabaseHelper(mCtx);
        db = dbHelper.getWritableDatabase();
    }
    //close the database
    public void close() {
        if (dbHelper != null) {
            dbHelper.close();
        }
    }

    //CREATE
    //note that the id will be created for you automatically
    public void createReminder(String name, boolean important) {
        ContentValues values = new ContentValues();
        values.put(COL_CONTENT, name);
        values.put(COL_IMPORTANT, important ? 1 : 0);
        db.insert(TABLE_NAME, null, values);
    }
    //overloaded to take a reminder
    public long createReminder(Reminder reminder) {
        ContentValues values = new ContentValues();
        values.put(COL_CONTENT, reminder.getContent()); // Contact Name
        values.put(COL_IMPORTANT, reminder.getImportant()); // Contact Phone Number
        // Inserting Row
        return db.insert(TABLE_NAME, null, values);
    }

    //READ
    public Reminder fetchReminderById(int id) {

        Cursor cursor = db.query(TABLE_NAME, new String[]{COL_ID,
                        COL_CONTENT, COL_IMPORTANT}, COL_ID + "=?",
                new String[]{String.valueOf(id)}, null, null, null, null
        );
        if (cursor != null)
            cursor.moveToFirst();
        return new Reminder(
                cursor.getInt(INDEX_ID),
                cursor.getString(INDEX_CONTENT),
                cursor.getInt(INDEX_IMPORTANT)
        );
    }
    public Cursor fetchAllReminders() {
        Cursor mCursor = db.query(TABLE_NAME, new String[]{COL_ID,
                        COL_CONTENT, COL_IMPORTANT},
                null, null, null, null, null
        );
        if (mCursor != null) {
            mCursor.moveToFirst();
        }
        return mCursor;
    }

    //UPDATE
    public void updateReminder(Reminder reminder) {
        ContentValues values = new ContentValues();
        values.put(COL_CONTENT, reminder.getContent());
        values.put(COL_IMPORTANT, reminder.getImportant());
        db.update(TABLE_NAME, values,
                COL_ID + "=?", new String[]{String.valueOf(reminder.getId())});
    }

    //DELETE
    public void deleteReminderById(int nId) {
        db.delete(TABLE_NAME, COL_ID + "=?", new String[]{String.valueOf(nId)});

    }


    public void deleteAllReminders() {
        db.delete(TABLE_NAME, null, null);
    }

    private static class DatabaseHelper extends SQLiteOpenHelper {
        DatabaseHelper(Context context) {
            super(context, DATABASE_NAME, null, DATABASE_VERSION);
        }

        @Override
        public void onCreate(SQLiteDatabase db) {
            Log.w(TAG, DATABASE_CREATE);
            db.execSQL(DATABASE_CREATE);
        }

        @Override
        public void onUpgrade(SQLiteDatabase db, int oldVersion, int newVersion) {
            Log.w(TAG, "Upgrading database from version " + oldVersion + " to "
                    + newVersion + ", which will destroy all old data");
            db.execSQL("DROP TABLE IF EXISTS " + TABLE_NAME);
            onCreate(db);
        }
    }
}