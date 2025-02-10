package com.yourapp.aviator;

import android.os.Bundle;
import android.widget.TextView;
import androidx.appcompat.app.AppCompatActivity;

public class MainActivity extends AppCompatActivity {
    private AviatorMultiplierReader aviatorReader;
    private ClockDisplay clockDisplay;

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

        // Initialize and start clock display
        TextView clockTextView = findViewById(R.id.clockTextView);
        clockDisplay = new ClockDisplay(clockTextView);
    }

    @Override
    protected void onDestroy() {
        super.onDestroy();
        if (clockDisplay != null) {
            clockDisplay.stopClock();
        }
    }
}
