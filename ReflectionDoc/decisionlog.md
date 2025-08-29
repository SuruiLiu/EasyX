# Decision Log

## @EdenTian98

22.08.2025:
- Established project decision backlogs based on Internal Meeting 1 and Client Meeting 1

### 1. Project Scope and Goals Decisions
**Decision**: Establish first sprint goal: extract data from PDFs and verify data
**Reason**: Client needs automated PDF timesheet processing to reduce manual data entry errors

**Decision**: Focus on three main components: extract information from emails, verify data using AI, import data to Xero via API
**Reason**: Meet client's complete workflow requirements, from data extraction to final accounting system integration

### 2. Technical Approach Decisions
**Decision**: Choose Java for backend development
**Reason**: Team has experience with Java, suitable for enterprise application development

**Decision**: Choose Python for PDF extraction and email processing
**Reason**: Python has rich library support for PDF processing and AI/ML

**Decision**: Use Postgres as database for storing extracted data
**Reason**: Enterprise-grade database with support for complex queries and data integrity

**Decision**: Agree to use IMAP protocol for email extraction
**Reason**: Standard email protocol with good compatibility and security

### 3. Development Process Decisions
**Decision**: Adopt sprint-based approach with three-week cycles
**Reason**: Agile development methodology, facilitates iteration and client feedback

**Decision**: Prioritize backend functionality over frontend development
**Reason**: Core value lies in data processing and verification, frontend can be optimized later

**Decision**: Plan to generate test data using provided Excel template
**Reason**: Ensure test data aligns with actual business scenarios

**Decision**: Commit to local data processing to maintain privacy
**Reason**: Client requires data sovereignty, avoid cloud service dependencies

### 4. Project Milestone Decisions
**Decision**: Aim to complete core functionality by end of current semester
**Reason**: Academic project time constraints, need clear delivery timeline

**Decision**: Plan to provide weekly updates to project sponsor
**Reason**: Maintain transparent communication, get timely feedback

**Decision**: Create user stories and issues on GitHub
**Reason**: Facilitate team collaboration and progress tracking

### 5. Data Verification Strategy Decisions
**Decision**: Implement system to compare extracted data with expected values
**Reason**: Ensure data accuracy, reduce errors

**Decision**: Initially verify all AI extractions manually
**Reason**: Build trust, validate AI model accuracy

**Decision**: Focus on checking critical fields like PO numbers and employee names
**Reason**: These fields are most critical to business, highest cost of errors

## @nandairjayandi

22.08.2025:
- Suggest skipping Firebase usage as James requires data sovereignty, switch to local database system
**Reason**: Client's emphasis on data privacy and control, avoid third-party cloud service dependencies

## @larrywangggg

22.08.2025:
- Suggest using Python for backend development with Flask framework
**Reason**: Maintain consistency with PDF processing tech stack, simplify development and maintenance

## @JamesSKTechLauncher

22.08.2025:
- Confirm preference for more modern backend technology than Java
**Reason**: Modern tech stack provides better development experience and performance
