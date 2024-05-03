// Global variables
let eventDate = 0;
let current_id = 0;
let createEventModal = null;
let deleteEventModal = null;
let calendar = null;

// Utility functions

/**
 * Calculates the maximum ID value from the given events array and returns the next available ID.
 *
 * @param {Array} events - The array of events.
 * @returns {number} - The next available ID.
 */
function getMaxId(events) {
    let max_id = 0;
    for (let event of events) {
        if (event.id > max_id) {
            max_id = event.id;
        }
    }
    current_id = max_id + 1;
}

// -> Credit for getWeekday: https://www.w3schools.com/jsref/jsref_getday.asp
/**
 * Returns the week day for a given date.
 *
 * @param {string} date - The date in string format.
 * @returns {string} - The week day corresponding to the given date.
 */
function getWeekDay(date) {
    const weekdays = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'];
    return weekdays[new Date(date).getDay()];
}

/**
 * Converts an event object to a plain object with recurrence rule (RRule) information.
 * If the event is recurring, it extracts the RRule information and adds it to the event object.
 *
 * @param {Object} event - The event object to convert.
 * @returns {Object} - The converted event object with RRule information.
 */
function toPlainObjectWithRRule(event) {
    let event_object = event.toPlainObject();
    if (event._def.recurringDef) {
        const event_rrule_object = {
            freq: event._def.recurringDef.typeData.rruleSet._rrule[0].options.freq,
            interval: event._def.recurringDef.typeData.rruleSet._rrule[0].options.interval,
            dstart: event._def.recurringDef.typeData.rruleSet._rrule[0].options.dtstart.toISOString().split('T')[0],
            until: event._def.recurringDef.typeData.rruleSet._rrule[0].options.until.toISOString().split('T')[0],
        };
        event_object.rrule = event_rrule_object;
    }
    return event_object;
}

/**
 * Creates a new event on the specified date.
 * Does this by resetting and showing the create event modal.
 *
 * @param {string} date - The date for which the event is to be created.
 */
function createEvent(date) {
    createEventModal = new bootstrap.Modal(document.getElementById('createEventModal'));
    document.getElementById('create-event-modal-title').textContent = `Create a new event on ${getWeekDay(date)}, ${date}`;
    // -> Credit for selectedIndex: https://www.w3schools.com/jsref/prop_select_selectedindex.asp
    document.getElementById('bin-type').selectedIndex = 0;
    document.getElementById('recurrence').selectedIndex = 0;
    eventDate = new Date(date);
    createEventModal.show();
}


// This should handle Event removal but it is not working yet
// To get this to work I need to add exdates to the rrule in the event object
function handleModalSubmit(event, info, submitButton) {
    console.log(info.event.id);
    event.preventDefault();
    deleteEventModal.hide();
    submitButton.removeEventListener('click', handleModalSubmit);

    if (document.getElementById('delete-select').value === 'only this event') {
        info.event.exdate += [info.event.startStr];
    } else {
        var events = calendar.getEvents();
        for (var event of events) {
            if (event.groupId === event.id) {
                event.remove();
            }
        }
    }
    calendar.refetchEvents();
}

/**
 * Retrieves JSON events from the 'event-data' element and parses them into an object.
 *
 * @returns {Object} The parsed JSON events.
 */
function getJsonEvents() {
    let json_events = JSON.parse(document.getElementById('event-data').textContent);
    json_events = JSON.parse(json_events);
    return json_events;
}

/**
 * Renders the calendar with the provided event data.
 * Adjusts the Settings of the FullCalendar
 *
 * @function renderCalendar
 */
function renderCalendar() {
    json_events = getJsonEvents();

    const calendarEl = document.getElementById('calendar');
    calendar = new FullCalendar.Calendar(calendarEl, {
        initialView: 'dayGridMonth',
        defaultAllDay: true,
        dateClick: function (info) {
            createEvent(info.dateStr);
        },
        eventMouseEnter: function (info) {
            info.el.style.backgroundColor = 'lightblue';
            info.el.style.border = 'none';
            info.el.style.color = 'white';
            info.el.innerHTML += '<i class="fas fa-trash-alt"></i>';
        },
        eventMouseLeave: function (info) {
            info.el.style.backgroundColor = '';
            info.el.innerHTML = `${info.event.title}<br>`;
            info.el.style.color = 'white';
        },
        eventClick: function (info) {
            deleteEventModal = new bootstrap.Modal(document.getElementById('deleteEventModal'));
            document.getElementById('delete-event-modal-title').textContent = `Delete event: ${info.event.title} from ${info.event.start}`;

            let submitButton = document.getElementById('delete-event');
            submitButton.addEventListener('click', (event) => handleModalSubmit(event, info, submitButton));

            deleteEventModal.show();
        },
        events: json_events,
    });
    calendar.render();
}


/**
 * This function is responsible for posting calendar events to the server.
 * It includes The CSRF token that is generated in the Django template.
 * The function expects a redirect URL from the server.
 *
 * @returns {void}
 */
function postCalendarEvents(e) {
    // Should I use Ajax here instead?
    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    const jsonBody = JSON.stringify(get_calender_event_objects());
    console.log(jsonBody);
    scheduleId = e.target.getAttribute('data-schedule-id');
    console.log(e.target);
    fetch(scheduleId, {
        method: "POST",
        headers: {
            'Content-Type': 'application/json',
            // Include CSRF token in the header
            'X-CSRFToken': csrftoken
        },
        body: jsonBody,
    }).then(response => response.json()).then(data => {
        if (data.redirect_url) {
            window.location.href = data.redirect_url;
        }
    }).catch(error => {
        console.error('Error:', error);
    });
}

/**
 * Retrieves the calendar event objects.
 * @returns {Array} An array of calendar event objects.
 */
function get_calender_event_objects() {
    let events = [];
    for (let event of calendar.getEvents()) {
        console.log(event.toPlainObject());
        events.push(toPlainObjectWithRRule(event));
    }
    return events;
}

// On document load
document.addEventListener('DOMContentLoaded', function () {
    renderCalendar();

    // This is to know where to continue the ID count
    getMaxId(calendar.getEvents());

    // -> Credit for query selector: https://developer.mozilla.org/en-US/docs/Web/API/Document/querySelector?retiredLocale=de
    // Call the postCalendarEvents function when the submit button is clicked
    document.getElementById('submit-button').addEventListener('click', function (e) {
        e.preventDefault();
        postCalendarEvents(e);
    });

    // Save the event when the save button is clicked
    document.getElementById('save-event').addEventListener('click', function () {
        const bin_type = document.getElementById('bin-type').value;
        const recurrence = document.getElementById('recurrence').value;
        if (recurrence === '0') {
            calendar.addEvent({
                id: current_id,
                title: bin_type,
                start: eventDate,
                groupId: bin_type,
            });
        } else {
            // -> Credit for adding a year to a date: https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Date/setFullYear
            let endRecurrence = new Date(new Date(eventDate).setFullYear(eventDate.getFullYear() + 1));
            calendar.addEvent({
                id: current_id,
                title: bin_type,
                start: eventDate,
                groupId: bin_type,
                rrule: {
                    freq: 'weekly',
                    interval: recurrence,
                    dtstart: eventDate,
                    until: endRecurrence
                }
            });
        }
        current_id++;
        createEventModal.hide();
    });
});

