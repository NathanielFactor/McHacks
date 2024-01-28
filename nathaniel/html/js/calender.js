

function generateCalendar() {

    const container = document.getElementById('calendar-container');
    const currentDate = new Date();
    const currentYear = currentDate.getFullYear();
    const currentMonth = currentDate.getMonth();

    const firstDayOfMonth = new Date(currentYear, currentMonth, 1);
    const daysInMonth = new Date(currentYear, currentMonth + 1, 0).getDate();

    const colorArray = [daysInMonth];  // set cell colors to white 
        
    const table = document.createElement('table');
    container.appendChild(table);

    const daysOfWeek = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'];
    const headerRow = document.createElement('tr');
    daysOfWeek.forEach(day => {
        const th = document.createElement('th');
        th.textContent = day;
        headerRow.appendChild(th);
    });
    table.appendChild(headerRow);

    let dayCounter = 1;
    for (let i = 0; i < 6; i++) {
        const row = document.createElement('tr');
        for (let j = 0; j < 7; j++) {
            const td = document.createElement('td');
            if (i === 0 && j < firstDayOfMonth.getDay()) {
                td.textContent = '';
            } else if (dayCounter <= daysInMonth) {
                td.textContent = dayCounter;

                td.style.backgroundColor = colorArray[dayCounter - 1]; //set background colour using colorArrray
                td.className = 'color' + dayCounter;
                td.addEventListener('click', function () {
                    openModal(dayCounter);
                });

                dayCounter++;
            }
            row.appendChild(td);
        }
        table.appendChild(row);
    }
    handleButtonClick();
}

function openModal(selectedDay) {
    const modal = document.getElementById('myModal');
    const selectedDayText = document.getElementById('selectedDayText');
    selectedDayText.textContent = "stuff";
    modal.style.display = 'flex';
}

function closeModal() {
    const modal = document.getElementById('myModal');
    modal.style.display = 'none';
}


//input color is a string 
function changeCellColor(color, dayOfMonth) {

    if (color == yellow) {
        colorCode = '#f6ff76'
    }
    if (color == blue) {
        colorCode = '#7698ff'
    }
    if (color == red) {
        colorCode = '#ea354d'
    }
    colorArray[dayOfMonth - 1] = colorCode;

    enableButtonClick();
}


function handleButtonClick() {
    document.getElementById("calendarButton").disabled = true;

   
}

function enableButtonClick() {
    document.getElementById("calendarButton").disabled = false;
    
} 

