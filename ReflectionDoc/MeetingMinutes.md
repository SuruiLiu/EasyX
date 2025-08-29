# Aug 22 Meeting Minutes - Internal Agenda
## Agenda
- Project structure and framework discussion  
- Issue assignments and progress updates  
- Technical stack decisions (**React** for frontend, **Flask** for backend)  
- Database integration concerns  
- Sprint deliverables clarification  

---

## Project Progress Review
- Some team members have completed their previously assigned issues.  
- One member was stuck with signature-related problems.  
- Decision made to skip signature concerns for now.  
- Local database design is progressing.  

---

## Next Week's Plan
- Create the **framework/structure** for the project.  
- Connect functionality with database.  
- Focus on completing current sprint issues rather than adding new ones.  

---

## Technical Challenges Discussion
- Signature handling had three options, but the team decided to **skip for now**.  
- Database connection with backend structure needs clarification.  
- Discussion about **PyTorch vs Flask** for backend.  
- Team agreed **Flask** would be more suitable.  

---

## Product Requirements Update
- **Sprint 1 deliverable** must demonstrate:  
  - Data extraction from PDF  
  - Basic data validation  
- GUI/frontend is confirmed to be part of **Sprint 2**, not Sprint 1.  
- A simple demonstration page may still be needed for Sprint 1.  

---

## Team Collaboration and Communication
- Team discussed **framework creation** and who will handle it.  
- Clarification: team members can work on their issues in **parallel** with framework development.  
- Potential stakeholder might be present in the meeting.  

---

## Risk Management
- Concern raised about adding **frontend** as a new issue when sprint is already planned.  
- Discussion about feasibility of completing all sprint requirements.  
- Decision: focus on **core functionality** before UI development.  

---

## Resource Allocation
- **React** will be used for frontend development.  
- **Flask** will be used for backend development.  
- Team members continuing with their previously assigned issues.  

---

## Continuous Improvement
- Suggestion to build proper project structure/framework.  
- Discussion about technology choices and their suitability for the project.  

---

## Todo for Everyone
- [ ] Database Design (*Larry / Weimiao / Yudong*)  
- [ ] PDF Extraction (*Suu*)  
- [ ] Frontend created with React (*Cherl*)  
- [ ] Frontend Data Validation (*Eden*)  
- [ ] Test case and Sprint 1 test (*Farris*)  



# Aug 22 Meeting Minutes - With Clients
## Topics
- James discussed adding new teams and GitHub access for team members.  
- The team discussed the need to finish Sprint 1 earlier than expected.  
- The team evaluated what could be completed in the shortened timeframe.  
- James presented his frontend design concepts through Figma.  
- The team discussed database structure requirements for storing company, employee, and contract information.  
- The team clarified the data extraction process from PDF timesheets.  
- The team discussed expected data calculation and validation for timesheet processing.  

---

## Review
- James mentioned that the team initially thought they had two weeks to finish their sprint, but were informed they need to complete it by the beginning of next week.  
- A team member noted that last week they were only working on user scenarios and making decisions about programming language and local data, but hadn't started coding yet.  
- James acknowledged the shortened timeframe was due to this being the first sprint, and assured that future sprints would be better planned since preparations would already be in place.  

---

## Progress
- James shared that he had worked on frontend design concepts during the week and was ready to show the team what he had been thinking about.  
- James presented his frontend design through Figma, showing pages for company information, employees, contracts, and timesheet templates.  
- A team member suggested they could work in parallel with one person handling extraction and another working on the database to complete different parts simultaneously.  
- James agreed with the parallel work approach, stating that for Sprint 1 they probably wouldn't get to connecting everything, but could have a database backend ready for future connection.  
- James clarified that the team doesn't need to store the scanned PDFs, just the extracted data and expected data in the database.  
- James explained that the extracted data would eventually need to be sent via API to accounting software.  

---

## Issues
- **Issue**: The team discovered they have less time than expected to complete Sprint 1.  
  - **Solution**: James suggested re-evaluating Sprint 1 goals and moving some tasks to the next sprint.  

- **Issue**: Team members were unsure about what data needs to be stored in the database.  
  - **Solution**: James clarified they need to store expected data and extracted data from timesheets, not the PDFs themselves.  

- **Issue**: A team member was confused about how to calculate expected data for timesheets.  
  - **Solution**: James explained that expected data would be calculated based on contract information such as maximum contract value, hourly rate, and contract duration.  

- **Issue**: Team members were uncertain about the database structure needed.  
  - **Solution**: James clarified they need tables for company details, employees, and contracts, with most information stored in the contract table for flexibility.  

- **Issue**: A team member was confused about the timesheet format and what data needed to be extracted.  
  - **Solution**: James explained they only need to extract the total hours worked per day, not the detailed breakdown of start and end times.  

---

## Decisions
- Re-evaluate Sprint 1 goals due to the shortened timeframe and move some tasks to Sprint 2.  
- Work in parallel with different team members focusing on separate components (extraction, database, frontend) to maximize productivity.  
- Build a database structure that includes tables for company details, employees, and contracts.  
- For Sprint 1, create a simple frontend that allows viewing extracted data from PDFs without full functionality.  
- Focus on extracting data from a **single timesheet format** for Sprint 1, rather than supporting multiple formats.  
- Database design to keep employee and company information minimal, with most details stored in the **contract table** for greater flexibility.  

