using UnityEngine;

public class CameraController : MonoBehaviour
{
    public Transform target; // The target the camera orbits and zooms towards
    public float rotationSpeed = 500.0f;

    public float zoomSpeed = 10.0f;
    public float minZoomDistance = 2.0f; // Minimum distance to the target
    public float maxZoomDistance = 50.0f; // Maximum distance to the target

    private float currentZoomDistance;

    void Start()
    {
        // Calculate the initial distance from the camera to the target
        currentZoomDistance = Vector3.Distance(transform.position, target.position);
    }

    void Update()
    {
        // Handle rotation around the target when the right mouse button is held down
        if (Input.GetMouseButton(1)) // Right mouse button pressed
        {
            float horizontalInput = Input.GetAxis("Mouse X") * rotationSpeed * Time.deltaTime;
            float verticalInput = Input.GetAxis("Mouse Y") * rotationSpeed * Time.deltaTime;

            // Rotate horizontally around the target
            transform.RotateAround(target.position, Vector3.up, horizontalInput);

            // Allow vertical movement (up and down)
            transform.RotateAround(target.position, transform.right, -verticalInput); // Use negative to match intuitive movement

            // Recalculate the direction for proper zoom orientation
            currentZoomDistance = Vector3.Distance(transform.position, target.position);
        }

        // Handle zoom towards the target
        float scroll = Input.GetAxis("Mouse ScrollWheel");
        if (scroll != 0)
        {
            currentZoomDistance -= scroll * zoomSpeed;
            currentZoomDistance = Mathf.Clamp(currentZoomDistance, minZoomDistance, maxZoomDistance);

            // Recalculate camera position based on current direction and zoom distance
            Vector3 direction = (transform.position - target.position).normalized;
            transform.position = target.position + direction * currentZoomDistance;
        }
    }
}
