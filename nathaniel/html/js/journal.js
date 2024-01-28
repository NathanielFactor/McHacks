function redirectToCalendar() {
    // Collect form data
    var entryTitle = document.getElementById("entryTitle").value;
    var entryDate = document.getElementById("entryDate").value;
    var entryText = document.getElementById("entryText").value;

    // Create JSON object
    var entryData = {
        title: entryTitle,
        date: entryDate,
        text: entryText
    };

    // Convert JSON object to a string
    var jsonString = JSON.stringify(entryData);

    // Send data to the server (replace 'your-server-endpoint' with your actual server endpoint)
    fetch('your-server-endpoint', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: jsonString,
    })
    .then(response => response.json())
    .then(data => {
        console.log('Success:', data);
        print("success");
    })
    .catch((error) => {
        console.error('Error:', error);
        print("fail");
    });

    // Redirect to the calendar page
    window.location.href = 'calendar.html';
    
    return false;  // Prevent the default form submission behavior
}