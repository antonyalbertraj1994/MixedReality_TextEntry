package com.example.vrtextentry.presentation

import java.io.*
import java.net.Socket
import kotlinx.coroutines.*

class Socket(private val activity: MainActivity) {

    private var socket: Socket? = null
    private var input: BufferedReader? = null
    private var output: PrintWriter? = null
    private var isRunning = true
    var mainactivity_instance = MainActivity()
    // Connect to the server
    fun connectToServer(host: String, port: Int) {
        CoroutineScope(Dispatchers.IO).launch {
            try {
                // Establish socket connection
                socket = Socket(host, port)
                input = BufferedReader(InputStreamReader(socket!!.getInputStream()))
                output = PrintWriter(socket!!.getOutputStream(), true)

                // Start reading and writing
                launch { readFromSocket() }
            } catch (e: Exception) {
                e.printStackTrace()
            }
        }
    }

    // Continuously read data from the socket
    private suspend fun readFromSocket() {
        try {
            while (isRunning) {
                //println("reading")
                val message = input?.readLine()

                if (message != null) {
                    withContext(Dispatchers.Main) {
                        println("Received: $message")
                        //Thread.sleep(10)

//                        activity.setBrightness(message.toInt())
//                        activity.send_brightness()

                        if(message == "1") {
                            activity.send_lightvalue()
                        }else if(message == "2") {
                            //activity.stop_sending()
                        }

                        //val light = activity.livedata.value
                        //sendData(light.toString())
                        // Update UI or process received data
                    }
                }
            }
        } catch (e: Exception) {
            e.printStackTrace()
        }
    }

    // Send data to the socket
    fun sendData(message: String) {

        CoroutineScope(Dispatchers.IO).launch {
            try {
                output?.println(message)
                println("Sent: $message")
            } catch (e: Exception) {
                e.printStackTrace()
            }
        }
    }

    // Close the socket and cleanup
    fun closeConnection() {
        isRunning = false
        input?.close()
        output?.close()
        socket?.close()
    }
}