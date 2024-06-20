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

checkbox.addEventListener('click', function() {
  if (this.checked) {
    reasonForConvictionDiv.style.display = 'flex';
  } else {
    reasonForConvictionDiv.style.display = 'none';
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
                    <label for="date_graduated" class="input-label">Date Graduated</label>
                    <input type="date" name="date_graduated[]" required>
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
                <label for="start_date" class="input-label">Start Date</label>
                <input type="date" name="start_date[]" required>
            </div>
            <div class="input-box">
                <label for="end_date" class="input-label">End Date</label>
                <input type="date" name="end_date[]" required>
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



// Function to toggle the display of supervisor contact information and reason textarea based on checkbox state
function toggleSupervisorContactInfo() {
    const checkbox = document.getElementById('present_employer_contact_permission');
    const supervisorContactInfo = document.querySelector('.supervisor-contact-info');
    const reasonTextarea = document.querySelector('.no-contact-reason');

    // If the checkbox is checked, show the supervisor contact info and hide the reason textarea; otherwise, hide the supervisor contact info and show the reason textarea
    if (checkbox.checked) {
        supervisorContactInfo.style.display = 'block';
        reasonTextarea.style.display = 'none';
    } else {
        supervisorContactInfo.style.display = 'none';
        reasonTextarea.style.display = 'block';
    }
}

// Add event listener to the checkbox to trigger the function when its state changes
document.getElementById('present_employer_contact_permission').addEventListener('change', toggleSupervisorContactInfo);

// Initial call to the function to ensure correct display on page load
toggleSupervisorContactInfo();


// SUBMISSION REVIEW SECTION
// Set the default value of the date input to the current date
document.getElementById('date_of_application_submission').valueAsDate = new Date();