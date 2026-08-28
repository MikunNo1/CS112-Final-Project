# Clinic Patient Administration and Communication System
ClinicCare Lite is a Clinic management system that enables physicians to assign tasks to their patients and request submissions. It also enables the patients to see tasks assigned to them and submit the required documents, while ensuring documents submitted meet the file type requirements. It enables Clinicians to review submission, classify them and add notes and patients to see the status of their submissions.

### SETUP INSTRUCTIONS
1. Install required modules, Requirements: refer to requirements.txt
2. From inside the clinic care folder, run python app.py, to run the program
3. Open http://127.0.0.1:5000 in your browser

### DEMO CREDENTIALS
- **Clinician** — ID `30010000`, password `Doctor@2000` (Yam Abu)
- **Patient** — ID `30012026`, password `Test@1234` (Tain Plan)

You may also register new accounts. 
ID rules: clinician IDs are 8 digits ending
in `0000`; patient IDs are 8 digits ending in a year between 2022 and 2028.
Passwords require at least 8 characters with an uppercase letter, a lowercase
letter, a digit, and a special character.

### Limitations and Constraints
-Message class was created and programmed, however it has not been integrated into the user interface. Notifications on pending tasks and assigned tasks are included on the clinician and patient dashboard to fulfill a basic verison of the messaging and notification requirement.
- Clinic class has been created and is ready for future implementation. However for this MVP, to enable the system function properly the clinician ID doubles as the clinic ID and clinic specific functionality has not been integrated into the entire sytem yet.
- This system was designed to be administrative and does not diagnose patients or suggest treatments.
