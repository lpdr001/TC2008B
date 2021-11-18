using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class Luces : MonoBehaviour
{

    public GameObject red;
    public GameObject green;
    public GameObject yellow; 
    // Start is called before the first frame update
    void Start()
    {

        StartCoroutine(ActivationRoutine());

    }

    private IEnumerator ActivationRoutine(){


        green.SetActive(false);
        yellow.SetActive(false);
        red.SetActive(true);


        yield return new WaitForSeconds(5);
        red.SetActive(false);
        green.SetActive(true);


        yield return new WaitForSeconds(5);
        green.SetActive(false);
        yellow.SetActive(true);


        yield return new WaitForSeconds(3);
        yellow.SetActive(false);
        red.SetActive(true);


    }
}
