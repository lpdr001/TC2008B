// TC2008B Modelación de Sistemas Multiagentes con gráficas computacionales
// C# client to interact with Python server via POST
// Sergio Ruiz-Loza, Ph.D. March 2021

using System;
using System.Collections;
using System.Collections.Generic;
using UnityEditor;
using UnityEngine;
using UnityEngine.Networking;
using Newtonsoft.Json;

[Serializable]
public class CarData
{
    public float x;
    public float y;
    public float z;
    public float r;
}


[Serializable]
public class TrafficLightData
{
    public int status;
}

public class WebController : MonoBehaviour
{
    List<List<Vector4>> positions;
    List<List<int>> trafficLightStatus;

    public GameObject[] cars;
    public Light[] trafficLights;
    public float timeToUpdate = 1.0f;
    private float timer;
    public float dt;

    // IEnumerator - yield return
    IEnumerator SendData(string data)
    {
        WWWForm form = new WWWForm();
        form.AddField("bundle", "the data");
        string url = "http://localhost:8585/reto/trafficLights";
        //using (UnityWebRequest www = UnityWebRequest.Post(url, form))
        using (UnityWebRequest www = UnityWebRequest.Get(url))
        {
            byte[] bodyRaw = System.Text.Encoding.UTF8.GetBytes(data);
            www.uploadHandler = (UploadHandler)new UploadHandlerRaw(bodyRaw);
            www.downloadHandler = (DownloadHandler)new DownloadHandlerBuffer();
            //www.SetRequestHeader("Content-Type", "text/html");
            www.SetRequestHeader("Content-Type", "application/json");

            yield return www.SendWebRequest();          // Talk to Python
            if (www.isNetworkError || www.isHttpError)
            {
                Debug.Log(www.error);
            }
            else
            {
                //Debug.Log(www.downloadHandler.text);    // Answer from Python
                //Debug.Log("Form upload complete!");
                //Data tPos = JsonUtility.FromJson<Data>(www.downloadHandler.text.Replace('\'', '\"'));
                //Debug.Log(tPos);

                /*
                List<Vector4> newPositions = new List<Vector4>();
                string txt = www.downloadHandler.text.Replace('\'', '\"');
                Debug.Log(txt);
                txt = txt.TrimStart('"', '{', 'd', 'a', 't', 'a', ':', '[');
                txt = "{\"" + txt;
                txt = txt.TrimEnd(']', '}');
                txt = txt + '}';
                string[] strs = txt.Split(new string[] { "}, {" }, StringSplitOptions.None);
                Debug.Log("strs.Length:" + strs.Length);
                for (int i = 4; i < strs.Length; i++)
                {
                    strs[i] = strs[i].Trim();
                    if (i == 0) strs[i] = strs[i] + '}';
                    else if (i == strs.Length - 1) strs[i] = '{' + strs[i];
                    else strs[i] = '{' + strs[i] + '}';
                    Vector4 test = JsonUtility.FromJson<Vector4>(strs[i]);
                    Debug.Log("Resultado json"+test);
                    newPositions.Add(test);
                }

                List<Vector4> poss = new List<Vector4>();
                for (int s = 0; s < cars.Length; s++)
                {
                    //cars[s].transform.localPosition = newPositions[s];
                    poss.Add(newPositions[s]);
                }
                positions.Add(poss);
                */
                List<TrafficLightData> trafficLightData = JsonConvert.DeserializeObject<List<TrafficLightData>>(www.downloadHandler.text);
                List<int> ss = new List<int>();
                for (int i = 0; i < trafficLightData.Count; i++) 
                {
                    int s = 0 + trafficLightData[i].status;
                    ss.Add(s);
                }
                trafficLightStatus.Add(ss);
            }
        }

    }

