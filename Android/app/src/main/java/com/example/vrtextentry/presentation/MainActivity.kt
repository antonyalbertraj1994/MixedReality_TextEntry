/* While this template provides a good starting point for using Wear Compose, you can always
 * take a look at https://github.com/android/wear-os-samples/tree/main/ComposeStarter to find the
 * most up to date changes to the libraries and their usages.
 */

package com.example.vrtextentry.presentation


import android.annotation.SuppressLint
import android.content.Context
import android.graphics.Bitmap
import android.graphics.BitmapFactory
import android.net.Uri
import android.os.Bundle
import android.view.InputDevice
import android.view.MotionEvent
import android.view.View
import android.view.WindowManager
import android.widget.Button
import android.widget.FrameLayout
import android.widget.ImageView
import androidx.activity.ComponentActivity
import androidx.compose.foundation.background
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.runtime.Composable
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.res.stringResource
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.tooling.preview.Preview
import androidx.wear.compose.material.MaterialTheme
import androidx.wear.compose.material.Text
import androidx.wear.compose.material.TimeText
import androidx.wear.tooling.preview.devices.WearDevices
import androidx.wear.widget.SwipeDismissFrameLayout
import com.example.vrtextentry.R
import com.example.vrtextentry.presentation.theme.VRTextEntryTheme
import com.google.ai.client.generativeai.BuildConfig
import com.google.ai.client.generativeai.GenerativeModel
import com.google.ai.client.generativeai.type.BlockThreshold
import com.google.ai.client.generativeai.type.Content
import com.google.ai.client.generativeai.type.GenerateContentResponse
import com.google.ai.client.generativeai.type.GenerationConfig
import com.google.ai.client.generativeai.type.HarmCategory
import com.google.ai.client.generativeai.type.SafetySetting
import com.google.ai.client.generativeai.type.TextPart
import com.google.ai.client.generativeai.type.content
import com.google.ai.client.generativeai.type.generationConfig
import kotlinx.coroutines.CoroutineScope
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.launch
import kotlinx.coroutines.withContext
import java.io.File
import java.io.InputStream


class MainActivity : ComponentActivity() {

    lateinit var drawview: DrawingView
    private lateinit var socketClient: com.example.vrtextentry.presentation.Socket
    private lateinit var flashbutton: Button
    private lateinit var frameLayout: FrameLayout
    private lateinit var generativeModel: GenerativeModel
    private val apiKey = "AIzaSyD1YyuLBOAPEAxcPfsl49JPFpI0M5k8H3c"  // Replace with your actual API key
    private val modelName = "gemini-1.5-flash" // Or use "gemini-pro-vision" for multimodal
    private lateinit var imageView: ImageView

    override fun onCreate(savedInstanceState: Bundle?) {

        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)

        drawview = DrawingView(this)
        frameLayout = findViewById(R.id.swipe)

        imageView = findViewById(R.id.imageView)


        socketClient = com.example.vrtextentry.presentation.Socket(this)



        //getGeminiResponse("What is the meaning of life?")
        frameLayout.addView(drawview)
        //loadImageFromAppSpecificStorage(this, "canvas_image.png", imageView)

        flashbutton = findViewById(R.id.flash)
        flashbutton.setOnClickListener {
            val host = "192.168.1.11" // Directly put the IP number shown by ipconfig command on Desktop
            val port = 9003
            socketClient.connectToServer(host, port)
            socketClient.sendData("Hello")

        }
        generativeModel = GenerativeModel(
            modelName = modelName,
            apiKey = apiKey,
        )
        //getGeminiResponse_Image("sdfs")

        flashbutton.visibility = View.INVISIBLE

