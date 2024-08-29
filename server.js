const express = require('express');
const OpenAI = require('openai');

const app = express();
const port = 3000;

// Hardcoded API key (not recommended for production)
const apiKey = "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";

const openai = new OpenAI({ apiKey });

app.use(express.json());

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