// Smooth scrolling for section links with offset
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();

        const sectionId = this.getAttribute('href');
        const section = document.querySelector(sectionId);

        if (section) {
            const navHeight = document.querySelector('header').offsetHeight; // Get the height of the navigation bar
            const additionalOffset = 20; // Additional offset
            const offset = section.getBoundingClientRect().top + window.scrollY - navHeight - additionalOffset;
            window.scrollTo({
                top: offset,
                behavior: 'smooth'
            });
        }
    });
});


// PERSONAL INFORMATION SECTION
// Checks criminal_conviction_status checkbox and displays additional question based on status
const checkbox = document.getElementById('criminal_conviction_status');
const reasonForConvictionDiv = document.querySelector('.reason_for_conviction_div');
const reasonForConvictionTextarea = document.getElementById('reason_for_conviction');

checkbox.addEventListener('change', function() {
    // Toggle the display of the reasonForConvictionDiv
    reasonForConvictionDiv.style.display = this.checked ? 'flex' : 'none';

    // Enable or disable the textarea based on the checkbox state
    reasonForConvictionTextarea.disabled = !this.checked;

    // Clear the textarea if checkbox is unchecked
    if (!this.checked) {
        reasonForConvictionTextarea.value = "";
    }
});

document.addEventListener('DOMContentLoaded', function() {
    const form = document.querySelector('form');
    form.addEventListener('submit', function(e) {
        e.preventDefault();
        
        fetch('/application-form', {
            method: 'POST',
            body: new FormData(form)
        })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                // Show success message
                showPopup('Success', data.message);
                // Optionally, reset the form or redirect
                // form.reset();
                // or
                // window.location.href = '/';
            } else if (data.status === 'error') {
                if (data.field) {
                    // Highlight the field with error
                    const field = document.getElementById(data.field);
                    field.classList.add('error');
                    field.setCustomValidity(data.message);
                    field.reportValidity();

                    // Remove the error class and message when the user starts typing
                    field.addEventListener('input', function() {
                        this.classList.remove('error');
                        this.setCustomValidity('');
                    }, { once: true });
                }
                // Show error popup
                showPopup('Error', data.message);
            }
        })
        .catch(error => {
            console.error('Error:', error);
            showPopup('Error', 'An unexpected error occurred. Please try again later.');
        });
    });

    function showPopup(title, message) {
        const popup = document.createElement('div');
        popup.className = 'popup';
        popup.innerHTML = `
            <div class="popup-content">
                <h2>${title}</h2>
                <p>${message}</p>
                <button onclick="this.parentElement.parentElement.remove()">Close</button>
            </div>
        `;
        document.body.appendChild(popup);
    }
});



document.addEventListener('DOMContentLoaded', function() {
    const updateForm = document.querySelector('form');  // Adjust this selector if needed
    updateForm.addEventListener('submit', function(e) {
        e.preventDefault();
        
        const sssNumber = this.getAttribute('data-sss-number');  // Assuming you've added this attribute to the form
        
        fetch(`/view-database/${sssNumber}/update`, {
            method: 'POST',
            body: new FormData(this)
        })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                showPopup('Success', data.message);
                // Optionally redirect or refresh the page
                // window.location.href = '/view-database';
            } else if (data.status === 'error') {
                showPopup('Error', `${data.message}<br><br><strong>Details:</strong><br>${data.details}`);
            }
        })
        .catch(error => {
            console.error('Error:', error);
            showPopup('Error', 'An unexpected error occurred. Please try again later.');
        });
    });

    function showPopup(title, message) {
        const popup = document.createElement('div');
        popup.className = 'popup';
        popup.innerHTML = `
            <div class="popup-content">
                <h2>${title}</h2>
                <p>${message}</p>
                <button onclick="this.parentElement.parentElement.remove()">Close</button>
            </div>
        `;
        document.body.appendChild(popup);
    }
});




let educationEntryCount = 1; // Track the number of education entries dynamically

    function addEducation() {
        educationEntryCount++; // Increment the education entry count
        const educationSection = document.getElementById('education-section');
        const newEducationEntry = document.createElement('div');
        newEducationEntry.classList.add('education-entry');
        newEducationEntry.innerHTML = `
            <p class="entry_count_label">Entry ${educationEntryCount}</p>
            <div class="education-input-fields">
                <div class="input-box">
                    <label for="school" class="input-label">School</label>
                    <input type="text" name="school[]" required>
                </div>
                <div class="input-box">
                    <label for="location" class="input-label">Location</label>
                    <input type="text" name="location[]" required>
                </div>
                <div class="input-box">
                    <label for="date-graduated" class="input-label">Date Graduated</label>
                    <input type="date" name="date-graduated[]" required>
                </div>
                <div class="input-box">
                    <label for="attainment" class="input-label">Attainment</label>
                    <input type="text" name="attainment[]" required>
                </div>
            </div>
            <button type="button" class="delete-bt button_version_1" onclick="deleteEducationEntry(this)">Delete Entry</button>
        `;
        educationSection.appendChild(newEducationEntry);
    }

    function deleteEducationEntry(button) {
        const entryToDelete = button.parentElement;
        entryToDelete.remove();

        // Update entry count labels after deletion
        const entryLabels = document.querySelectorAll('.entry_count_label');
        entryLabels.forEach((label, index) => {
            label.textContent = `Entry ${index + 1}`;
        });

        // Reset educationEntryCount to the current number of entries
        educationEntryCount = entryLabels.length;
    }


