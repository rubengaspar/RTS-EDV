using UnityEngine;
using System.Net.Sockets;
using System.Text;
using System.Threading;
using System.Collections.Generic;
using System;

public class HandTrackingReceiver : MonoBehaviour
{
    [SerializeField] public float multiplier = 20f;
    [SerializeField] public int hand_size = 21;
    
    private TcpClient client;
    private Thread clientThread;
    private bool isRunning = false;
    private List<HandPoint> handKeypoints = new List<HandPoint>();
    public GameObject[] handObjects; // Assign hand objects in the Unity Editor

    void Start()
    {
        clientThread = new Thread(new ThreadStart(ClientThread));
        clientThread.IsBackground = true;
        clientThread.Start();
    }

    void Update()
    {
        lock(handKeypoints)
        {
            // Debug.Log("handKeypoints.Count: " + handKeypoints.Count);
            if (handKeypoints.Count > 0)
            {
                
                foreach (var handPoint in handKeypoints)
                {
                    if (handPoint.id < hand_size)
                    {
                        handObjects[handPoint.id].transform.position = new Vector3(handPoint.x, 
                            handPoint.y, 
                            handPoint.z) * -multiplier;
                    }
                }
            }
        }    
    }

    private void ClientThread()
    {
        client = new TcpClient();

        try
        {
            client.Connect("127.0.0.1", 65432);
            isRunning = true;
            Debug.Log("Client connected");

            StringBuilder sb = new StringBuilder();

            while (isRunning)
            {
                if (client.Connected)
                {
                    NetworkStream stream = client.GetStream();
                    byte[] buffer = new byte[1024];
                    int bytesRead = stream.Read(buffer, 0, buffer.Length);
                    sb.Append(Encoding.UTF8.GetString(buffer, 0, bytesRead));

                   
                    string allData = sb.ToString();
                    int endOfMessageIndex = allData.IndexOf("\n");
                    if (endOfMessageIndex > -1)
                    {
                        string message = allData.Substring(0, endOfMessageIndex); 
                        sb = new StringBuilder(allData.Substring(endOfMessageIndex + 1)); 
                        if (!string.IsNullOrEmpty(message))
                        {
                            ParseMessage(message); 
                            Thread.Sleep(100);
                        }
                    }
                }
            }
        }
        catch (Exception e)
        {
            Debug.Log("Failed to Connect: " + e.Message);
        }
        client.Close();
    }

    private void ParseMessage(string message)
    {
        // Debug.Log("message: " + message);
        lock (handKeypoints)
        {
            try
            {
                // Debug.Log("Trying to Deserialize message into data");
                var wrapper = JsonUtility.FromJson<HandPointWrapper>("{\"handPoints\": " + message + '}');
                handKeypoints.Clear();
                handKeypoints = wrapper.handPoints;
                // Debug.Log("Successfully Deserialized");
                // Debug.Log("Hand Object: "+ wrapper);
                
            }
            catch (Exception e)
            {
                Debug.Log("Failed to parse message");
                Debug.LogError(e.StackTrace);
            }
        }
    }

    [Serializable]
    public class HandPointWrapper
    {
        public List<HandPoint> handPoints;
    }

    [Serializable]
    public class HandPoint
    {
        public int id;
        public float x;
        public float y;
        public float z;

        public override string ToString()
        {
            return $"id: {id}, ({x}, {y}, z)";
        }
    }

    void OnApplicationQuit()
    {
        isRunning = false;
        if (clientThread != null && clientThread.IsAlive)
        {
            clientThread.Abort();
        }
        if (client != null)
        {
            client.Close();
        }
    }
}