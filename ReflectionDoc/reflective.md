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


## @XXX
