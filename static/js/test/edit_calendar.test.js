/**
 * @jest-environment jsdom
 */

const { test, expect } = require("@jest/globals");
const { getMaxId } = require("../edit_calendar.js");

// beforeAll(() => {
//     let fs = require("fs");
//     let fileContents = fs.readFileSync("index.html", "utf-8");
//     document.open();
//     document.write(fileContents);
//     document.close();
// });

test("getMaxId returns the maximum id of the events", () => {
    let events = [
        { id: 0 },
        { id: 1 },
        { id: 2 }
    ];
    expect(getMaxId(events)).toBe(3);
});