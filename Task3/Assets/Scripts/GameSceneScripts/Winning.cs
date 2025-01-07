using UnityEngine;
using UnityEngine.SceneManagement; // For scene management
using TMPro;

public class PuzzleCompletion : MonoBehaviour
{
    public static PuzzleCompletion Instance;

    [Header("UI References")]
    public GameObject completionPanel; // Panel containing completion message
    public TextMeshProUGUI completionText; // For displaying the winning message
    public GameObject restartButton; // The restart button (assigned in the inspector)

    [Header("Audio")]
    public AudioSource audioSource;
    public AudioClip completionSound;  // Sound to play when the puzzle is completed
    public AudioClip snapPieceSound;   // Sound to play when a piece is snapped into place

    [Header("Timer Reference")]
    public Timer timer; // Reference to the Timer script

    [Header("Messages")]
    public string completionMessage = "Congratulations!\nPuzzle Complete!";
    public float messageDisplayTime = 3f; // How long to show the message

    private int totalPieces;
    private int snappedPieces = 0;
    private bool puzzleCompleted = false;

    private void Awake()
    {
        if (Instance == null)
            Instance = this;
        else
            Destroy(gameObject);

        // Initialize audio source if not set
        if (audioSource == null)
            audioSource = gameObject.AddComponent<AudioSource>();
    }

    void Start()
    {
        totalPieces = FindObjectsOfType<SnapPiece>().Length;

        // Hide completion panel at start
        if (completionPanel != null)
            completionPanel.SetActive(false);

        // Hide the restart button at the start
        if (restartButton != null)
            restartButton.SetActive(false);
    }

    public void PieceSnapped()
    {
        snappedPieces++;
        if (snapPieceSound != null && audioSource != null)
        {
            audioSource.clip = snapPieceSound;
            audioSource.Play();  // Play sound every time a piece is snapped
        }

        if (snappedPieces >= totalPieces && !puzzleCompleted)
        {
            PuzzleCompleted();
        }
    }

    private void PuzzleCompleted()
    {
        puzzleCompleted = true;
        Debug.Log("Puzzle Complete!");

        // Stop the timer
        if (timer != null)
        {
            timer.StopTimer();
        }

        // Show completion message
        if (completionPanel != null && completionText != null)
        {
            completionPanel.SetActive(true);
            completionText.text = completionMessage + "\nYou completed the puzzle in\n" + timer.GetElapsedTime();

            // Optional: Hide the panel after a delay
            Invoke("HideCompletionMessage", messageDisplayTime);
        }

        // Show the restart button
        if (restartButton != null)
        {
            restartButton.SetActive(true);
        }

        // Play completion sound
        if (audioSource != null && completionSound != null)
        {
            audioSource.clip = completionSound;
            audioSource.Play();
        }
    }

    private void HideCompletionMessage()
    {
        if (completionPanel != null)
            completionPanel.SetActive(false);
    }

    // Method to restart the game by reloading the current scene
    public void RestartGame()
    {
        SceneManager.LoadScene(SceneManager.GetActiveScene().name); // Reloads the current scene
    }

    // Optional: Method to reset the puzzle
    public void ResetPuzzle()
    {
        snappedPieces = 0;
        puzzleCompleted = false;
        if (completionPanel != null)
            completionPanel.SetActive(false);
    }
}


