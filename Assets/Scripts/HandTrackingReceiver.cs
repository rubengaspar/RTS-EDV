using UnityEngine;
using System.Net.Sockets;
using System.Text;
using System.Threading;
using System.Collections.Generic;
using System;

public class HandTrackingReceiver : MonoBehaviour
{
    [SerializeField] public float multiplier = 10f;
    
    private TcpClient client;
    private Thread clientThread;
    private bool isRunning = false;
    private Dictionary<int, List<Vector3>> handKeypoints = new Dictionary<int, List<Vector3>>();
    public GameObject[] handObjects; // Assign hand objects in the Unity Editor

    void Start()
    {
        clientThread = new Thread(new ThreadStart(ClientThread));
        clientThread.IsBackground = true;
        clientThread.Start();
    }

    void Update()
    {
        lock (handKeypoints)
        {
            foreach (var kvp in handKeypoints)
            {
                int handIndex = kvp.Key;
                List<Vector3> keypoints = kvp.Value;

                if (handIndex < handObjects.Length && keypoints.Count > 0)
                {
                    // Update hand object transform
                    
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
                            ParseMessage(message.Trim()); 
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
        Debug.Log("message: " + message);
        lock (handKeypoints)
        {
            try
            {
                var data = JsonUtility.FromJson<HandData>(message);
                
                Debug.Log("Hand Object: "+ data);
                handKeypoints.Clear();

                for (int i = 0; i < data.hands.Count; i++)
                {
                    var keypoints = new List<Vector3>();
                    foreach (var point in data.hands[i])
                    {
                        keypoints.Add(new Vector3(point.x, point.y, point.z) * multiplier);
                    }
                    handKeypoints[i] = keypoints;
                }
            }
            catch (Exception e)
            {
                Debug.Log("Failed to parse message");
                Debug.LogError(e.StackTrace);
            }
        }
    }

[Serializable]
public class HandData
{
    public List<List<HandPoint>> hands;

    public override string ToString()
    {
        string allHands = "";
        for (int i = 0; i < hands.Count; i++)
        {
            string handPoints = "";
            for (int j = 0; j < hands[i].Count; j++)
            {
                handPoints += hands[i][j].ToString();
                if(j != hands[i].Count - 1) 
                    handPoints += ", ";
            }

            allHands += handPoints;
            if(i != hands.Count - 1) 
                allHands += " | ";
        }

        return $"HandData: {allHands}";
    }
}

    [Serializable]
    public class HandPoint
    {
        public float x;
        public float y;
        public float z;
        
        public override string ToString()
        {
            return $"x:{x}, y:{y}, z:{z}";
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
