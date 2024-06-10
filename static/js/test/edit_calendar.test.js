/**
 * @jest-environment jsdom
 */

const {
    test,
    expect
} = require("@jest/globals");
const {
    getMaxId,
    getWeekDay,
    displayEventCreationModal,
} = require("../edit_calendar.js");

beforeAll(() => {
    let fs = require("fs");
    // I doubt this will work because this is linking to a html file with templating language in it
    let fileContents = fs.readFileSync("/workspace/waste-schedule/schedulebuilder/templates/schedulebuilder/calendar.html", "utf-8");
    document.open();
    document.write(fileContents);
    document.close();
});

describe("helper function tests", () => {
    test("getMaxId returns the maximum id of the events", () => {
        let events = [{
                id: 0
            },
            {
                id: 1
            },
            {
                id: 2
            }
        ];
        expect(getMaxId(events)).toBe(3);
    });

    test("getWeekDay returns the correct day of the week", () => {
        let date = new Date("2021-10-10");
        expect(getWeekDay(date)).toBe("Sunday");
    });
});

// this doesnt work because FullCalendar elements need to be loaded in their library for anything within the calendar to load to the DOM ...
describe("displayEventCreationModal tests", () => {
    test("displayEventCreationModal displays the modal", () => {
        displayEventCreationModal();
        let modal = document.getElementById("createEventModal");
        expect(modal.style.display).toBe("block");
    });
});

// All functions working with fullCalendar might need to be tested in the browser ...
// I don't know how to work with real full calendar event objects.
// and making mock objects is too inaccurate i think.