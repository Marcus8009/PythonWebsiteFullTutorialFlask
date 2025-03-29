function deleteNote(noteId) {  // Changed parameter name to noteId
    fetch('/delete-note', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': document.querySelector('input[name="csrf_token"]').value
        },
        body: JSON.stringify({ noteId: noteId })  // Changed to noteId
    }).then((_res) => {
        window.location.href = "/";
    }).catch((error) => {
        console.error('Error:', error);
    });
}