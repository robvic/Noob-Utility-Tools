document.addEventListener('DOMContentLoaded', function() {
    const button = document.querySelector('button');
    const input = document.querySelector('input');
    const displayArea = document.createElement('div');
    
    document.body.appendChild(displayArea);

    button.addEventListener('click', function() {
        const userInput = input.value;
        const url = `https://api.example.com/data?query=${encodeURIComponent(userInput)}`;

        fetch(url)
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                return response.json();
            })
            .then(data => {
                displayArea.innerHTML = `Response: ${JSON.stringify(data)}`;
            })
            .catch(error => {
                displayArea.innerHTML = `Error: ${error.message}`;
            });
    });
});