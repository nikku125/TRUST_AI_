document.getElementById('analyzeBtn').addEventListener('click', async () => {
    const text = document.getElementById('messageInput').value;
    const resultSection = document.getElementById('resultSection');
    const resultLabel = document.getElementById('resultLabel');
    const confidenceScore = document.getElementById('confidenceScore');
    const confidenceFill = document.getElementById('confidenceFill');

    if (!text.trim()) {
        alert("Please enter some text to analyze.");
        return;
    }

    // Show loading state
    document.getElementById('analyzeBtn').disabled = true;
    document.getElementById('analyzeBtn').innerText = "Analyzing...";

    try {
        const response = await fetch('/predict', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ text: text })
        });

        const data = await response.json();

        if (response.ok) {
            resultSection.classList.remove('hidden');
            resultLabel.innerText = data.result;
            confidenceScore.innerText = data.confidence;
            
            // Update UI based on result
            if (data.result === 'Real') {
                resultLabel.className = 'real';
                confidenceFill.style.backgroundColor = '#27ae60';
            } else {
                resultLabel.className = 'fake';
                confidenceFill.style.backgroundColor = '#c0392b';
            }
            
            confidenceFill.style.width = data.confidence + '%';
        } else {
            alert("Error: " + data.error);
        }
    } catch (error) {
        console.error('Error:', error);
        alert("An error occurred while connecting to the server.");
    } finally {
        document.getElementById('analyzeBtn').disabled = false;
        document.getElementById('analyzeBtn').innerText = "Analyze Text";
    }
});
