# Cafe Fuencarral
This website is designed for people in Bristol, whether residents or visitors, who are interested in enjoying Spanish tapas, perhaps for the first time. It helps users to see the different types of tapas dishes we offer on our menu and provides the option to book a table. Whether they're specifically seeking Spanish food or just looking for a  place to eat in Bristol, this website makes discovering tapas easy.

## Features

### Hero image and navbar

At the top of every page is the name of the cafe over a background image of some tapas. Directly below the image is the navbar, allowing for easy navigation around the entire website.

![Header](static/images/hero-image-navbar.png)

### Menu

There is a dedicated page for the menu where users can see the food and drinks we offer at the cafe. There is also a link at the bottom of this page that takes the user directly to the reservation screen where they can book a table.

![Menu](static/images/menu.png)

### Reservation part 1

The reservation form is split into two parts, so the customer can know for certain that their chosen time and date are available before they need to provide contact information. This enhances the user experience. Part 1 of the form asks for the date, time, and the number of people.

![Reservation-part1](static/images/reservation-part1.png)

### Reservation part 2

Once the user selects an appropriate time and clicks 'Next', they are taken to Part 2, where they are asked to enter their first and last name and email address. There is then a 'Submit' button to complete the reservation form.

![Reservation-part2](static/images/reservation-part2.png)

### Reservation confirmation

After clicking 'Submit,' the user is taken to the submission confirmation screen. Here, the user receives confirmation that their reservation was successful and is provided with the reservation details, allowing them to verify accuracy. They are also provided with a randomly generated code they can use to access their reservation. Finally, there is a link at the bottom of the screen where the user can go to modify or cancel their reservation.

![Reservation-confirmation](static/images/reservation-confirmation.png)

### Reservation search

If the user wishes to make changes to their reservation, they will first be taken to this screen, where they will need to search for their reservation using the randomly generated code they were given.

![Reservation-search](static/images/reservation-search.png)

### Reservation details

After the user enters their code and clicks 'Search', they will go to the details screen. Here, they will see details of their reservation along with two buttons: 'Modify' and 'Cancel.' 'Modify' will take them to another screen, while 'Cancel' will cancel the reservation.

![Reservation-details](static/images/reservation-details.png)

### Reservation modify

If the user clicks the 'Modify' button, they will be taken to this screen, where they can make changes to their reservation. Once they have made their changes, they can click the 'Update' button to save them.

![Reservation-modify](static/images/reservation-modify.png)

### Update confirmation

After clicking 'Update', the user will be taken to the next screen, where they will receive confirmation that the update has been successful.

![Update-confirmation](static/images/update-confirmation.png)

### Cancellation confirmation

On the modify screen, if the user clicks the 'Cancel' button, they will go to this screen, where they will see confirmation that their reservation has been cancelled.

![Details-cancellation](static/images/details-cancellation.png)

### Colour scheme

The two colours chosen for this website are dark red and gold, which nicely reflect the colours of the Spanish flag. A background image in the main section of every page also gives the website a more Spanish feel. 

### Navigation

Throughout the website, I have added links to other pages where appropriate to help with navigation. For example, after scrolling to the bottom of the menu page, I added a link to the reservation page, allowing the user to quickly jump to that page instead of scrolling back up to the top. Similarly, at the bottom of the homepage, if the user wants to learn more about what the cafe offers, there is a link to the menu page.

![Reservation-link](static/images/reservation-link.png)
![Menu-link](static/images/menu-link.png)


## Testing

### HTML

The code was ran through the [W3C validator](https://validator.w3.org/#validate_by_input), and only one error was found where a '/' was placed in the wrong place in a paragraph tag. The error has been fixed.

### CSS

No errors were found when the CSS code was run through the [Jigsaw Validator](https://jigsaw.w3.org/css-validator/#validate_by_input)

### Python

The code was ran through the [CI Python Linter](https://pep8ci.herokuapp.com/). The only errors were blank whitespaces and lines too long. All errors have been fixed.

### Manual testing

All the fields in the form are mandatory, so the form cannot be submitted without all fields being completed. This works for both Part 1 and Part 2 of the form, with an error message showing otherwise.

If the user selects a date in the past, an error message will let them know this date cannot be selected.

![Date-error](static/images/date-error.png)

There are only 10 tables in the cafe, so if all tables are already booked at a chosen time and date, an error message will show up after 'Next' is clicked, asking the user to select a different time. The user will also not be able to select a time within a two-hour window of a fully booked slot. For example, if there are 10 bookings at 5 pm, the next available booking will be at 7 pm.

![Reservation-error-message](static/images/reservation-error-message.png)

In Part 2 of the form, names and email addresses can still be submitted even if spaces are added at the front or end of entries. Submitting names or email addresses in all lowercase or all uppercase will convert them to the proper format. If an email is submitted in an incorrect format, an error message will prompt the correct format.

If the user searches with an incorrect code, they will receive an error message letting them know that the code does not exist. As above, codes submitted with spaces on either side are still accepted. Similarly, codes entered in lowercase are converted to uppercase.

![Search-error-message](static/images/search-error-message.png)

On the modify screen, if the user changes the time or date to a fully booked slot, they will receive an error message, as with a new reservation. If they select a date in the past, they will also receive an error message.

![Modify-error-message](static/images/modify-error-message.png)

When searching for a reservation that has already been cancelled, a message will display on the details screen to let the user know.

![Details-cancellation](static/images/details-cancellation.png)


## Deployment

The website has been deployed through Heroku.

Steps taken for deployment:
 - Created a new app in Heroku.
 - Gave the app a unique name and chose the appropriate region.
 - Revealed the config vars and added the variables.
 - Linked the new app to the repository in GitHub.
 - Installed the requirements.txt and Procfile.
 - Added web: gunicorn cafefuencarral.wsgi to the Procfile.
 - Deployed the app.


## Accessibility

Running the homepage through Lighthouse shows there are no issues. The website was tested on both mobile and desktop, with very little variation in the scores on the other pages.

![lighthouse-mobile](static/images/lighthouse-mobile.png)
![lighthouse-desktop](static/images/lighthouse-desktop.png)

## Credits

### Content

 - The font was taken from [Google font](https://fonts.google.com/)
 - Website icon downloaded from [Favicon](https://favicon.io/)
 - The social media icons are from [Font Awesome](https://fontawesome.com/).

### Media

Images were taken from various website after searching in Google images
