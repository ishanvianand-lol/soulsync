const API = "https://soulsync-a1af.onrender.com";
let currentMood = "stressed";

// Text Mood
async function analyzeText() {
let text = document.getElementById("textInput").value;

```
let res = await fetch(API + "/analyze-text", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ text })
});

let data = await res.json();
showResult(data);
```

}

// Show result
function showResult(data) {
document.getElementById("result").innerText =
"Mood: " + data.mood + " | Chakra: " + data.chakra;

```
document.getElementById("musicPlayer").src = data.audio;
currentMood = data.mood;
```

}

// Voice Recording
let recorder;
let chunks = [];

async function recordVoice() {
let stream = await navigator.mediaDevices.getUserMedia({ audio: true });

```
recorder = new MediaRecorder(stream);
recorder.start();

recorder.ondataavailable = e => chunks.push(e.data);

recorder.onstop = async () => {
    let blob = new Blob(chunks, { type: 'audio/webm' });
    chunks = [];

    let formData = new FormData();
    formData.append("file", blob, "speech.webm");

    let res = await fetch(API + "/speech-mood", {
        method: "POST",
        body: formData
    });

    let data = await res.json();

    document.getElementById("spoken").innerText =
        "You said: " + data.text;

    showResult(data);
};

setTimeout(() => recorder.stop(), 5000);
```

}

// Gemini Story
async function getStory() {
let res = await fetch(API + "/story", {
method: "POST",
headers: { "Content-Type": "application/json" },
body: JSON.stringify({ mood: currentMood })
});

```
let data = await res.json();

document.getElementById("story").innerText = data.story;
document.getElementById("storyPlayer").src = data.audio;
```

}
