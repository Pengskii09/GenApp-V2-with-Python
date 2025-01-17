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

//CONTACT SUPERVISOR 
const checkbox1 = document.getElementById('contact_present_employer');
const nameOfSupervisor = document.getElementById('name_of_supervisor');
const supervisorContact = document.getElementById('supervisor_contact');
const whyNotContact = document.getElementById('why_not_contact');
const nameOfSupervisorDiv = document.querySelector('.supervisor-contact-info');
const noContactReasonDiv = document.querySelector('.no-contact-reason');

checkbox1.addEventListener('change', function() {
    // Toggle the display of the nameOfSupervisorDiv and noContactReasonDiv
    nameOfSupervisorDiv.style.display = this.checked ? 'block' : 'none';
    noContactReasonDiv.style.display = this.checked ? 'none' : 'flex';

    // Enable or disable inputs based on the checkbox state
    whyNotContact.disabled = this.checked;
    nameOfSupervisor.disabled = !this.checked;
    supervisorContact.disabled = !this.checked;

    if (!this.checked) {
        nameOfSupervisor.value = "";
        supervisorContact.value = "";
    } else {
        whyNotContact.value = "";
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



// Delete Button Confirm
function confirmDelete() {
    return confirm("Are you sure you want to delete this entry? There is no way to retrieve this data once deleted.");
}
