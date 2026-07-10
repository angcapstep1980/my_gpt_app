const chatDiv = document.getElementById('chat');
const promptEl = document.getElementById('prompt');
const sendBtn = document.getElementById('send');

// Configura marked per usare highlight.js
marked.setOptions({
    highlight: function(code, lang) {
        const language = hljs.getLanguage(lang)? lang : 'plaintext';
        return hljs.highlight(code, { language }).value;
    },
    breaks: true // \n diventa <br>
});

function addMessage(role, content) {
    const div = document.createElement('div');
    div.className = `msg ${role}`;

    if (role === 'assistant') {
        // Renderizza markdown solo per l'assistant
        div.innerHTML = marked.parse(content);
    } else {
        div.textContent = content; // user msg rimane testo semplice
    }

    chatDiv.appendChild(div);
    chatDiv.scrollTop = chatDiv.scrollHeight;
}

async function loadHistory() {
    const res = await fetch('/api/history');
    const history = await res.json();
    chatDiv.innerHTML = '';
    history.forEach(m => addMessage(m.role, m.content));
}

async function sendMessage() {
    const message = promptEl.value.trim();
    if (!message) return;

    addMessage('user', message);
    promptEl.value = '';
    promptEl.disabled = true;
    sendBtn.disabled = true;

    try {
        const res = await fetch('/api/chat', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({message})
        });
        const data = await res.json();
        if (data.error) {
            addMessage('assistant', 'Errore: ' + data.error);
        } else {
            addMessage('assistant', data.reply);
        }
    } catch (e) {
        addMessage('assistant', 'Errore di rete');
    } finally {
        promptEl.disabled = false;
        sendBtn.disabled = false;
        promptEl.focus();
    }
}

async function resetChat() {
    await fetch('/api/reset', {method: 'POST'});
    location.reload();
}

promptEl.addEventListener('keydown', e => {
    if (e.key === 'Enter' &&!e.shiftKey) {
        e.preventDefault();
        sendMessage();
    }
});

loadHistory();