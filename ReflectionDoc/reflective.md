# Sprint1

## @Surui Liu

### 22.08.2025:
 1. What I did this week：
 - Set up the overall system architecture with a separated frontend and backend. 
 Implemented the PDF extraction feature: extracted structured JSON data from timesheet PDFs, defined the full JSON schema for PDF data, and researched/tested several PDF extraction tools — selected a stable solution.
 - Created a basic Dockerfile for the service.
 2. Plan for next week:
 - Perform front-end ↔ back-end integration and end-to-end testing to ensure Sprint 1 is complete: PDF → extraction → storage → query.
 - Harden the pipeline against edge cases found during integration and prepare integration tests and a deployable Docker image.
 3. Hurdles:
 - PDF extraction initially lacked sufficient granularity; this has been addressed.
 - Considering whether to run benchmarks to demonstrate and quantify the correctness and stability of the PDF extraction — will decide on benchmark metrics and test cases during integration.

### 29.08.2025:
 1. What I did this week
- Implemented and committed the `extract_pdf` feature in the backend: converts timesheet PDFs into the predefined structured JSON (following the agreed JSON schema).  
- Added entries to the **decision log** recording: chosen PDF extraction solution, JSON schema version, field-mapping rules, failure/degredation strategy, and logging/observability decisions.  
- Exposed an HTTP API endpoint for `extract_pdf` to allow the frontend to trigger extraction; integrated the endpoint locally with the existing backend.  
- Ran smoke tests on a representative sample set (≈10 timesheets) to validate extraction correctness and field completeness for common formats.  
- Updated the Dockerfile with the extraction service dependencies and produced a development image candidate (not yet optimized for final deployment or multi-stage builds).  
- Improved error handling and observability: failure reasons are logged, key-field-missing alerts defined, and basic telemetry added (extraction latency, success rate).

 2. Plan for next week
- Complete front-end ↔ back-end integration and validate the end-to-end flow: PDF upload → backend `extract_pdf` → storage → query.  
- Define and run an integration test suite (including edge-case samples) and add tests to CI:  
  - Benchmark metrics to record: field extraction accuracy, field completeness, average processing latency, memory/CPU per PDF.  
  - Initial targets: **field extraction accuracy ≥ 95%** on known-format samples; average processing time ≤ 2s (single-thread baseline).  
- Harden the pipeline for edge cases discovered during integration (e.g., low-res scanned pages, multi-page tables, varied date/unit formats) — consider OCR pre-processing or template fallbacks.  
- Produce an optimized, deployable Docker image: multi-stage build, reduced image size, configurable env vars, and health checks.  
- Expand the decision log with: the benchmark sample set definition, evaluation methodology, and acceptance criteria.

 3. Hurdles / Risks
- Variant PDFs (scans, low resolution, non-standard headers) reduce extraction granularity and accuracy; may require additional OCR cleanup or template-based extraction.  
- Final benchmark sample set and labeling standards are not yet fixed — must define soon to ensure reproducible evaluation.  
- Concurrency and performance strategy is not finalized; if throughput increases we need to decide between batching, queueing, or worker pools.  
- Need to align API details with frontend (error payloads, progress feedback, retry semantics) to avoid repeated API changes during integration.

## @Xingxuan Li
### 22.08.2025
 1. What I did this week
 - Connected the frontend with the backend timesheet check API, now showing ✔/✘ results from backend checks.
 - Added the ability to manually change ✔/✘ for human review.
 - Implemented the feature to automatically generate a signature when all checks pass.
 - Created the frontend page to display the checking results and reviewing table
 2. Plan for next week
 - Prepare one clear mismatch test case to showcase error detection.
 - Improve the UI layout and usability.
 - Merging frontend branch into main.
 3. Hurdles
 - Encountered backend constant mismatch at first but solved it after debugging.

### 29.08.25
 1. What I did this week
 - Tested the review page to ensure normal operation.
 - Verified the connection between backend and frontend after integration.
 - Successfully merged into main and checked that the connection still works after merge.
 2. Plan for next week
 - Get the review table data dynamically from the backend instead of using hard-coded samples.
 - Generate a page that shows each employee’s payroll details
 3. Hurdles
 - Encounters merge conflict when merge branch Cheryl-Validation-Frontend into main at first.
 - The current review table is still a static sample, so it cannot yet fetch real data.


