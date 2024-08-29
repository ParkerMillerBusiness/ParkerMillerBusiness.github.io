async function getAnswer() {
    const question = document.getElementById('question').value;
    const response = await fetch('/getCompletion', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            messages: [
                { role: "system", content: "You are a helpful assistant." },
                { role: "user", content: question },
            ],
        }),
    });

    const answer = await response.json();
    document.getElementById('answer').innerText = answer;
}