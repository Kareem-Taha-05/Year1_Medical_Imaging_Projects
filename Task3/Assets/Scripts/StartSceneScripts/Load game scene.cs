using UnityEngine;
using UnityEngine.SceneManagement; // Required to use SceneManager

public class SceneManagerController : MonoBehaviour
{
    // This function will be called by the button to change scenes
    public void StartNewGame()
    {
        // Load the game scene by its name (replace "GameScene" with your actual scene name)
        SceneManager.LoadScene("GameScene");
    }
}

