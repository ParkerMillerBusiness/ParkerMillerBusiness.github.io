import OpenAI from 'https://cdn.jsdelivr.net/npm/openai';

const openai = new OpenAI({
    apiKey: "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"
});

async function getCompletion() {
    const completion = await openai.chat.completions.create({
        model: "gpt-4o-mini",
        messages: [
            { role: "system", content: "You are a helpful assistant." },
            { role: "user", content: "What's 1+1?" },
        ],
    });
    console.log(completion.choices[0].message.content);
}

getCompletion();