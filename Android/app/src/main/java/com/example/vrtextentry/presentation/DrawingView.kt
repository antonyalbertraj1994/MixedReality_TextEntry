package com.example.vrtextentry.presentation

import android.content.Context
import android.graphics.Bitmap
import android.graphics.Canvas
import android.graphics.Color
import android.graphics.Paint
import android.graphics.Path
import android.os.Environment
import android.util.AttributeSet
import android.view.MotionEvent
import android.view.View
import android.widget.ImageView
import java.io.File
import java.io.FileOutputStream

// Custom Drawing View
class DrawingView(context: Context, attrs: AttributeSet? = null) : View(context, attrs) {
    private lateinit var mainActivity:MainActivity

    private var drawPath: Path = Path()
    private var paint: Paint = Paint()
    private val paths = mutableListOf<Path>()
    private val paths_x = mutableListOf<Double>()
    private val paths_y = mutableListOf<Double>()
    private val twofingerdetect = false

    private var clear = false
    private var canvasBitmap: Bitmap? = null

    init {
        mainActivity = MainActivity()
        // Configure paint
        paint.color = Color.BLACK
        paint.style = Paint.Style.STROKE
        paint.strokeWidth = 8f
        paint.isAntiAlias = true
        paint.isDither = true
        paint.strokeJoin = Paint.Join.ROUND
        paint.strokeCap = Paint.Cap.ROUND
    }
    fun clearCanvas(){
        clear = true
        invalidate()

    }

    override fun onSizeChanged(w: Int, h: Int, oldw: Int, oldh: Int) {
        super.onSizeChanged(w, h, oldw, oldh)
        canvasBitmap = Bitmap.createBitmap(w, h, Bitmap.Config.ARGB_8888)
        println("Gemini:w,h: $w,$h")
    }

    override fun onDraw(canvas: Canvas) {
        super.onDraw(canvas)
        // Draw saved paths
        if(!clear) {
            for (path in paths) {
                canvas.drawPath(path, paint)
            }
            //canvas.drawBitmap(canvasBitmap!!, 0f, 0f, null)

            // Draw the current path
            canvas.drawPath(drawPath, paint)
        } else {
            canvas.drawColor(Color.WHITE)
            clear = false
            paths.clear()
        }
    }

    fun getx(): MutableList<Double> {
        return paths_x
    }

    fun gety(): MutableList<Double> {
        return paths_y
    }

    fun saveImage_Bitmap() {
        var drawCanvas: Canvas? = null
        drawCanvas = Canvas(canvasBitmap!!)
        drawCanvas.setBitmap(canvasBitmap)
        drawCanvas.drawColor(Color.WHITE)

        for (path in paths) {
            drawCanvas.drawPath(path, paint)
        }
        //drawCanvas.drawBitmap(canvasBitmap!!, 0f, 0f, null)

        val filename = "canvas_image.png"
        val file = File(context.filesDir, filename) // App-specific storage
        val bitmap: Bitmap? = canvasBitmap
        mainActivity.getGeminiResponse_Image("Dfsg", canvasBitmap!!)

//        val folder = File(Environment.getExternalStorageDirectory(), "MyCanvasImages")
//        if (!folder.exists()) {
//            folder.mkdirs() // Create the folder if it doesn't exist
//        }
//
//        val file = File(folder, "canvas_image.png")
//        try {
//            val outputStream = FileOutputStream(file)
//            bitmap?.compress(Bitmap.CompressFormat.PNG, 100, outputStream)
//            outputStream.flush()
//            outputStream.close()
//            println("Gemini: Image saved successfully at ${file.absolutePath}, ${file.length()}")
//        } catch (e: Exception) {
//            e.printStackTrace()
//            println("Failed to save image: ${e.message}")
//        }
        //canvasBitmap!!.eraseColor(Color.TRANSPARENT)

    }

    override fun onTouchEvent(event: MotionEvent): Boolean {
        val x = event.x
        val y = event.y
        val pointerCount = event.pointerCount // Number of fingers on the screen

        when (event.action) {
            MotionEvent.ACTION_DOWN -> {
                if(pointerCount == 1) {
                    drawPath.moveTo(x, y)
                    invalidate()
                }
            }
            MotionEvent.ACTION_MOVE -> {
                if(pointerCount == 1) {
                    drawPath.lineTo(x, y)
                    paths_x.add(x.toDouble())
                    paths_y.add(y.toDouble())
                    invalidate()
                }
            }
            MotionEvent.ACTION_UP, MotionEvent.ACTION_POINTER_UP  -> {
                if(pointerCount == 1) {
                    // Save the path to the list and reset the current path
                    paths.add(Path(drawPath))
                    paths_x.add(x.toDouble())
                    paths_y.add(y.toDouble())
                    drawPath.reset()
                    invalidate()
                } else if(pointerCount == 2) {
                    saveImage_Bitmap()
                    clearCanvas()
                }
            }
        }
        //return super.onTouchEvent(event)

        return true
    }
}
