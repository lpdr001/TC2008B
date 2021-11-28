using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class Movement : MonoBehaviour
{
    public GameObject car;
    Vector3[] positions;
    public Vector3 startP;
    public Vector3 endP;
    public float t;

    Vector3[] applyTransform() {
        Vector3 p = startP + t * (startP-endP);
        Matrix4x4 tm = Transformations.TranslateM(p.x,p.y,p.z);
        Vector3[] transform = new Vector3[positions.Length];

        for (int i = 0; i < positions.Length; i++) {
            Vector3 v = positions[i];
            Vector4 temp = new Vector4(p.x, p.y, p.z, 1);
            transform[i] = tm * temp;
        }

        return transform;

    }


    // Start is called before the first frame update
    void Start()
    {
        t = 0;
        Vector3 currPos = car.transform.position;
        startP = new Vector3(currPos.x + Random.Range(-2f, 4f), currPos.y, currPos.z + Random.Range(-4f, 4f));
        endP = new Vector3(currPos.x + Random.Range(-4f, 4f), currPos.y, currPos.z + Random.Range(-4f, 4f));
        MeshFilter mf = car.GetComponent<MeshFilter>();
        Mesh mesh = mf.mesh;
        positions = mesh.vertices;
    }

    // Update is called once per frame
    void Update()
    {
        MeshFilter mf = car.GetComponent<MeshFilter>();
        Mesh mesh = mf.mesh;
        t += 0.1f;
        mesh.vertices = applyTransform();
    }
}