// WORK EXPERIENCE SECTION
// Add new entries of work experience
let workExperienceEntryCount = 1; // Track the number of work experience entries dynamically

function addWorkExperience() {
    workExperienceEntryCount++; // Increment the work experience entry count
    const workExperienceSection = document.getElementById('work-experience-section');
    const newWorkExperienceEntry = document.createElement('div');
    newWorkExperienceEntry.classList.add('work-experience-entry');

    newWorkExperienceEntry.innerHTML = `
        <p class="entry_count_label">Entry ${workExperienceEntryCount}</p>
        <div class="input-box">
            <label for="company_name" class="input-label">Company Name</label>
            <input type="text" name="company_name[]" required>
        </div>
        <div class="period-div">
            <div class="input-box">
                <label for="period_start" class="input-label">Start Date</label>
                <input type="date" name="period_start[]" required>
            </div>
            <div class="input-box">
                <label for="period_end" class="input-label">End Date</label>
                <input type="date" name="period_end[]" required>
            </div>
        </div>
        <div class="input-box">
            <label for="position" class="input-label">Position</label>
            <input type="text" name="position[]" required>
        </div>
        <div class="input-box">
            <label for="reason_for_leaving" class="input-label">Reason for Leaving</label>
            <textarea name="reason_for_leaving[]" required></textarea>
        </div>
        <button type="button" class="delete-btn button_version_1" onclick="deleteWorkExperienceEntry(this)">Delete Entry</button>
    `;
    workExperienceSection.appendChild(newWorkExperienceEntry);
}

function deleteWorkExperienceEntry(button) {
    const entryToDelete = button.parentElement;
    entryToDelete.remove();

    // Update entry count labels after deletion
    const entryLabels = document.querySelectorAll('.work-experience-entry .entry_count_label');
    entryLabels.forEach((label, index) => {
        label.textContent = `Entry ${index + 1}`;
    });

    // Reset workExperienceEntryCount to the current number of entries
    workExperienceEntryCount = entryLabels.length;
}


// Function to toggle display of supervisor contact info and reason textarea
function toggleSupervisorContactInfo() {
    const checkbox = document.getElementById('contact_present_employer');
    const supervisorContactInfo = document.querySelector('.supervisor-contact-info');
    const reasonTextarea = document.querySelector('.no-contact-reason');

    if (checkbox.checked) {
        supervisorContactInfo.style.display = 'block';
        reasonTextarea.style.display = 'none';
        makeFieldsRequired(true); // Make supervisor fields required
    } else {
        supervisorContactInfo.style.display = 'none';
        reasonTextarea.style.display = 'block';
        makeFieldsRequired(false); // Make reason textarea required
    }
}

// Function to make fields required or not required based on display status
function makeFieldsRequired(required) {
    const supervisorNameInput = document.getElementById('name_of_supervisor');
    const supervisorContactInput = document.getElementById('supervisor_contact');
    const reasonTextarea = document.getElementById('why_not_contact');

    supervisorNameInput.required = required;
    supervisorContactInput.required = required;
    reasonTextarea.required = !required;
}

// Event listener for checkbox change
document.addEventListener('DOMContentLoaded', function() {
    const checkbox = document.getElementById('contact_present_employer');
    checkbox.addEventListener('change', toggleSupervisorContactInfo);
});

// Add event listener to the checkbox to trigger the function when its state changes
document.getElementById('contact_present_employer').addEventListener('change', toggleSupervisorContactInfo);

// Initial call to the function to ensure correct display on page load
toggleSupervisorContactInfo();


// SUBMISSION REVIEW SECTION
// Set the default value of the date input to the current date
// document.addEventListener('DOMContentLoaded', function() {
//     document.getElementById('date_of_application_submission').valueAsDate = new Date();
// });


// // POPUP Confirming Submission
// function confirmSubmission(event) {
//     event.preventDefault(); // Prevent the default form submission
//     alert("Your application was successfully submitted!");
//     window.location.href = "/"; // Replace with your desired URL
// }

// Delete Button Confirm
function confirmDelete() {
    return confirm("Are you sure you want to delete this entry? There is no way to retrieve this data once deleted.");
}

// Add this script to handle form submission and display confirmation
// document.querySelector('form').addEventListener('submit', function(event) {
    // Prevent the default form submission
    // event.preventDefault();

    // Perform any necessary validation or data handling here

    // Display confirmation message
    // alert('Your application has been submitted successfully!');
// });
