    document.addEventListener('DOMContentLoaded', function () {
        let json_events = JSON.parse(document.getElementById('event-data').textContent);
        json_events = JSON.parse(json_events);

        const calendarEl = document.getElementById('calendar');
        calendar = new FullCalendar.Calendar(calendarEl, {
            initialView: 'dayGridMonth',
            defaultAllDay: true,
            events: json_events,
        });

        calendar.render();
    });
