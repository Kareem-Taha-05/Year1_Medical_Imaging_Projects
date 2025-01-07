using UnityEngine;

public class RandomizePositionAndRotation : MonoBehaviour
{
    // Define the range for random positions
    public float positionRange = 2f;

    // Define the range for random rotations (in degrees)
    public float rotationRange = 30f;

    void Start()
    {
        // Randomize the position within a small range
        float randomX = Random.Range(-positionRange, positionRange);
        float randomY = Random.Range(-positionRange, positionRange);
        float randomZ = Random.Range(-positionRange, positionRange);
        transform.position += new Vector3(randomX, randomY, randomZ);

        // Randomize the rotation within a small range
        float randomRotX = Random.Range(-rotationRange, rotationRange);
        float randomRotY = Random.Range(-rotationRange, rotationRange);
        float randomRotZ = Random.Range(-rotationRange, rotationRange);
        transform.rotation = Quaternion.Euler(randomRotX, randomRotY, randomRotZ);
    }
}
