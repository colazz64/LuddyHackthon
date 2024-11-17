const uploadForm = document.getElementById('upload-form');
const qaForm = document.getElementById('qa-form');
const fileInput = document.getElementById('document');
const fileDetails = document.getElementById('file-details');

// Handle document upload
fileInput.addEventListener('change', () => {
    const file = fileInput.files[0];
    if (file) {
        fileDetails.innerText = `File Selected: ${file.name} (${(file.size / 1024).toFixed(2)} KB)`;
    }
});

uploadForm.addEventListener('submit', async (event) => {
    event.preventDefault();
    const formData = new FormData();
    formData.append('document', fileInput.files[0]);

    const response = await fetch('/summarize', {
        method: 'POST',
        body: formData
    });

    const data = await response.json();
    document.getElementById('summary-result').innerText = "Summary: " + data.summary;
});

// Handle Q&A
qaForm.addEventListener('submit', async (event) => {
    event.preventDefault();
    const context = document.getElementById('context').value;
    const question = document.getElementById('question').value;

    const response = await fetch('/qa', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ context, question })
    });

    const data = await response.json();
    document.getElementById('qa-result').innerText = "Answer:\n" + data.answer;
});
