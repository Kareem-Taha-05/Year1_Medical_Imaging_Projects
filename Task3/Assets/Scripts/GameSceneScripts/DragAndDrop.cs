using UnityEngine;

public class DragAndDrop : MonoBehaviour
{
    private Vector3 offset;
    private float zCoord;

    void OnMouseDown()
    {
        zCoord = Camera.main.WorldToScreenPoint(gameObject.transform.position).z;
        offset = gameObject.transform.position - GetMouseWorldPos();
    }

    void OnMouseDrag()
    {
        // Get the current mouse position and set the object's position without clamping
        Vector3 currentPosition = GetMouseWorldPos() + offset;
        transform.position = currentPosition;
    }

    private Vector3 GetMouseWorldPos()
    {
        // Convert the mouse position from screen space to world space
        Vector3 mousePoint = Input.mousePosition;
        mousePoint.z = zCoord;
        return Camera.main.ScreenToWorldPoint(mousePoint);
    }
}