        getWindow().addFlags(WindowManager.LayoutParams.FLAG_KEEP_SCREEN_ON);

    }

    fun socketsetup() {
        Thread.sleep(2000)
        val host = "192.168.1.10" // Directly put the IP number shown by ipconfig command on Desktop
        val port = 9002
        println("Connectingport")
        socketClient.connectToServer(host, port)
        socketClient.sendData("Hello")
    }

    override fun onGenericMotionEvent(event: MotionEvent?): Boolean {
        if (event?.action == MotionEvent.ACTION_SCROLL &&
            event.source and InputDevice.SOURCE_ROTARY_ENCODER == InputDevice.SOURCE_ROTARY_ENCODER
        ) {
            // Get the rotation direction.
            val delta = -event.getAxisValue(MotionEvent.AXIS_SCROLL)

            // Positive delta = clockwise rotation, Negative delta = counterclockwise rotation.
            //handleCrownRotation(delta)
            send_lightvalue()
            drawview.clearCanvas()

            return true
        }
        return super.onGenericMotionEvent(event)
    }

    fun loadImageFromAppSpecificStorage(context: Context, fileName: String, imageView: ImageView): Bitmap {
        var canvasBitmap = Bitmap.createBitmap(456, 456, Bitmap.Config.ARGB_8888)

        val file = File(context.filesDir, fileName)
        if (file.exists()) {
            val bitmap = BitmapFactory.decodeFile(file.absolutePath)

            imageView.setImageBitmap(bitmap)
            println("Gemini: Image loaded successfully from ${file.absolutePath}")
            canvasBitmap = bitmap
        } else {
            println("Image file does not exist: ${file.absolutePath}")
        }
        return canvasBitmap
    }

    fun loadImage(context: Context, fileName: String):Bitmap {
        var canvasBitmap = Bitmap.createBitmap(456, 456, Bitmap.Config.ARGB_8888)

        val file = File(context.filesDir, fileName)
        if (file.exists()) {
            val bitmap = BitmapFactory.decodeFile(file.absolutePath)
            println("Gemini1: Image loaded successfully from ${file.absolutePath}")
            canvasBitmap = bitmap
        } else {
            println("Image file does not exist: ${file.absolutePath}")
        }
        return canvasBitmap
    }

    fun send_lightvalue() {
        //sending = true
//        val path_x = drawview.getx()
//        val path_y = drawview.gety()
//
//        println("Sendsize:$path_x.size")

        //val iterator = mutablelist.listIterator()
//        var i = 0
//        var len = path_y.size
//        while (i < len) {
//            val x = path_x.get(i).toInt()
//            val y = path_y.get(i).toInt()
//            val sendstring = "$x,$y"
//            println("send:$sendstring")
//            i++;
//            socketClient.sendData(sendstring)
//
//        }
        //println("sending")
        socketClient.sendData("Hellow")

    }

    private fun getGeminiResponse(prompt: String) {
        CoroutineScope(Dispatchers.IO).launch {
            try{
                val response = generativeModel.generateContent(
                    Content(parts = listOf(TextPart(prompt)))
                )

                handleResponse(response)
            }
            catch (e:Exception){
                handleError(e)
            }

        }
    }

    fun getGeminiResponse_Image(prompt: String, image: Bitmap ) {
        val context = this
        //var image = loadImage(context, "canvas_image.png")
        println("Gemini started1")
        generativeModel = GenerativeModel(
            modelName = modelName,
            apiKey = apiKey,
        )
        println("Gemini started2")

        CoroutineScope(Dispatchers.IO).launch {
            try{

//                val response = generativeModel.generateContent(
//                    Content(parts = listOf(TextPart(prompt)))
//                )

                val response = generativeModel.generateContent(
                    content{
                        image(image)
                        text("Important: Only return a single english alphabet. Only a single character and nothing else. \\n It is not a number.\"?")
                    }
                )

                handleResponse(response)
            }
            catch (e:Exception){
                handleError(e)
            }

        }
    }

    private suspend fun handleResponse(response: GenerateContentResponse){
        withContext(Dispatchers.Main){
            // Update UI with the response
            val text = response.text
            println("Gemini Response: $text")

        }
    }

    private suspend fun handleError(e:Exception){
        withContext(Dispatchers.Main){
            println("Gemini: Error generating content ${e.message}")
        }
    }

}


