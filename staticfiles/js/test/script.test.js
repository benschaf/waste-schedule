/**
 * @jest-environment jsdom
 */

const {
    test,
    expect
} = require("@jest/globals");
const {
    updateCopyrightNotice
} = require("../script.js");

describe("copyright notice tests", () => {
    test("updateCopyrightNotice updates the year correctly", () => {
        const yearElement = document.createElement("span");
        yearElement.id = "year";
        document.body.appendChild(yearElement);

        updateCopyrightNotice();

        expect(yearElement.innerHTML).toBe("2024");
    });
});