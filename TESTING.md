# Testing

> [!NOTE]
> Return back to the [README.md](README.md) file.

## Code Validation

### HTML

I have used the recommended [HTML W3C Validator](https://validator.w3.org) to validate all of my HTML deployed source code. In the table below, the results are by template file that would render the respective page.

| Directory | File | Screenshot | Notes |
| --- | --- | --- | --- |
| core | about.html | ![screenshot](documentation/validation-about.png) | no warnings or errors |
| core | index.html | ![screenshot](documentation/validation-index.png) | no warnings or errors |
| schedulebuilder | calendar.html | ![screenshot](documentation/validation-calendar.png) | no warnings or errors |
| schedulebuilder | location_form.html | ![screenshot](documentation/validation-location-form.png) | no warnings or errors |
| schedulebuilder | schedule_confirm_delete.html | ![screenshot](documentation/validation-schedule-confirm-delete.png) | no warnings or errors |
| schedulebuilder | schedule_form.html | ![screenshot](documentation/validation-schedule-form.png) | no warnings or errors |
| schedulebuilder | update_schedule_form.html | ![screenshot](documentation/validation-update-schedule-form.png) | no warnings or errors |
| templates | 404.html | ![screenshot](documentation/validation-404.png) | no warnings or errors |
| templates | 500.html | ![screenshot](documentation/validation-500.png) | no warnings or errors |
| wasteschedules | dashboard.html | ![screenshot](documentation/validation-dashboard.png) | no warnings or errors |
| wasteschedules | schedule_detail.html | ![screenshot](documentation/validation-schedule-detail.png) | no warnings or errors |
| wasteschedules | schedule_list.html | ![screenshot](documentation/validation-schedule-list.png) | no warnings or errors |

### CSS

I have used the recommended [CSS Jigsaw Validator](https://jigsaw.w3.org/css-validator) to validate all of my CSS files.

![jigsaw badge](http://jigsaw.w3.org/css-validator/images/vcss-blue)

| Directory | File | Screenshot | Notes |
| --- | --- | --- | --- |
| static | style.css | ![screenshot](documentation/validation-css.png) | no errors, 51 Warnings |

The warnings are due to the vendor prefixes that are used in the CSS file. I added the prefixes using the [Autoprefixer](https://autoprefixer.github.io) tool. The prefixes are necessary for the CSS to work on all browsers.

There is one other warning that is due to the background color and border of the calendar events having the same color value. This was necessary in order to override the default FullCalendar styling.

### JavaScript

I have used the recommended [JShint Validator](https://jshint.com) via its command-line interface to validate all of my JavaScript files. for this I installed the jshint package as a dev dependency using the command `npm install jshint --save-dev`. After this I created a `.jshintrc` file in the root of the project with the following content in order to enable ES6 syntax:

```json
{
    "esversion": 6
}
```

I then ran the following command to validate all of my JavaScript files: `npx jshint <directory>/<filename.js>`:

| Directory | File | Screenshot | Notes |
| --- | --- | --- | --- |
| static | comments.js | ![screenshot](documentation/js-validation-comments.png) | Warning about a function within a loop. This is not an issue as the function is only referencing and not changing the document object. It is used to create a form for each comment. |
| static | dashboard.js | ![screenshot](documentation/js-validation-dashboard.png) | Warning about a function within a loop. This is not an issue as the function is only referencing and not changing the document object. It is used to trigger a modal for a click on any download button. |
| static | edit_calendar.js | ![screenshot](documentation/js-validation-edit-calendar.png) | no warnings or errors |
| static | index.js | ![screenshot](documentation/js-validation-index.png) | no warnings or errors |
| static | only_schedule.js | ![screenshot](documentation/js-validation-only-schedule.png) | no warnings or errors |
| static | script.js | ![screenshot](documentation/js-validation-script.png) | no warnings or errors |
| static/test | edit_calendar.test.js | ![screenshot](documentation/js-validation-edit-calendar-test.png) | warning about document.write. This is save to ignore as it is used to load my own HTML template file for testing. |

### Python

I have used the recommended [PEP8 CI Python Linter](https://pep8ci.herokuapp.com) to validate all of my Python files.

Files that are unchanged from the Django template have been excluded from the validation as they are known to be valid.

| Directory | File | CI URL | Screenshot | Notes |
| --- | --- | --- | --- | --- |
|  | copy-credits.py | [PEP8 CI](https://pep8ci.herokuapp.com/https://raw.githubusercontent.com/benschaf/waste-schedule/main/copy-credits.py) | ![screenshot](documentation/python-validation-copy-credits.png) | |
| core | urls.py | [PEP8 CI](https://pep8ci.herokuapp.com/https://raw.githubusercontent.com/benschaf/waste-schedule/main/core/urls.py) | ![screenshot](documentation/python-validation-core-urls.png) | |
| core | views.py | [PEP8 CI](https://pep8ci.herokuapp.com/https://raw.githubusercontent.com/benschaf/waste-schedule/main/core/views.py) | ![screenshot](documentation/python-validation-core-views.png) | |
| schedulebuilder | admin.py | [PEP8 CI](https://pep8ci.herokuapp.com/https://raw.githubusercontent.com/benschaf/waste-schedule/main/schedulebuilder/admin.py) | ![screenshot](documentation/python-validation-schedulebuilder-admin.png) | |
| schedulebuilder | forms.py | [PEP8 CI](https://pep8ci.herokuapp.com/https://raw.githubusercontent.com/benschaf/waste-schedule/main/schedulebuilder/forms.py) | ![screenshot](documentation/python-validation-schedulebuilder-forms.png) | |
| schedulebuilder | models.py | [PEP8 CI](https://pep8ci.herokuapp.com/https://raw.githubusercontent.com/benschaf/waste-schedule/main/schedulebuilder/models.py) | ![screenshot](documentation/python-validation-schedulebuilder-models.png) | |
| schedulebuilder | urls.py | [PEP8 CI](https://pep8ci.herokuapp.com/https://raw.githubusercontent.com/benschaf/waste-schedule/main/schedulebuilder/urls.py) | ![screenshot](documentation/python-validation-schedulebuilder-urls.png) | |
| schedulebuilder | views.py | [PEP8 CI](https://pep8ci.herokuapp.com/https://raw.githubusercontent.com/benschaf/waste-schedule/main/schedulebuilder/views.py) | ![screenshot](documentation/python-validation-schedulebuilder-views.png) | |
| tonne | settings.py | [PEP8 CI](https://pep8ci.herokuapp.com/https://raw.githubusercontent.com/benschaf/waste-schedule/main/tonne/settings.py) | ![screenshot](documentation/python-validation-tonne-settings.png) | |
| tonne | urls.py | [PEP8 CI](https://pep8ci.herokuapp.com/https://raw.githubusercontent.com/benschaf/waste-schedule/main/tonne/urls.py) | ![screenshot](documentation/python-validation-tonne-urls.png) | |
| wasteschedules | admin.py | [PEP8 CI](https://pep8ci.herokuapp.com/https://raw.githubusercontent.com/benschaf/waste-schedule/main/wasteschedules/admin.py) | ![screenshot](documentation/python-validation-wasteschedules-admin.png) | |
| wasteschedules | forms.py | [PEP8 CI](https://pep8ci.herokuapp.com/https://raw.githubusercontent.com/benschaf/waste-schedule/main/wasteschedules/forms.py) | ![screenshot](documentation/python-validation-wasteschedules-forms.png) | |
| wasteschedules | models.py | [PEP8 CI](https://pep8ci.herokuapp.com/https://raw.githubusercontent.com/benschaf/waste-schedule/main/wasteschedules/models.py) | ![screenshot](documentation/python-validation-wasteschedules-models.png) | |
| wasteschedules | urls.py | [PEP8 CI](https://pep8ci.herokuapp.com/https://raw.githubusercontent.com/benschaf/waste-schedule/main/wasteschedules/urls.py) | ![screenshot](documentation/python-validation-wasteschedules-urls.png) | |
| wasteschedules | views.py | [PEP8 CI](https://pep8ci.herokuapp.com/https://raw.githubusercontent.com/benschaf/waste-schedule/main/wasteschedules/views.py) | ![screenshot](documentation/python-validation-wasteschedules-views.png) | |

Test Files were validated, too:

| Directory | File | CI URL | Screenshot | Notes |
| --- | --- | --- | --- | --- |
| core | test_views.py | [PEP8 CI](https://pep8ci.herokuapp.com/https://raw.githubusercontent.com/benschaf/waste-schedule/main/core/test_views.py) | ![screenshot](documentation/python-validation-core-test-views.png) | |
| schedulebuilder | test_forms.py | [PEP8 CI](https://pep8ci.herokuapp.com/https://raw.githubusercontent.com/benschaf/waste-schedule/main/schedulebuilder/test_forms.py) | ![screenshot](documentation/python-validation-schedulebuilder-test-forms.png) | |
| schedulebuilder | test_views.py | [PEP8 CI](https://pep8ci.herokuapp.com/https://raw.githubusercontent.com/benschaf/waste-schedule/main/schedulebuilder/test_views.py) | ![screenshot](documentation/python-validation-schedulebuilder-test-views.png) | |
| wasteschedules | test_forms.py | [PEP8 CI](https://pep8ci.herokuapp.com/https://raw.githubusercontent.com/benschaf/waste-schedule/main/wasteschedules/test_forms.py) | ![screenshot](documentation/python-validation-wasteschedules-test-forms.png) | |
| wasteschedules | test_views.py | [PEP8 CI](https://pep8ci.herokuapp.com/https://raw.githubusercontent.com/benschaf/waste-schedule/main/wasteschedules/test_views.py) | ![screenshot](documentation/python-validation-wasteschedules-test-views.png) | |

Additionaly to the final testing, pycodestyle was used frequently to test python files locally.

## Browser Compatibility

I've tested my deployed project manually on multiple browsers to check for compatibility issues.

| Browser | Landing | Schedule List | Schedule Detail | Schedule Builder | Dashboard | About | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Chrome | ![screenshot](documentation/browser-chrome-landing.png) | ![screenshot](documentation/browser-chrome-schedule-list.png) | ![screenshot](documentation/browser-chrome-schedule-detail.png) | ![screenshot](documentation/browser-chrome-schedule-builder.png) | ![screenshot](documentation/browser-chrome-dashboard.png) | ![screenshot](documentation/browser-chrome-about.png) | no issues |
| Firefox | ![screenshot](documentation/browser-firefox-landing.png) | ![screenshot](documentation/browser-firefox-schedule-list.png) | ![screenshot](documentation/browser-firefox-schedule-detail.png) | ![screenshot](documentation/browser-firefox-schedule-builder.png) | ![screenshot](documentation/browser-firefox-dashboard.png) | ![screenshot](documentation/browser-firefox-about.png) | no issues |
| Edge | ![screenshot](documentation/browser-edge-landing.png) | ![screenshot](documentation/browser-edge-schedule-list.png) | ![screenshot](documentation/browser-edge-schedule-detail.png) | ![screenshot](documentation/browser-edge-schedule-builder.png) | ![screenshot](documentation/browser-edge-dashboard.png) | ![screenshot](documentation/browser-edge-about.png) | no issues |
| Brave | ![screenshot](documentation/browser-brave-landing.png) | ![screenshot](documentation/browser-brave-schedule-list.png) | ![screenshot](documentation/browser-brave-schedule-detail.png) | ![screenshot](documentation/browser-brave-schedule-builder.png) | ![screenshot](documentation/browser-brave-dashboard.png) | ![screenshot](documentation/browser-brave-about.png) | no issues |
| Opera | ![screenshot](documentation/browser-opera-landing.png) | ![screenshot](documentation/browser-opera-schedule-list.png) | ![screenshot](documentation/browser-opera-schedule-detail.png) | ![screenshot](documentation/browser-opera-schedule-builder.png) | ![screenshot](documentation/browser-opera-dashboard.png) | ![screenshot](documentation/browser-opera-about.png) | no issues |
| Safari | ![screenshot](documentation/browser-safari-landing.png) | ![screenshot](documentation/browser-safari-schedule-list.png) | ![screenshot](documentation/browser-safari-schedule-detail.png) | ![screenshot](documentation/browser-safari-schedule-builder.png) | ![screenshot](documentation/browser-safari-dashboard.png) | ![screenshot](documentation/browser-safari-about.png) | minor differences but no issues |

## Responsiveness

I've tested my deployed project on multiple devices to check for responsiveness issues. I've used the Chrome Developer Tools to simulate the devices. I have also tested the project on a physical Google Pixel 6 device.

| Device | Landing | Schedule List | Schedule Detail | Schedule Builder | Dashboard | About | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Mobile (DevTools: iPhone 12 Pro) | ![screenshot](documentation/responsive-mobile-landing.png) | ![screenshot](documentation/responsive-mobile-schedule-list.png) | ![screenshot](documentation/responsive-mobile-schedule-detail.png) | ![screenshot](documentation/responsive-mobile-schedule-builder.png) | ![screenshot](documentation/responsive-mobile-dashboard.png) | ![screenshot](documentation/responsive-mobile-about.png) | Works as expected |
| Tablet (DevTools: iPad Air) | ![screenshot](documentation/responsive-tablet-landing.png) | ![screenshot](documentation/responsive-tablet-schedule-list.png) | ![screenshot](documentation/responsive-tablet-schedule-detail.png) | ![screenshot](documentation/responsive-tablet-schedule-builder.png) | ![screenshot](documentation/responsive-tablet-dashboard.png) | ![screenshot](documentation/responsive-tablet-about.png) | Works as expected |
| Desktop (1920 x 1080) | ![screenshot](documentation/responsive-desktop-landing.png) | ![screenshot](documentation/responsive-desktop-schedule-list.png) | ![screenshot](documentation/responsive-desktop-schedule-detail.png) | ![screenshot](documentation/responsive-desktop-schedule-builder.png) | ![screenshot](documentation/responsive-desktop-dashboard.png) | ![screenshot](documentation/responsive-desktop-about.png) | Works as expected |
| Google Pixel 6 | ![screenshot](documentation/responsive-pixel-landing.png) | ![screenshot](documentation/responsive-pixel-schedule-list.png) | ![screenshot](documentation/responsive-pixel-schedule-detail.png) | ![screenshot](documentation/responsive-pixel-schedule-builder.png) | ![screenshot](documentation/responsive-pixel-dashboard.png) | ![screenshot](documentation/responsive-pixel-about.png) | Works as expected |

There were no responsiveness issues on any of the devices tested.

## Lighthouse Audit

I've tested my deployed project using the Lighthouse Audit tool in the Chrome Developer Tools to mainly check for accessibility and best practices but also to check for performance and SEO.

| Page | Mobile | Desktop | Notes |
| --- | --- | --- | --- |
| Landing | ![screenshot](documentation/lighthouse-landing-mobile.png) | ![screenshot](documentation/lighthouse-landing-desktop.png) |  Warnings about performance due to hero image and layout shift (acceptable) |
| About | ![screenshot](documentation/lighthouse-about-mobile.png) | ![screenshot](documentation/lighthouse-about-desktop.png) | Minor warnings |
| Schedule List | ![screenshot](documentation/lighthouse-schedule-list-mobile.png) | ![screenshot](documentation/lighthouse-schedule-list-desktop.png) | Minor warnings |
| Schedule Detail | ![screenshot](documentation/lighthouse-schedule-detail-mobile.png) | ![screenshot](documentation/lighthouse-schedule-detail-desktop.png) | Warnings due to schedule image loading, layout shift, and "links aren't crawlable" |
| Dashboard | ![screenshot](documentation/lighthouse-dashboard-mobile.png) | ![screenshot](documentation/lighthouse-dashboard-desktop.png) | Minor warnings |
| Builder Location | ![screenshot](documentation/lighthouse-builder-location-mobile.png) | ![screenshot](documentation/lighthouse-builder-location-desktop.png) | Minor warnings |
| Builder Schedule | ![screenshot](documentation/lighthouse-builder-schedule-mobile.png) | ![screenshot](documentation/lighthouse-builder-schedule-desktop.png) | Minor warnings |
| Builder Calendar | ![screenshot](documentation/lighthouse-builder-calendar-mobile.png) | ![screenshot](documentation/lighthouse-builder-calendar-desktop.png) | Minor warnings and "links aren't crawlable" |
| Register | ![screenshot](documentation/lighthouse-register-mobile.png) | ![screenshot](documentation/lighthouse-register-desktop.png) | Minor warnings |
| Login | ![screenshot](documentation/lighthouse-login-mobile.png) | ![screenshot](documentation/lighthouse-login-desktop.png) | Minor warnings |

The "links aren't crawlable" warning is due to FullCalendar which puts some anchor tags into the DOM that aren't actually links. These links not being crawlable is not an issue as they are not meant to be followed by search engines and are only used for FullCalendar's internal functionality.

## Defensive Programming

🛑🛑🛑🛑🛑🛑🛑🛑🛑🛑-START OF NOTES (to be deleted)

Forms:
- Users cannot submit an empty form
- Users must enter valid email addresses

MS3 (Flask) | MS4/PP4/PP5 (Django):
- Users cannot brute-force a URL to navigate to a restricted page
- Users cannot perform CRUD functionality while logged-out
- User-A should not be able to manipulate data belonging to User-B, or vice versa
- Non-Authenticated users should not be able to access pages that require authentication
- Standard users should not be able to access pages intended for superusers


🛑🛑🛑🛑🛑🛑🛑🛑🛑🛑-END OF NOTES (to be deleted)

Defensive programming was manually tested with the below user acceptance testing:

| Page | Expectation | Test | Result | Fix | Screenshot |
| --- | --- | --- | --- | --- | --- |
| **Landing** | | | | | |
| | The Postcode field should only accept values made up of 5 digits | Tested the field by entering an empty form, a 6-digit value, a 5-non-digit value, and a 5-digit value | The field only accepted the 5-digit value | Test concluded and passed | ![screenshot](documentation/defensive-landing-postcode.png) |
| **Schedule List** | | | | | |
| | The Poscrode field should only accept values made up of 5 digits | Tested the field by entering an empty form, a 6-digit value, a 5-non-digit value, and a 5-digit value | The field only accepted the 5-digit value | Test concluded and passed | ![screenshot](documentation/defensive-schedule-list-postcode.png) |
| | The Like Button should only perform a CRUD operation for a logged-in user | Tested the button while logged out and while logged in | The button only performed the CRUD operation while logged in | Test concluded and passed | ![screenshot](documentation/defensive-schedule-list-like.png) |
| | The Subscribe Button should only perform a CRUD operation for a logged-in user | Tested the button while logged out and while logged in | The button only performed the CRUD operation while logged in | Test concluded and passed | ![screenshot](documentation/defensive-schedule-list-subscribe.png) |
| | **Schedule Detail** | | | | |
| | The Like Button should only perform a CRUD operation for a logged-in user | Tested the button while logged out and while logged in | The button only performed the CRUD operation while logged in | Test concluded and passed | ![screenshot](documentation/defensive-schedule-detail-like.png) |
| | The Subscribe Button should only perform a CRUD operation for a logged-in user | Tested the button while logged out and while logged in | The button only performed the CRUD operation while logged in | Test concluded and passed | ![screenshot](documentation/defensive-schedule-detail-subscribe.png) |
| | The Edit Schedule and Delete Schedule Buttons should only be available to the user who created the schedule | Tested the buttons while logged in as the creator and as a different user | The buttons were only available to the creator | Test concluded and passed | ![screenshot](documentation/defensive-schedule-detail-edit-delete.png) |
| | The Edit Schedule URL should not be accessible if brute forced by a user who is not the creator of the Schedule | Attempted to brute force the [URL](https://tonne-waste-reminders-a6836f2888b0.herokuapp.com/schedule-builder/edit-schedule/kleingarnstadt) | The user was redirected to the landing page and the message was displayed: "You are not the owner of this schedule" | Test concluded and passed | ![screenshot](documentation/defensive-schedule-detail-brute-force.png) |
| | The Delete Schedule URL should not be accessible if brute forced by a user who is not the creator of the Schedule | Attempted to brute force the [URL](https://tonne-waste-reminders-a6836f2888b0.herokuapp.com/schedule-builder/delete-schedule/kleingarnstadt) | The user was redirected to the landing page and the message was displayed: "You are not the owner of this schedule" | Test concluded and passed | ![screenshot](documentation/defensive-schedule-detail-brute-force.png) |
| | The Comment field and button should only be available to a logged-in user | Tested the field and button while logged out and while logged in | The field and button were only available while logged in | Test concluded and passed | ![screenshot](documentation/defensive-schedule-detail-comment.png) |
| | The Comment URL should not be accessible if brute forced by a user | Attempted to brute force the [URL](https://tonne-waste-reminders-a6836f2888b0.herokuapp.com/wasteschedules/schedule-comment/kleingarnstadt) | The user was redirected to the relevant schedule detail page | Test concluded and passed | ![screenshot](documentation/defensive-schedule-detail-brute-force.png) |
| | The Comment field should only accept freeform text | Tested the field by entering an empty form, a form with only spaces, and a form with text | The field only accepted the form with text | Test concluded and passed | ![screenshot](documentation/defensive-schedule-detail-comment.png) |
| | A valid Comment should only be submitted by a logged-in user | Tested the form by entering a comment while logged out and while logged in | The comment was only submitted while logged in | Test concluded and passed | ![screenshot](documentation/defensive-schedule-detail-comment.png) |
| | The Edit and Delete Buttons for a Comment should only be available to the user who created the Comment | Tested the buttons while logged in as the creator and as a different user | The buttons were only available to the creator | Test concluded and passed | ![screenshot](documentation/defensive-schedule-detail-comment-edit-delete.png) |
| | The Edit Comment URL should not be accessible if brute forced by a user who is not the creator of the Comment | Attempted to brute force the [URL](https://tonne-waste-reminders-a6836f2888b0.herokuapp.com/wasteschedules/schedule-comment-update/27/kleingarnstadt) | The user was redirected to the landing page and a message was displayed "please use the edit button to edit your comment." | Test concluded and passed | ![screenshot](documentation/defensive-schedule-detail-comment-brute-force.png) |

!!! ADD THE REST OF THE TESTS FOR THE REMAINING PAGES !!!
beofore refer to the question in issue  [#47](https://github.com/benschaf/waste-schedule/issues/47)

## User Story Testing

| User Story | Screenshot |
| --- | --- |
| [#3](https://github.com/benschaf/waste-schedule/issues/3) As a user, I want an intuitive landing page that explains the app’s purpose and features clearly, so that I can quickly understand how to use it. | ![screenshot](documentation/feature-landing.png) |
| [#13](https://github.com/benschaf/waste-schedule/issues/13) As a user I can instantly find relevant information for my area when visiting the website so that I can get right into setting up the reminders I came for | ![screenshot](documentation/feature-search.png) |
| [#5](https://github.com/benschaf/waste-schedule/issues/5) As a user, I want to be able to browse waste collection schedules for my area without logging in, so that I can explore available options easily. | ![screenshot](documentation/feature-search.png) |
| [#6](https://github.com/benschaf/waste-schedule/issues/6) As a user, I want to only have to log in, when I want to subscribe to a schedule or make a schedule so that I can explore as much of the site without being distracted by a log in screen. | ![screenshot](documentation/feature-detail.png) |
| [#14](https://github.com/benschaf/waste-schedule/issues/14) As a user I can click on a specific waste collection schedule from the search results and view detailed information about that schedule so that I can confirm that it's helpful for me | ![screenshot](documentation/feature-detail.png) |
| [#15](https://github.com/benschaf/waste-schedule/issues/15) As a user, I can subscribe to waste collection schedules so that I receive timely reminders for upcoming collection events. (notice the download button) | ![screenshot](documentation/feature-dashboard.png) |
| [#17](https://github.com/benschaf/waste-schedule/issues/17) As a user I can view a dashboard that provides relevant information on my subscribed schedules so that I can stay organized and have an overview of what I subscribed to. | ![screenshot](documentation/feature-dashboard.png) |
| [#10](https://github.com/benschaf/waste-schedule/issues/10) As a user, I want to upload my community’s waste collection schedule, so that others can benefit from accurate information. | ![screenshot](documentation/feature-builder2.png) |
| [#12](https://github.com/benschaf/waste-schedule/issues/12) As a user, I want to verify the accuracy of uploaded schedules by comparing them with official waste calendars or images, so that I can trust the data. | ![screenshot](documentation/feature-detail.png) |
| [#11](https://github.com/benschaf/waste-schedule/issues/11) As a user, I want to rate and provide feedback on uploaded schedules to help the community, so that we collectively improve waste management. | ![screenshot](documentation/feature-comments.png) |
| [#18](https://github.com/benschaf/waste-schedule/issues/18) As a user who commented on a schedule I can edit or delete my comment so that I can refine or retract my feedback. | ![screenshot](documentation/feature-comments.png) |
| [#19](https://github.com/benschaf/waste-schedule/issues/19) As a user I can like or express appreciation for a specific waste collection schedule so that I can acknowledge well-maintained schedules. | ![screenshot](documentation/feature-search.png) |

## Automated Testing

I have conducted a series of automated tests on my application.

I fully acknowledge and understand that, in a real-world scenario, an extensive set of additional tests would be more comprehensive.

### JavaScript (Jest Testing)

I have used the [Jest](https://jestjs.io) JavaScript testing framework to test the application functionality.

In order to work with Jest, I first had to initialize NPM.

- `npm init`
- Hit `enter` for all options, except for **test command:**, just type `jest`.

Add Jest to a list called **Dev Dependencies** in a dev environment:

- `npm install --save-dev jest`

**IMPORTANT**: Initial configurations

When creating test files, the name of the file needs to be `file-name.test.js` in order for Jest to properly work.

Without the following, Jest won't properly run the tests:

- `npm install -D jest-environment-jsdom`

Due to a change in Jest's default configuration, you'll need to add the following code to the top of the `.test.js` file:

```js
/**
 * @jest-environment jsdom
 */

const { test, expect } = require("@jest/globals");
const { function1, function2, function3, etc. } = require("../script-name");

beforeAll(() => {
    let fs = require("fs");
    let fileContents = fs.readFileSync(
        "/workspace/waste-schedule/schedulebuilder/templates/schedulebuilder/calendar.html", "utf-8");
    document.open();
    document.write(fileContents);
    document.close();
});
```

Remember to adjust the `fs.readFileSync()` to the specific file you'd like you test.
The example above is testing the `calendar.html` file.

Finally, at the bottom of the script file where your primary scripts are written, include the following at the bottom of the file.
Make sure to include the name of all of your functions that are being tested in the `.test.js` file.

```js
if (typeof module !== "undefined") module.exports = {
    function1, function2, function3, etc.
};
```

Now that these steps have been undertaken, further tests can be written, and be expected to fail initially.
Write JS code that can get the tests to pass as part of the Red-Green refactor process.

Once ready, to run the tests, use this command:

- `npm test`

**NOTE**: To obtain a coverage report, use the following command:

- `npm test --coverage`

Below are the results from the tests that I've written for this application:

| Test Suites | Tests | Screenshot |
| --- | --- | --- |
| 1 passed | 16 passed | ![screenshot](documentation/tests/js-test-coverage.png) |
| x | x | repeat for all remaining tests |

#### Jest Test Issues

🛑🛑🛑🛑🛑🛑🛑🛑🛑🛑-START OF NOTES (to be deleted)

Use this section to list any known issues you ran into while writing your Jest tests.
Remember to include screenshots (where possible), and a solution to the issue (if known).

This can be used for both "fixed" and "unresolved" issues.

🛑🛑🛑🛑🛑🛑🛑🛑🛑🛑-END OF NOTES (to be deleted)

### Python (Unit Testing)

🛑🛑🛑🛑🛑🛑🛑🛑🛑🛑-START OF NOTES (to be deleted)

Adjust the code below (file names, etc.) to match your own project files/folders.

🛑🛑🛑🛑🛑🛑🛑🛑🛑🛑-END OF NOTES (to be deleted)

I have used Django's built-in unit testing framework to test the application functionality.

In order to run the tests, I ran the following command in the terminal each time:

`python3 manage.py test name-of-app `

To create the coverage report, I would then run the following commands:

`coverage run --source=name-of-app manage.py test`

`coverage report`

To see the HTML version of the reports, and find out whether some pieces of code were missing, I ran the following commands:

`coverage html`

`python3 -m http.server`

Below are the results from the various apps on my application that I've tested:

| App | File | Coverage | Screenshot |
| --- | --- | --- | --- |
| Bag | test_forms.py | 99% | ![screenshot](documentation/tests/py-test-bag-forms.png) |
| Bag | test_models.py | 89% | ![screenshot](documentation/tests/py-test-bag-models.png) |
| Bag | test_urls.py | 100% | ![screenshot](documentation/tests/py-test-bag-urls.png) |
| Bag | test_views.py | 71% | ![screenshot](documentation/tests/py-test-bag-views.png) |
| Checkout | test_forms.py | 99% | ![screenshot](documentation/tests/py-test-checkout-forms.png) |
| Checkout | test_models.py | 89% | ![screenshot](documentation/tests/py-test-checkout-models.png) |
| Checkout | test_urls.py | 100% | ![screenshot](documentation/tests/py-test-checkout-urls.png) |
| Checkout | test_views.py | 71% | ![screenshot](documentation/tests/py-test-checkout-views.png) |
| Home | test_forms.py | 99% | ![screenshot](documentation/tests/py-test-home-forms.png) |
| Home | test_models.py | 89% | ![screenshot](documentation/tests/py-test-home-models.png) |
| Home | test_urls.py | 100% | ![screenshot](documentation/tests/py-test-home-urls.png) |
| Home | test_views.py | 71% | ![screenshot](documentation/tests/py-test-home-views.png) |
| Products | test_forms.py | 99% | ![screenshot](documentation/tests/py-test-products-forms.png) |
| Products | test_models.py | 89% | ![screenshot](documentation/tests/py-test-products-models.png) |
| Products | test_urls.py | 100% | ![screenshot](documentation/tests/py-test-products-urls.png) |
| Products | test_views.py | 71% | ![screenshot](documentation/tests/py-test-products-views.png) |
| Profiles | test_forms.py | 99% | ![screenshot](documentation/tests/py-test-profiles-forms.png) |
| Profiles | test_models.py | 89% | ![screenshot](documentation/tests/py-test-profiles-models.png) |
| Profiles | test_urls.py | 100% | ![screenshot](documentation/tests/py-test-profiles-urls.png) |
| Profiles | test_views.py | 71% | ![screenshot](documentation/tests/py-test-profiles-views.png) |
| x | x | x | repeat for all remaining tested apps/files |

#### Unit Test Issues

🛑🛑🛑🛑🛑🛑🛑🛑🛑🛑-START OF NOTES (to be deleted)

Use this section to list any known issues you ran into while writing your unit tests.
Remember to include screenshots (where possible), and a solution to the issue (if known).

This can be used for both "fixed" and "unresolved" issues.

🛑🛑🛑🛑🛑🛑🛑🛑🛑🛑-END OF NOTES (to be deleted)

## Bugs

🛑🛑🛑🛑🛑🛑🛑🛑🛑🛑-START OF NOTES (to be deleted)

This section is primarily used for JavaScript and Python applications,
but feel free to use this section to document any HTML/CSS bugs you might run into.

It's very important to document any bugs you've discovered while developing the project.
Make sure to include any necessary steps you've implemented to fix the bug(s) as well.

**PRO TIP**: screenshots of bugs are extremely helpful, and go a long way!

🛑🛑🛑🛑🛑🛑🛑🛑🛑🛑-END OF NOTES (to be deleted)

- JS Uncaught ReferenceError: `foobar` is undefined/not defined

    ![screenshot](documentation/bugs/bug01.png)

    - To fix this, I _____________________.

- JS `'let'` or `'const'` or `'template literal syntax'` or `'arrow function syntax (=>)'` is available in ES6 (use `'esversion: 11'`) or Mozilla JS extensions (use moz).

    ![screenshot](documentation/bugs/bug02.png)

    - To fix this, I _____________________.

- Python `'ModuleNotFoundError'` when trying to import module from imported package

    ![screenshot](documentation/bugs/bug03.png)

    - To fix this, I _____________________.

- Django `TemplateDoesNotExist` at /appname/path appname/template_name.html

    ![screenshot](documentation/bugs/bug04.png)

    - To fix this, I _____________________.

- Python `E501 line too long` (93 > 79 characters)

    ![screenshot](documentation/bugs/bug04.png)

    - To fix this, I _____________________.

### GitHub **Issues**

🛑🛑🛑🛑🛑🛑🛑🛑🛑🛑-START OF NOTES (to be deleted)

An improved way to manage bugs is to use the built-in **Issues** tracker on your GitHub repository.
To access your Issues, click on the "Issues" tab at the top of your repository.
Alternatively, use this link: https://github.com/benschaf/waste-schedule/issues

If using the Issues tracker for your bug management, you can simplify the documentation process.
Issues allow you to directly paste screenshots into the issue without having to first save the screenshot locally,
then uploading into your project.

You can add labels to your issues (`bug`), assign yourself as the owner, and add comments/updates as you progress with fixing the issue(s).

Once you've sorted the issue, you should then "Close" it.

When showcasing your bug tracking for assessment, you can use the following format:

🛑🛑🛑🛑🛑🛑🛑🛑🛑🛑-END OF NOTES (to be deleted)

**Fixed Bugs**

[![GitHub issue custom search](https://img.shields.io/github/issues-search?query=repo%3Abenschaf%2Fwaste-schedule%20label%3Abug&label=bugs)](https://github.com/benschaf/waste-schedule/issues?q=is%3Aissue+is%3Aclosed+label%3Abug)

All previously closed/fixed bugs can be tracked [here](https://github.com/benschaf/waste-schedule/issues?q=is%3Aissue+is%3Aclosed).

| Bug | Status |
| --- | --- |
| [JS Uncaught ReferenceError: `foobar` is undefined/not defined](https://github.com/benschaf/waste-schedule/issues/1) | Closed |
| [Python `'ModuleNotFoundError'` when trying to import module from imported package](https://github.com/benschaf/waste-schedule/issues/2) | Closed |
| [Django `TemplateDoesNotExist` at /appname/path appname/template_name.html](https://github.com/benschaf/waste-schedule/issues/3) | Closed |

**Open Issues**

[![GitHub issues](https://img.shields.io/github/issues/benschaf/waste-schedule)](https://github.com/benschaf/waste-schedule/issues)
[![GitHub closed issues](https://img.shields.io/github/issues-closed/benschaf/waste-schedule)](https://github.com/benschaf/waste-schedule/issues?q=is%3Aissue+is%3Aclosed)

Any remaining open issues can be tracked [here](https://github.com/benschaf/waste-schedule/issues).

| Bug | Status |
| --- | --- |
| [JS `'let'` or `'const'` or `'template literal syntax'` or `'arrow function syntax (=>)'` is available in ES6 (use `'esversion: 11'`) or Mozilla JS extensions (use moz).](https://github.com/benschaf/waste-schedule/issues/4) | Open |
| [Python `E501 line too long` (93 > 79 characters)](https://github.com/benschaf/waste-schedule/issues/5) | Open |

## Unfixed Bugs

🛑🛑🛑🛑🛑🛑🛑🛑🛑🛑-START OF NOTES (to be deleted)

You will need to mention unfixed bugs and why they were not fixed.
This section should include shortcomings of the frameworks or technologies used.
Although time can be a big variable to consider, paucity of time and difficulty understanding
implementation is not a valid reason to leave bugs unfixed.

If you've identified any unfixed bugs, no matter how small, be sure to list them here.
It's better to be honest and list them, because if it's not documented and an assessor finds the issue,
they need to know whether or not you're aware of them as well, and why you've not corrected/fixed them.

Some examples:

🛑🛑🛑🛑🛑🛑🛑🛑🛑🛑-END OF NOTES (to be deleted)

- On devices smaller than 375px, the page starts to have `overflow-x` scrolling.

    ![screenshot](documentation/bugs/unfixed-bug01.png)

    - Attempted fix: I tried to add additional media queries to handle this, but things started becoming too small to read.

- For PP3, when using a helper `clear()` function, any text above the height of the terminal does not clear, and remains when you scroll up.

    ![screenshot](documentation/bugs/unfixed-bug02.png)

    - Attempted fix: I tried to adjust the terminal size, but it only resizes the actual terminal, not the allowable area for text.

- When validating HTML with a semantic `section` element, the validator warns about lacking a header `h2-h6`. This is acceptable.

    ![screenshot](documentation/bugs/unfixed-bug03.png)

    - Attempted fix: this is a known warning and acceptable, and my section doesn't require a header since it's dynamically added via JS.

🛑🛑🛑🛑🛑🛑🛑🛑🛑🛑-START OF NOTES (to be deleted)

If you legitimately cannot find any unfixed bugs or warnings, then use the following sentence:

🛑🛑🛑🛑🛑🛑🛑🛑🛑🛑-END OF NOTES (to be deleted)

> [!NOTE]
> There are no remaining bugs that I am aware of.