    IEnumerator SendData2(string data)
    {
        WWWForm form = new WWWForm();
        form.AddField("bundle", "the data");
        string url = "http://localhost:8585/reto/cars";
        //using (UnityWebRequest www = UnityWebRequest.Post(url, form))
        using (UnityWebRequest www = UnityWebRequest.Get(url))
        {
            byte[] bodyRaw = System.Text.Encoding.UTF8.GetBytes(data);
            www.uploadHandler = (UploadHandler)new UploadHandlerRaw(bodyRaw);
            www.downloadHandler = (DownloadHandler)new DownloadHandlerBuffer();
            //www.SetRequestHeader("Content-Type", "text/html");
            www.SetRequestHeader("Content-Type", "application/json");

            yield return www.SendWebRequest();          // Talk to Python
            if (www.isNetworkError || www.isHttpError)
            {
                Debug.Log(www.error);
            }
            else
            {
                //Debug.Log(www.downloadHandler.text);    // Answer from Python
                //Debug.Log("Form upload complete!");
                //Data tPos = JsonUtility.FromJson<Data>(www.downloadHandler.text.Replace('\'', '\"'));
                //Debug.Log(tPos);

                /*
                List<Vector4> newPositions = new List<Vector4>();
                string txt = www.downloadHandler.text.Replace('\'', '\"');
                Debug.Log(txt);
                txt = txt.TrimStart('"', '{', 'd', 'a', 't', 'a', ':', '[');
                txt = "{\"" + txt;
                txt = txt.TrimEnd(']', '}');
                txt = txt + '}';
                string[] strs = txt.Split(new string[] { "}, {" }, StringSplitOptions.None);
                Debug.Log("strs.Length:" + strs.Length);
                for (int i = 4; i < strs.Length; i++)
                {
                    strs[i] = strs[i].Trim();
                    if (i == 0) strs[i] = strs[i] + '}';
                    else if (i == strs.Length - 1) strs[i] = '{' + strs[i];
                    else strs[i] = '{' + strs[i] + '}';
                    Vector4 test = JsonUtility.FromJson<Vector4>(strs[i]);
                    Debug.Log("Resultado json"+test);
                    newPositions.Add(test);
                }

                List<Vector4> poss = new List<Vector4>();
                for (int s = 0; s < cars.Length; s++)
                {
                    //cars[s].transform.localPosition = newPositions[s];
                    poss.Add(newPositions[s]);
                }
                positions.Add(poss);
                */
                List<CarData> carData = JsonConvert.DeserializeObject<List<CarData>>(www.downloadHandler.text);
                List<Vector4> poss = new List<Vector4>();
                for (int i = 0; i < carData.Count; i++) 
                {
                    Vector4 pos = new Vector4(carData[i].x, carData[i].y, carData[i].z, carData[i].r);
                    poss.Add(pos);
                }
                positions.Add(poss);

                
            }
        }

    }

    // Start is called before the first frame update
    void Start()
    {
        positions = new List<List<Vector4>>();
        trafficLightStatus = new List<List<int>>();
        Debug.Log(cars.Length);
#if UNITY_EDITOR
        //string call = "WAAAAASSSSSAAAAAAAAAAP?";
        Vector4 fakePos = new Vector4(3.44f, 0, -15.707f, 0);
        string json = EditorJsonUtility.ToJson(fakePos);
        //StartCoroutine(SendData(call));
        StartCoroutine(SendData(json));
        StartCoroutine(SendData2(json));
        timer = timeToUpdate;
#endif
    }

    // Update is called once per frame
    void Update()
    {
        /*
         *    5 -------- 100
         *    timer ----  ?
         */
        timer -= Time.deltaTime;
        dt = 1.0f - (timer / timeToUpdate);

        if(timer < 0)
        {
#if UNITY_EDITOR
            timer = timeToUpdate; // reset the timer
            Vector4 fakePos = new Vector4(3.44f, 0, -15.707f, 0);
            string json = EditorJsonUtility.ToJson(fakePos);
            StartCoroutine(SendData(json));
            StartCoroutine(SendData2(json));
#endif
        }


        if (positions.Count > 1)
        {

            for (int s = 0; s < cars.Length; s++)
            {
                // Get the last position for s
                List<Vector4> last = positions[positions.Count - 1];
                // Get the previous to last position for s
                List<Vector4> prevLast = positions[positions.Count - 2];
                // Interpolate using dt
                //Vector3 interpolated = Vector3.Lerp(prevLast[s], last[s], dt);
                float x = positions[positions.Count-1][s][0];
                float y = positions[positions.Count-1][s][1];
                float z = positions[positions.Count-1][s][2];
                cars[s].transform.position = new Vector3(x, y, z);
                //cars[s].transform.Rotation(0, 90*positions[positions.Count-1][s][3], 0);
                cars[s].transform.localRotation = Quaternion.Euler(0, 90*(positions[positions.Count-1][s][3]-1), 0);
                //cars[s].transform.RotateAround(transform.position, transform.up, positions[positions.Count-1][s][3]);

                //Vector3 dir = last[s] - prevLast[s];
                //cars[s].transform.rotation = Quaternion.LookRotation(dir);
            }
        }
    }
}
