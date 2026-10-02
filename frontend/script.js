
const form = document.getElementById("url-form");
const input = document.getElementById("url-input");
const button = document.getElementById("check-button");

const status = document.getElementById("status");
const result = document.getElementById("result");
const prediction = document.getElementById("prediction");
const checkedUrl = document.getElementById("checked-url");
const score = document.getElementById("score");

const API_URL = "http://127.0.0.1:5000/predict";

form.addEventListener("submit", async (event) => {
    // Prevent the page from reloading
    event.preventDefault();

    const url = input.value.trim();

    if (!url) {
        status.textContent = "Please enter a URL.";
        return;
    }

    // Show loading state
    button.disabled = true;
    button.textContent = "Analyzing...";
    status.textContent = "Checking the URL using machine learning...";
    result.classList.add("hidden");

    try {
        // Send the URL to the Python backend
        const response = await fetch(API_URL, {
            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({
                url: url
            })
        });

        const data = await response.json();

        // Handle errors returned by Flask
        if (!response.ok) {
            throw new Error(
                data.error || "Unable to analyze the URL."
            );
        }

        // Display the model's prediction
        prediction.textContent = data.prediction;
        checkedUrl.textContent = "URL: " + data.url;

        score.textContent =
            data.phishing_probability + "%";

        // Change the result heading color
        if (data.prediction === "Phishing") {
            prediction.style.color = "#f87171";
        } else {
            prediction.style.color = "#4ade80";
        }

        result.classList.remove("hidden");
        status.textContent = "Analysis complete.";

    } catch (error) {
        console.error("Error:", error);

        status.textContent =
            "Could not connect to the model. " +
            "Make sure the Python backend is running.";

    } finally {
        // Restore the button
        button.disabled = false;
        button.textContent = "Detect Phishing";
    }
});