## @EdenTian
### 22.08.2025:
 1. What I did this week
 - Finished this week’s Internal Meeting Minutes and Client Meeting Minutes  
 - Finished the backend logic of timesheet validation with test cases  
 - Revised the issues’ description and organising  
 2. Plan for next week
 - Plan to integrate the logic with the frontend  
 - Discuss with teammates about the timesheet processing from the extracted raw data to Xero-compatible format  
 3. Hurdles
 - I assumed the data my logic is using is the processed data, but it might actually be raw data.  
 - Need more discussion with teammates on handling the gap between raw extracted data and Xero-compatible data in advance.  
 - Did not realise this issue until I was working on it.  

### 29.08.2025:
 1. What I did this week
 - Finished this week’s Internal Meeting Minutes and Client Meeting Minutes  
 - Updated the backend logic based on client feedback and test cases
  
 2. Plan for next week
 - Integrate the validation logic with the frontend  
 - Develop a new frontend page: **Company Details Page**   

 3. Hurdles
 - Waiting for database teammates to provide data for integration


## @Weimiao Sun
### 22.08.2025:
 1. What I did this week
 - Based on the data requirements, I conducted a study on the design of relational databases .
 - Then created a basic database for feasibility verification.
   
 2. Plan for next week
 - Next week, based on specific data requirements, I will further refine the current project's basic database base on what I designed last week.
 
 3. Hurdles
 - There were some minor issues in the implementation of the database technology, but they can be resolved within the limited time frame at present.

### 29.08.2025:
 1. What I did this week
 - Reconfigured the local project deployment environment by setting up a virtual machine to run Bash scripts and configuring the required dependencies.
 - Improved the database creation logic and optimized the project startup script.
 - Refined the database design, balancing performance and functionality requirements.
 - Discussed and finalized the Sprint 2 goals with the team.
  
 2. Plan for next week
 - Deploy the improved database in practice.  
 - Apply adjustments on the database service side to support more complex data access requirements.
 - Further refine the project startup script by integrating environment parameters into an .env file for better simplicity and maintainability.

 3. Hurdles
 - Need to explore strategies for balancing performance and functionality in complex database design.
 - Further learning is required to improve database deployment scripts and SQL statements.
 - Clarifying and implementing the database optimization direction remains a key task.
 - 


 ## @Yudong Qiu  
### 29 August 2025

---

### 1. Work Completed This Week

- **Implemented PostgreSQL Query Functionality:**  
  Developed the core database query module in the software based on the project’s data access requirements.  
  Using Python (`psycopg2`), successfully established connections to the PostgreSQL database and implemented basic `SELECT` queries.

- **Initial Testing and Validation Completed:**  
  Integrated the module into the local development environment and tested it to ensure connection stability, correctness of query results, and proper parameter passing and data type conversion.

- **Prepared for Future Feature Expansion:**  
  The current implementation was designed with extensibility in mind, allowing dynamic SQL construction and parameter binding to support future expansion of query conditions and functionality.

---

### 2. Work Plan for Next Week

- **Refine the Existing Query Module:**  
  Enhance error handling and edge case processing (e.g., empty fields, connection failures, empty query results) to improve robustness and user experience.

- **Expand Coverage to Additional Tables:**  
  Based on evolving business requirements and frontend demands, add new database tables and implement corresponding SQL queries to support more complex data access and visualization needs.

- **Improve Maintainability and Configuration:**  
  Externalize database connection parameters and query fields into `.env` files or YAML/JSON configuration files to simplify environment management and improve maintainability.

---

### 3. Current Challenges and Difficulties

- **Tight Coupling Between SQL and Application Logic:**  
  SQL statements are currently hardcoded in the application. Schema changes may cause maintenance difficulties.  
  Considering abstraction layers or ORM adoption for better modularity.

- **Query Performance Optimization Needs Improvement:**  
  Complex queries with multiple joins and filters are not yet optimized.  
  Plan to use `EXPLAIN` and indexing strategies to improve performance.

- **Transaction Control and Exception Handling Require Enhancement:**  
  Current database interactions lack complete transaction handling.  
  Need to explore `psycopg2` transaction practices to ensure proper rollback and error recovery.

---