# Aug 15 Meeting Minutes - Internal Agenda

## Sprint Goal Establishment and Project Name Discussion
- The team discussed potential project names, with **"Easy Take"** being suggested  
- Team established sprint goals focusing on data extraction from PDF and data verification  

## Email Extraction and PDF Processing
- Discussed email extraction methods including **IMAP** and **POP3** protocols  
- Selected programming languages: **Java** for backend, **Python** for PDF extraction  

## User Stories and Issues Creation
- Created GitHub repository and project structure  

## Database Selection for Expected Data
- Discussed database options for storing expected data  

## Task Assignment for Team Members
- Task assignments were defined (see Todo section)  

---

## Project Progress Review
- Sprint goals clarified  
- Repository and structure completed  

---

## Next Week's Plan
- Complete creating issues before **Friday next week**  
- Prepare for tutor examination of sprint goals  
- Meet with client (**James**) to discuss data validation rules  
- Submit individual reports to the tutor about weekly progress  

---

## Technical Challenge Discussion
- Email extraction methods: **IMAP vs POP3 protocols**  
- Potential issues with email extraction from different providers  
- PDF data extraction and validation approaches  
- Database selection for storing expected data  
- Programming language selection for different components  
- Docker container setup for the application  

---

## Team Collaboration and Communication
- Created GitHub repository and invited all team members  
- Set up project board with **Sprint 1 tasks**  
- Established process for creating and assigning issues  

---

## Todo

### Issue Assignments
- **Local Database** → *Weimiao Sun*  
- **Extract PDF data to JSON file** → *Larry Wang*  
- **Map to Xero API** → *Eden Tian / Larry Wang*  
- **Validate against expected data** → *Yudong Qiu*  
- **Test Case / Generate data sets** → *Farris*  
- **Create Dockerfile** → *Suu*  
- **User Story of their PBI** → *Everyone*  

### General Tasks
- Research technical solutions for assigned issues (*Everyone*)  
- Prepare individual reports for the tutor (*Everyone*)  
- Review meeting minutes / Decision Backlog → *Eden Tian*  
- Integrate User Story and write Scenario → *Cherl*  

# Aug 15 Meeting Minutes - Kickoff Meeting with Clients

## Project Overview
- The project aims to **automate extracting data from employee timesheets (PDFs)** and importing it into **Xero accounting software**.  
- Currently, the sponsor manually checks PDF timesheets from employees and enters data into Xero — a time-consuming process.  
- The automation will:
  - Extract key information (hours worked, PO numbers, signatures).  
  - Verify extracted data.  
  - Create timesheets in Xero via API.  
- **Initial phase**: focus on data extraction, verification capability, and API integration with Xero.  
- **Future phases**: email automation, consistency checking, and invoice generation.  
- The sponsor mentioned **commercialisation opportunities**, as many government contractors face similar challenges.  

---

## Timeline and Milestones
- First phase to be completed **by end of semester**.  
- Three main tasks in Phase 1:
  1. Extract information from emails.  
  2. Verify information using AI.  
  3. Import data via Xero API.  
- Work in **three-week sprints**, with kickoff meetings and end-sprint demos.  
- Sponsor to **attend weekly meetings** for updates and guidance.  

---

## Risk Assessment
- **Privacy concerns**: employee data must remain local (no overseas processing).  
- **Processing power risk**:
  - Question if Raspberry Pi is sufficient.  
  - Sponsor confirmed long processing time is acceptable if reliable.  
- **Incorrect data extraction**:
  - Need verification against expected values, especially for PO numbers.  
  - Protection against fraud or errors in submitted timesheets.  

---

## Tools and Resources
- **Xero API** for importing timesheet data.  
- **Docker** discussed for containerisation.  
- **PDF/OCR libraries** (e.g., Markup PDF) considered for extraction.  
- Sponsor to provide **Excel template** used to generate PDF timesheets.  
- Team will generate **sample test data** with the template.  
- **Xero demo account** for development and testing; sponsor will provide discount code for actual account.  
- **Local GPU processing** to maintain data privacy.  
- **Raspberry Pi** discussed as potential processing hardware.  

---

## Success Criteria
- System must **extract data from PDFs** and **import into Xero without manual intervention**.  
- Must **verify signatures** are present on timesheets.  
- Must extract:  
  - PO number  
  - Employee name  
  - Dates  
  - Hours worked  
- System should allow **human verification**, with side-by-side PDF and extracted data view.  
- Long-term goal: system is trusted enough to operate **without manual verification**.  
- Must be **scalable**: from 3 employees currently to potentially 100.  
- **Data privacy** must be ensured with local processing.  

---

## Next Steps
- Develop a **prototype** showing frontend page and backend functionality.  
- **Divide tasks** based on member skills.  
- Sponsor to provide **Excel template**.  
- Generate **sample test data** using the template.  
- Focus on implementing three main components:
  1. Email extraction.  
  2. AI-based information verification.  
  3. Xero API integration.  
- Research **Xero API documentation** to map PDF data to API fields.  
- Team to work **in parallel** on different components.  
- Provide **weekly updates** to sponsor (kept brief).  
