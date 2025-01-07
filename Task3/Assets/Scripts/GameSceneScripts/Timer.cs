using UnityEngine;
using TMPro; // Import TextMeshPro namespace

public class Timer : MonoBehaviour
{
    public TextMeshProUGUI timerText; // Use TextMeshProUGUI instead of Text
    private float elapsedTime = 0f; // Time passed since the game started
    private bool isGameOver = false;

    void Update()
    {
        if (!isGameOver)
        {
            elapsedTime += Time.deltaTime; // Count time since game started
            UpdateTimerUI();
        }
    }

    void UpdateTimerUI()
    {
        // Convert elapsedTime to minutes and seconds format (mm:ss)
        int minutes = Mathf.FloorToInt(elapsedTime / 60);
        int seconds = Mathf.FloorToInt(elapsedTime % 60);
        timerText.text = string.Format("{0:00}:{1:00}", minutes, seconds);
    }

    public void StopTimer()
    {
        isGameOver = true; // Stop the timer when the game is over
    }

    public string GetElapsedTime()
    {
        int minutes = Mathf.FloorToInt(elapsedTime / 60);
        int seconds = Mathf.FloorToInt(elapsedTime % 60);
        return string.Format("{0:00}:{1:00}", minutes, seconds);
    }
}
