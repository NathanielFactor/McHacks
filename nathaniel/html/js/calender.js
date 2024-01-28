function generateCalendar() {
    const container = document.getElementById('calendar-container');
    const currentDate = new Date();
    const currentYear = currentDate.getFullYear();
    const currentMonth = currentDate.getMonth();

    const firstDayOfMonth = new Date(currentYear, currentMonth, 1);
    const daysInMonth = new Date(currentYear, currentMonth + 1, 0).getDate();

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
                td.addEventListener('click', function () {
                    // Replace the URL with the actual page you want to navigate to
                    window.location.href = 'page-for-day-' + dayCounter + '.html';
                });
                dayCounter++;
            }
            row.appendChild(td);
        }
        table.appendChild(row);
    }
}

generateCalendar();