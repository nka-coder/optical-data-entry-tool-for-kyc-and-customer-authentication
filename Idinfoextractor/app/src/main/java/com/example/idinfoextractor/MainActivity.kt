package com.example.idinfoextractor


import android.app.Activity
import android.content.Intent
import android.content.pm.PackageManager
import android.os.Bundle
import android.provider.MediaStore
import android.view.View
import android.widget.Button
import android.widget.EditText
import android.widget.Toast
import androidx.appcompat.app.AppCompatActivity


class MainActivity() : AppCompatActivity() {

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)
        setSupportActionBar(findViewById(R.id.toolbar))

        val goToCamera = findViewById<Button>(R.id.goToCamera)
        goToCamera.setOnClickListener {
            startActivity(Intent(this, ScanDocumentActivity::class.java))
        }

        val scanButton = findViewById<Button>(R.id.scanButton)
        scanButton.isEnabled = hasCamera()
    }

    private val VIDEO_CAPTURE =101
    fun startScanning(view: View){
        val intent = Intent(MediaStore.ACTION_VIDEO_CAPTURE)
        startActivityForResult(intent, VIDEO_CAPTURE)

    }
    private fun hasCamera(): Boolean {
        return packageManager.hasSystemFeature(
                PackageManager.FEATURE_CAMERA)
    }

    override fun onActivityResult(requestCode: Int, resultCode: Int, data: Intent?) {
        super.onActivityResult(requestCode, resultCode, data)

        val videoUri = data?.data
        if (requestCode == VIDEO_CAPTURE){
            if (resultCode == Activity.RESULT_OK){
                Toast.makeText(this, "Video saved to: \n"
                        +videoUri, Toast.LENGTH_LONG).show()
                    UploadUtility(this).uploadFile(videoUri) // Either Uri, File or String file path
                    val first_name = findViewById<EditText>(R.id.first_name)
                    first_name.setText("Adamou")
                    val name = findViewById<EditText>(R.id.name)
                    name.setText("")
                    val date_of_birth = findViewById<EditText>(R.id.date_of_birth)
                    date_of_birth.setText("")
                    val sex = findViewById<EditText>(R.id.sex)
                    sex.setText("")
                    val nationality = findViewById<EditText>(R.id.nationality)
                    nationality.setText("")
                    val country = findViewById<EditText>(R.id.country)
                    country.setText("")
                    val doc_type = findViewById<EditText>(R.id.doc_type)
                    doc_type.setText("")
                    val doc_number = findViewById<EditText>(R.id.doc_number)
                    doc_number.setText("")
                    val date_of_expiration = findViewById<EditText>(R.id.date_of_expiration)
                    date_of_expiration.setText("")

                startActivity(Intent(this, ScanDocumentActivity::class.java))
            }else if (resultCode == Activity.RESULT_CANCELED){
                Toast.makeText(this, "Video recording cancelled",
                        Toast.LENGTH_LONG).show()
            }else {
                Toast.makeText(this, "Failed to record video",
                        Toast.LENGTH_LONG).show()
            }
        }

    }

}



