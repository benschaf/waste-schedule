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
    return maxId + 1;
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
 * The RRule information is added manually because the FullCalendar RRule plugin doesn't seem to provide a way to access it.
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
 * Displays the event creation modal with the specified date.
 *
 * @param {Date} date - The date for which the event creation modal should be displayed.
 */
function displayEventCreationModal(date) {
    createEventModal = new bootstrap.Modal(document.getElementById('createEventModal'));
    document.getElementById('create-event-modal-title').textContent = `Create a new event on ${getWeekDay(date)}, ${date}`;
    // -> Credit for selectedIndex: https://www.w3schools.com/jsref/prop_select_selectedindex.asp
    document.getElementById('bin-type').selectedIndex = 0;
    document.getElementById('recurrence').selectedIndex = 0;
    eventDate = new Date(date);
    createEventModal.show();
}

/**
 * The function below should handle Event removal but it is not working yet
 * To get this to work I need to add exdates to the rrule in the event object
 * It just cant get the exdate property from the calendar which doesn't let me edit it .........
 * it might work if i change the calendar library import to NPM but i don't know if i want to do that ...
 * what i could also do instead is convert the whole rrule property into a string. https://stackoverflow.com/questions/56580678/is-exdate-not-included-in-rrule-for-full-calendar
 */

/**
 * Handles the deletion of an event.
 * @param {Event} event - The event object.
 * @param {Object} info - Additional information about the event.
 */
function handleDeletion(event, info) {
    event.preventDefault();
    deleteEventModal.hide();

    if (document.getElementById('delete-select').value === 'only this event') {
        // right here - info.event.setProp isnt accessible i should be able to add exdate here ...
    } else {
        info.event.remove();
    }
    calendar.refetchEvents();
}

/**
 * Retrieves JSON events from the 'event-data' context-variable and parses them into an object.
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
 * The calendar is rendered with the initial view set to 'dayGridMonth'.
 * The dateClick event listener is set to display the event creation modal.
 * The eventMouseEnter and eventMouseLeave event listeners are set to change the background color of the event element on hover to indicate that it is clickable.
 * The eventClick event listener is set to display the delete event modal.
 * The events are set to the parsed JSON events from the 'event-data' context-variable.
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
            displayEventCreationModal(info.dateStr);
        },
        eventMouseEnter: function (info) {
            info.el.style.backgroundColor = '#1c7b47db';
            info.el.style.cursor = 'pointer';
            info.el.style.borderColor = 'red';
        },
        eventMouseLeave: function (info) {
            info.el.style.backgroundColor = '';
            info.el.style.borderColor = '';
        },
        eventClick: function (info) {
            deleteEventModal = new bootstrap.Modal(document.getElementById('deleteEventModal'));
            document.getElementById('delete-event-modal-title').textContent = `Delete event: ${info.event.title} from ${info.event.start}`;
            let submitButton = document.getElementById('delete-event');
            submitButton.addEventListener('click', (event) => handleDeletion(event, info));

            deleteEventModal.show();
        },
        events: jsonEvents,

    });
    calendar.render();
}


/**
 * Sends a POST request to the server with the calendar event data.
 *
 * @param {Event} e - The event object.
 * @returns {void}
 */
function postCalendarEvents(e) {
    // -> Credit for query selector: https://developer.mozilla.org/en-US/docs/Web/API/Document/querySelector?retiredLocale=de
    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    const jsonBody = JSON.stringify(getCalendarEventObjects());
    scheduleId = e.target.getAttribute('data-schedule-id');
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
function getCalendarEventObjects() {
    let events = [];
    for (let event of calendar.getEvents()) {
        events.push(toPlainObjectWithRRule(event));
    }
    return events;
}

/**
 * Saves the event by adding it to the calendar.
 * The bin type and recurrence are retrieved from the modal form.
 *
 * @returns {void}
 */
function saveEvent() {
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
}

// On document load
document.addEventListener('DOMContentLoaded', function () {
    renderCalendar();
    currendID = getMaxId(calendar.getEvents());

    // Event listeners
    document.getElementById('submit-button').addEventListener('click', function(event) {
        postCalendarEvents(event);
    });
    document.getElementById('save-event').addEventListener('click', saveEvent);
});

if (typeof module !== "undefined") module.exports = {
    getMaxId,
    getWeekDay,
    toPlainObjectWithRRule, // Don't know how to test this
    displayEventCreationModal, // I would need to test the html output
    handleDeletion, // Don't know how to test this
    getJsonEvents, // This is getting a json object from the django context variables ...
    renderCalendar, // Don't know how to test this
    postCalendarEvents, // Don't know how to test this
    getCalendarEventObjects, // Don't know how to test this
    saveEvent // Don't know how to test this
};