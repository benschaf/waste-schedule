// Global variables
let eventDate = 0;
let currendID = 0;
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
    let maxId = 0;
    for (let event of events) {
        if (event.id > maxId) {
            maxId = event.id;
        }
    }
    currendID = maxId + 1;
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
    let eventObject = event.toPlainObject();
    if (event._def.recurringDef) {
        const eventRruleObject = {
            freq: event._def.recurringDef.typeData.rruleSet._rrule[0].options.freq,
            interval: event._def.recurringDef.typeData.rruleSet._rrule[0].options.interval,
            dstart: event._def.recurringDef.typeData.rruleSet._rrule[0].options.dtstart.toISOString().split('T')[0],
            until: event._def.recurringDef.typeData.rruleSet._rrule[0].options.until.toISOString().split('T')[0],
        };
        eventObject.rrule = eventRruleObject;
    }
    return eventObject;
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


// The function below should handle Event removal but it is not working yet
// To get this to work I need to add exdates to the rrule in the event object
// It just cant get the exdate property from the calendar which doesn't let me edit it .........
// it might work if i change the calendar library import to NPM but i don't know if i want to do that ...
// what i could also do instead is convert the whole rrule property into a string. https://stackoverflow.com/questions/56580678/is-exdate-not-included-in-rrule-for-full-calendar

/**
 * Handles the deletion of an event.
 * @param {Event} event - The event object.
 * @param {Object} info - Additional information about the event.
 * @param {HTMLElement} submitButton - The submit button element.
 */
function handleDeletion(event, info, submitButton) {
    //maybe i can just remove prevent default
    event.preventDefault();
    deleteEventModal.hide();

    if (document.getElementById('delete-select').value === 'only this event') {
        console.log('one event removed');
        // right here - setProp isnt accessible
        info.event.setProp('exdate', '2024-05-23')
        console.log(info.event);
    } else {
        console.log('all events removed');
        info.event.remove();
    }
    calendar.refetchEvents();
}

/**
 * Retrieves JSON events from the 'event-data' element and parses them into an object.
 *
 * @returns {Object} The parsed JSON events.
 */
function getJsonEvents() {
    let jsonEvents = JSON.parse(document.getElementById('event-data').textContent);
    jsonEvents = JSON.parse(jsonEvents);
    return jsonEvents;
}

/**
 * Renders the calendar using FullCalendar library.
 *
 * @returns {void}
 */
function renderCalendar() {
    jsonEvents = getJsonEvents();

    const calendarEl = document.getElementById('calendar');
    calendar = new FullCalendar.Calendar(calendarEl, {
        initialView: 'dayGridMonth',
        defaultAllDay: true,
        dateClick: function (info) {
            createEvent(info.dateStr);
        },
        eventMouseEnter: function (info) {
            info.el.style.backgroundColor = '#1c7b47db';
            info.el.style.border = 'none';
            info.el.style.color = 'white';
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
            submitButton.addEventListener('click', (event) => handleDeletion(event, info, submitButton));

            deleteEventModal.show();
        },
        events: jsonEvents,

    });
    calendar.render();
}


// -> Credit for query selector: https://developer.mozilla.org/en-US/docs/Web/API/Document/querySelector?retiredLocale=de
/**
 * Attaches an event listener to the submit button that sends a POST request with calendar events.
 * @returns {void}
 */
function postCalendarEvents() {
    document.getElementById('submit-button').addEventListener('click', function (e) {
        e.preventDefault();
        const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
        const jsonBody = JSON.stringify(getCalendarEventObjects());
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
    });
}

/**
 * Retrieves the calendar event objects.
 * @returns {Array} An array of calendar event objects.
 */
function getCalendarEventObjects() {
    let events = [];
    for (let event of calendar.getEvents()) {
        console.log(event.toPlainObject());
        events.push(toPlainObjectWithRRule(event));
    }
    return events;
}

/**
 * Saves the event by adding it to the calendar.
 * @returns {void}
 */
function saveEvent() {
    document.getElementById('save-event').addEventListener('click', function () {
        const binType = document.getElementById('bin-type').value;
        const recurrence = document.getElementById('recurrence').value;
        if (recurrence === '0') {
            calendar.addEvent({
                id: currendID,
                title: binType,
                start: eventDate,
                groupId: binType,
            });
        } else {
            // -> Credit for adding a year to a date: https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Date/setFullYear
            let endRecurrence = new Date(new Date(eventDate).setFullYear(eventDate.getFullYear() + 1));
            calendar.addEvent({
                id: currendID,
                title: binType,
                start: eventDate,
                groupId: binType,
                rrule: {
                    freq: 'weekly',
                    interval: recurrence,
                    dtstart: eventDate,
                    until: endRecurrence
                },
                exdate: []
            });
        }
        currendID++;
        createEventModal.hide();
    });
}

// On document load
document.addEventListener('DOMContentLoaded', function () {
    renderCalendar();
    getMaxId(calendar.getEvents());

    // Event listeners
    postCalendarEvents();
    saveEvent();
});