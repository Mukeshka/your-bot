package com.yourapp.aviator;

import android.os.Bundle;
import android.util.Log;
import androidx.appcompat.app.AppCompatActivity;
import java.util.List;

public class MainActivity extends AppCompatActivity {
    private AviatorMultiplierReader aviatorReader;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        aviatorReader = new AviatorMultiplierReader(this);

        // Read and display multipliers from CSV
        List<String[]> multipliers = aviatorReader.readCSVFromInternalStorage();
        for (String[] row : multipliers) {
            Log.d("MainActivity", "Multiplier: " + row[0] + " at " + row[1]);
        }

        // Start auto-updating data every 5 minutes
        aviatorReader.startAutoUpdate(5);
    }
}
