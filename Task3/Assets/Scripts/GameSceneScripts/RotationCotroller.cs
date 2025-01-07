using UnityEngine;

public class RotationController : MonoBehaviour
{
    public float rotationSpeed = 100f;  // Rotation speed
    public float movementSpeed = 0.1f;  // Movement speed for Z position adjustment
    public KeyCode rotateXAxisPositiveKey = KeyCode.W;  // Button to rotate forward around X-axis
    public KeyCode rotateXAxisNegativeKey = KeyCode.S;  // Button to rotate backward around X-axis
    public KeyCode rotateYAxisPositiveKey = KeyCode.A;  // Button to rotate forward around Y-axis
    public KeyCode rotateYAxisNegativeKey = KeyCode.D;  // Button to rotate backward around Y-axis
    public KeyCode rotateZAxisPositiveKey = KeyCode.Z;  // Button to rotate forward around Z-axis
    public KeyCode rotateZAxisNegativeKey = KeyCode.X;  // Button to rotate backward around Z-axis
    public KeyCode increaseZPositionKey = KeyCode.UpArrow;  // Button to increase Z position
    public KeyCode decreaseZPositionKey = KeyCode.DownArrow;  // Button to decrease Z position
    private GameObject selectedBrainPart;  // The currently selected brain part to rotate

    void Update()
    {
        // Ensure that a brain part is selected before rotating or moving
        if (selectedBrainPart != null)
        {
            // Rotate around the local X-axis in the positive direction when "R" is pressed
            if (Input.GetKey(rotateXAxisPositiveKey))
            {
                selectedBrainPart.transform.localRotation *= Quaternion.Euler(rotationSpeed * Time.deltaTime / 3, 0, 0);
            }

            // Rotate around the local X-axis in the negative direction when "F" is pressed
            if (Input.GetKey(rotateXAxisNegativeKey))
            {
                selectedBrainPart.transform.localRotation *= Quaternion.Euler(-rotationSpeed * Time.deltaTime / 3, 0, 0);
            }

            // Rotate around the local Y-axis in the positive direction when "T" is pressed
            if (Input.GetKey(rotateYAxisPositiveKey))
            {
                selectedBrainPart.transform.localRotation *= Quaternion.Euler(0, rotationSpeed * Time.deltaTime / 3, 0);
            }

            // Rotate around the local Y-axis in the negative direction when "G" is pressed
            if (Input.GetKey(rotateYAxisNegativeKey))
            {
                selectedBrainPart.transform.localRotation *= Quaternion.Euler(0, -rotationSpeed * Time.deltaTime / 3, 0);
            }

            // Rotate around the local Z-axis in the positive direction when "Y" is pressed
            if (Input.GetKey(rotateZAxisPositiveKey))
            {
                selectedBrainPart.transform.localRotation *= Quaternion.Euler(0, 0, rotationSpeed * Time.deltaTime / 3);
            }

            // Rotate around the local Z-axis in the negative direction when "H" is pressed
            if (Input.GetKey(rotateZAxisNegativeKey))
            {
                selectedBrainPart.transform.localRotation *= Quaternion.Euler(0, 0, -rotationSpeed * Time.deltaTime / 3);
            }

            // Increase Z position when "U" is pressed
            if (Input.GetKey(increaseZPositionKey))
            {
                selectedBrainPart.transform.position += Vector3.forward * movementSpeed * Time.deltaTime;
            }

            // Decrease Z position when "I" is pressed
            if (Input.GetKey(decreaseZPositionKey))
            {
                selectedBrainPart.transform.position -= Vector3.forward * movementSpeed * Time.deltaTime;
            }
        }

        // You can dynamically select the brain part here, e.g., by clicking on it
        if (Input.GetMouseButtonDown(0))  // Left click
        {
            SelectBrainPartUnderMouse();
        }
    }

    void SelectBrainPartUnderMouse()
    {
        // Cast a ray from the mouse position to detect the clicked object
        Ray ray = Camera.main.ScreenPointToRay(Input.mousePosition);
        RaycastHit hit;

        if (Physics.Raycast(ray, out hit))
        {
            if (hit.collider != null)
            {
                // Set the selected brain part to the object that was clicked
                selectedBrainPart = hit.collider.gameObject;
                Debug.Log("Selected Brain Part: " + selectedBrainPart.name);
            }
        }
    }
}

