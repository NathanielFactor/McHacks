// Function to save mood
function saveMood() {
    const mood = document.getElementById('moodInput').value;
    if (mood) {
        console.log(`Mood saved: ${mood}`);
        // Here you would typically send this data to the backend
    }
}

// Function to save journal entry
function saveJournal() {
    const journalEntry = document.getElementById('journalEntry').value;
    if (journalEntry) {
        console.log(`Journal entry saved: ${journalEntry}`);
        // Here you would typically send this data to the backend
    }
}

let selectedMood = '';

// Function to set the selected mood
function setMood(mood) {
    selectedMood = mood;
    console.log(`Mood selected: ${selectedMood}`);
    // Optionally, highlight the selected mood button
    const buttons = document.querySelectorAll('.moodButton');
    buttons.forEach(button => {
        if (button.textContent.includes(mood)) {
            button.classList.add('selected');
        } else {
            button.classList.remove('selected');
        }
    });
}

// Function to save mood
function saveMood() {
    if (selectedMood) {
        console.log(`Mood saved: ${selectedMood}`);
        // Here you would typically send this data to the backend
    } else {
        console.log('No mood selected');
    }
}

document.addEventListener('DOMContentLoaded', function () {
    var calendarEl = document.getElementById('calendar');
    var calendar = new FullCalendar.Calendar(calendarEl, {
        initialView: 'dayGridMonth',
        dateClick: function(info) {
            // Open the modal when a date is clicked
            openModal();
        }
    });
    calendar.render();
});

// Get the modal
var modal = document.getElementById("moodJournalModal");

// Get the <span> element that closes the modal
var span = document.getElementsByClassName("close")[0];

// When the user clicks on <span> (x), close the modal
span.onclick = function() {
    modal.style.display = "none";
}

// When the user clicks anywhere outside of the modal, close it
window.onclick = function(event) {
    if (event.target == modal) {
        modal.style.display = "none";
    }
}

function openModal() {
    modal.style.display = "block";
}

// ... (rest of your script.js)
