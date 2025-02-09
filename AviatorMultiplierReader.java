package com.yourapp.aviator;

import android.content.Context;
import android.util.Log;
import java.io.BufferedReader;
import java.io.File;
import java.io.FileReader;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.util.ArrayList;
import java.util.List;

public class AviatorMultiplierReader {
    private static final String TAG = "AviatorMultiplierReader";
    private static final String FILE_NAME = "aviator_multipliers.csv";

    private Context context;

    public AviatorMultiplierReader(Context context) {
        this.context = context;
    }

    // Read CSV from assets folder
    public List<String[]> readCSVFromAssets() {
        List<String[]> multiplierList = new ArrayList<>();
        try {
            InputStream inputStream = context.getAssets().open(FILE_NAME);
            BufferedReader reader = new BufferedReader(new InputStreamReader(inputStream));

            String line;
            while ((line = reader.readLine()) != null) {
                String[] row = line.split(",");
                multiplierList.add(row);
            }

            reader.close();
        } catch (Exception e) {
            Log.e(TAG, "Error reading CSV from assets: " + e.getMessage());
        }
        return multiplierList;
    }

    // Read CSV from internal storage
    public List<String[]> readCSVFromInternalStorage() {
        List<String[]> multiplierList = new ArrayList<>();
        try {
            File file = new File(context.getFilesDir(), FILE_NAME);
            if (!file.exists()) {
                Log.e(TAG, "CSV file not found in internal storage.");
                return multiplierList;
            }

            BufferedReader reader = new BufferedReader(new FileReader(file));
            String line;
            while ((line = reader.readLine()) != null) {
                String[] row = line.split(",");
                multiplierList.add(row);
            }
            reader.close();
        } catch (Exception e) {
            Log.e(TAG, "Error reading CSV from internal storage: " + e.getMessage());
        }
        return multiplierList;
    }

    // Auto-update CSV data every X minutes
    public void startAutoUpdate(int intervalMinutes) {
        new Thread(() -> {
            while (true) {
                List<String[]> data = readCSVFromInternalStorage();
                Log.d(TAG, "Updated CSV Data: " + data.size() + " entries");

                try {
                    Thread.sleep(intervalMinutes * 60 * 1000); // Sleep for X minutes
                } catch (InterruptedException e) {
                    Log.e(TAG, "Auto-update thread interrupted: " + e.getMessage());
                }
            }
        }).start();
    }
}
