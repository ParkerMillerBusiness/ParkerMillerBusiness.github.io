const express = require('express');
const OpenAI = require('openai');

const app = express();
const port = 3000;

// Hardcoded API key (not recommended for production)
const apiKey = "your_api_key";

const openai = new OpenAI({ apiKey });

app.use(express.json());

app.get('/', (req, res) => {
    res.send('Welcome to my OpenAI server!');
});

app.post('/getCompletion', async (req, res) => {
    try {
        const completion = await openai.chat.completions.create({
            model: "gpt-4o-mini",
            messages: req.body.messages,
        });
        res.json(completion.choices[0].message.content);
    } catch (error) {
        res.status(500).send(error.toString());
    }
});

app.listen(port, () => {
    console.log(`Server running on port ${port}`);
});