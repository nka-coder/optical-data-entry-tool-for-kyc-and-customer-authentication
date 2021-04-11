package com.example.idinfoextractor

import android.content.Intent
import android.os.Bundle
import android.widget.Button
import android.widget.EditText
import android.widget.Toast
import androidx.appcompat.app.AppCompatActivity

class ScanDocumentActivity: AppCompatActivity() {

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.scan_identity_document)


        val goToCamera = findViewById<Button>(R.id.goToCameraToRescan)

        goToCamera.setOnClickListener {
            startActivity(Intent(this, MainActivity::class.java))
        }

        val screen = findViewById<Button>(R.id.screen)

        screen.setOnClickListener {
            Toast.makeText(this, "This service is not available yet!",Toast.LENGTH_LONG).show()
        }

        val close = findViewById<Button>(R.id.close)

        close.setOnClickListener {
            startActivity(Intent(this, MainActivity::class.java))
        }
    }



}