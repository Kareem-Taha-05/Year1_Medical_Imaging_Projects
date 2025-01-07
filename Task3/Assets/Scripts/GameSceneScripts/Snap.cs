using UnityEngine;

public class SnapPiece : MonoBehaviour
{
    public Transform targetPosition;  // Assign each piece's reference target in the Inspector
    public float positionThreshold = 0.5f;  // Distance threshold for snapping
    public Vector3 rotationThreshold = new Vector3(30f, 30f, 30f); // Rotation threshold for each axis (in degrees)

    private bool isSnapped = false;

    void Update()
    {
        // Only check for snapping if the piece hasn't already snapped
        if (!isSnapped)
        {
            // Check for snapping when the mouse button is released
            if (Input.GetMouseButtonUp(0)) // Left-click released
            {
                CheckSnap();
            }
        }
    }

    private void CheckSnap()
    {
        // Check if the piece is close enough to the target position
        if (Vector3.Distance(transform.position, targetPosition.position) < positionThreshold)
        {
            // Check if the piece's rotation on each axis is within the threshold
            Vector3 currentEulerAngles = NormalizeEulerAngles(transform.rotation.eulerAngles);
            Vector3 targetEulerAngles = NormalizeEulerAngles(targetPosition.rotation.eulerAngles);

            float xDifference = Mathf.Abs(Mathf.DeltaAngle(currentEulerAngles.x, targetEulerAngles.x));
            float yDifference = Mathf.Abs(Mathf.DeltaAngle(currentEulerAngles.y, targetEulerAngles.y));
            float zDifference = Mathf.Abs(Mathf.DeltaAngle(currentEulerAngles.z, targetEulerAngles.z));

            // Check if each axis' rotation difference is within the threshold
            if (xDifference <= rotationThreshold.x &&
                yDifference <= rotationThreshold.y &&
                zDifference <= rotationThreshold.z)
            {
                SnapToPosition();
            }
        }
    }

    private void SnapToPosition()
    {
        // Snap the piece to the exact target position and rotation
        transform.position = targetPosition.position;
        transform.rotation = targetPosition.rotation;
        isSnapped = true;

        Debug.Log(gameObject.name + " has snapped into place!");

        // Make the piece unmovable by disabling its collider
        Collider pieceCollider = GetComponent<Collider>();
        if (pieceCollider != null)
        {
            pieceCollider.enabled = false;
        }

        // Optionally, disable this script to prevent further updates
        this.enabled = false;

        // Notify the PuzzleCompletion script if needed
        PuzzleCompletion.Instance.PieceSnapped();
    }

    // Normalize Euler angles to avoid negative values
    private Vector3 NormalizeEulerAngles(Vector3 eulerAngles)
    {
        return new Vector3(
            eulerAngles.x < 0 ? eulerAngles.x + 360 : eulerAngles.x,
            eulerAngles.y < 0 ? eulerAngles.y + 360 : eulerAngles.y,
            eulerAngles.z < 0 ? eulerAngles.z + 360 : eulerAngles.z
        );
    }
}
