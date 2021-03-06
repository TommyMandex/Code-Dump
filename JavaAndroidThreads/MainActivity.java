package com.hivemind.zerodavila.threads;

import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.view.View;
import android.widget.TextView;
import android.os.Handler;
import android.os.Message;


public class MainActivity extends AppCompatActivity {

    Handler handler = new Handler() {
        @Override
        public void handleMessage(Message msg) {
            TextView myText = (TextView) findViewById(R.id.myText);
            myText.setText("10 seconds have passed.");
        }
    };

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
    }

    public void clickMyButton(View view) {

        Runnable r = new Runnable() {
            @Override
            public void run() {
                long futureTime = System.currentTimeMillis() + 10000;
                while(System.currentTimeMillis() < futureTime) {
                    synchronized (this) {
                        try {
                            wait(futureTime - System.currentTimeMillis());
                        } catch (Exception e) {

                        }
                    }
                }
                handler.sendEmptyMessage(0);
            }
        };

        Thread myThread = new Thread(r);
        myThread.start();
    }
}
