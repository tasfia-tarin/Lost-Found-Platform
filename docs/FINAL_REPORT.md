# Independent University, Bangladesh

## CSE309: Web Application & Internet

# Final Project Submission Report

**Project Title:** Lost & Found Platform

**Submitted By:**
- Name: Tasfia Tarin Shammi
- Student ID: 2311939
- Section: 06
- Team Number: None

**Project Links:**
- Live Application: https://2311939-s6.vercel.app/
- GitHub Repository: https://github.com/tasfia-tarin/Lost-Found-Platform
- API Documentation: https://2311939-s6.vercel.app/api/docs

**Submitted To:** Sayef Reyadh

**Semester:** Autumn 2026

**Submission Date:** November 28, 2026

---

# Table of Contents

1. Executive Summary
2. Part A: Product Requirements Document (PRD)
3. Part B: Software Requirements Specification (SRS)
4. Part C: Technical Design Document (TDD)
5. Part D: Screenshots of the Deployed Application
6. Part E: Project Management and Conclusion
7. Appendix

---

# 1. Executive Summary

## 1.1 Project Overview

Lost & Found Platform is a web-based application designed to help users report, manage, and find lost or found belongings. The main purpose of this platform is to provide a centralized place where users can publish information about lost or found items and access relevant information through a simple web interface.

The application provides a frontend built with React, TypeScript, and Vite. The backend is developed using Python and FastAPI, while Supabase PostgreSQL is used for database management. The application is deployed using Vercel.

Users can create item records, view available records, and manage item information through the application interface. The system also includes authentication-related functionality, role-based access control, group management, and administrative features.

## 1.2 What Has Been Built Since the Mid-Assessment

After the mid-assessment, the project structure and functionality were further developed.

The major development areas include:

- Reorganization of the frontend and backend folder structures.
- Separation of frontend components, services, and types.
- Development of authentication-related backend modules.
- Implementation of role-based access control mechanisms.
- Development of group management functionality.
- Introduction of administrative routes and dashboard components.
- Development of audit and security logging modules.
- Improvement of API organization and deployment configuration.
- Integration of the frontend and backend through REST APIs.

These improvements make the project more organized, maintainable, and suitable for future development.

## 1.3 Live Project Links

| Component | Link |
|---|---|
| Live Frontend | https://2311939-s6.vercel.app/ |
| GitHub Repository | https://github.com/tasfia-tarin/Lost-Found-Platform |
| API Base URL | https://2311939-s6.vercel.app/api |
| API Documentation | https://2311939-s6.vercel.app/api/docs |
| Health Endpoint | https://2311939-s6.vercel.app/api/health |

---

# 2. Part A: Product Requirements Document (PRD)

## A1. Problem Statement

Losing personal belongings is a common problem in educational institutions and public places. People often do not know where to report lost items or how to find information about belongings that have been found by others.

Traditional lost-and-found processes usually depend on physical notice boards, social media posts, or informal communication. These approaches can make information difficult to organize, search, and manage.

The Lost & Found Platform aims to solve this problem by providing a centralized web application where users can report lost or found items and manage relevant information.

The platform is designed to make the process more organized, accessible, and efficient.

## A2. Target Users and Roles

| User Role | Description |
|---|---|
| Visitor | Can access the public application and view available information. |
| Registered User | Can use authenticated application features and manage their own records. |
| Group Member | Can access group-related resources according to assigned permissions. |
| Group Owner | Can manage a group and its members. |
| Administrator | Can access administrative functionality and manage platform users. |

## A3. Project Goals

The major goals of the project are:

1. Provide a centralized platform for reporting lost and found belongings.
2. Allow users to create, view, update, and delete item records.
3. Provide an organized and user-friendly interface.
4. Protect restricted application functionality through authentication.
5. Apply role-based and permission-based access control.
6. Maintain administrative and security-related activity records.

### Security Goals

- Prevent unauthorized users from accessing protected resources.
- Restrict administrative operations to authorized administrators.
- Validate user input before processing requests.
- Apply ownership and permission checks to protected group operations.

## A4. Project Scope

### In Scope

- User interface for the Lost & Found Platform.
- Item creation and management.
- REST API integration.
- Database connectivity.
- Authentication-related functionality.
- Role-based access control.
- Group management.
- Administrative backend functionality.
- Deployment through Vercel.

### Out of Scope

The following features are not considered part of the current project scope:

- Artificial intelligence-based item recognition.
- Automatic image recognition.
- Machine learning-based matching.
- Real-time location tracking.
- Native Android or iOS applications.

### Assumptions

- Users have access to an internet connection.
- Users provide valid information when submitting item records.
- The database and deployment services remain available.
- Authorized administrators manage administrative activities.

## A5. User Stories

| ID | User Story |
|---|---|
| US-01 | As a visitor, I want to open the application so that I can access the platform. |
| US-02 | As a user, I want to register an account so that I can use authenticated features. |
| US-03 | As a registered user, I want to log in so that I can access my account. |
| US-04 | As a user, I want to create a lost item record so that others can see the information. |
| US-05 | As a user, I want to create a found item record so that the owner may identify the item. |
| US-06 | As a user, I want to view item records so that I can find relevant information. |
| US-07 | As a user, I want to update my item information so that the record remains accurate. |
| US-08 | As a user, I want to delete an item record when it is no longer needed. |
| US-09 | As a group owner, I want to manage group members. |
| US-10 | As an administrator, I want to view platform users so that I can manage user activities. |
| US-11 | As an administrator, I want to review administrative logs. |
| US-12 | As an administrator, I want to restrict problematic accounts when necessary. |

---

# 3. Part B: Software Requirements Specification (SRS)

## B1. Introduction

### B1.1 Purpose

This Software Requirements Specification (SRS) describes the functional and non-functional requirements of the Lost & Found Platform. It defines the expected behavior, system requirements, user roles, access permissions, and acceptance criteria.

### B1.2 System Overview

The Lost & Found Platform is a web application that allows users to report and manage lost or found items. It uses a React and TypeScript frontend, a FastAPI backend, and a Supabase PostgreSQL database.

The frontend communicates with the backend through REST API endpoints. The backend processes requests, applies validation and access-control logic, and interacts with the database.

### B1.3 Definitions

| Term | Meaning |
|---|---|
| API | Application Programming Interface |
| REST | Representational State Transfer |
| JWT | JSON Web Token |
| RBAC | Role-Based Access Control |
| CRUD | Create, Read, Update, Delete |
| HTTP | Hypertext Transfer Protocol |
| SQL | Structured Query Language |
| UI | User Interface |
| DB | Database |

### B1.4 References

- CSE309 course project requirements.
- FastAPI documentation.
- React documentation.
- TypeScript documentation.
- Supabase documentation.
- Vercel documentation.

## B2. Functional Requirements

### B2.1 Authentication Requirements

| ID | Requirement |
|---|---|
| FR-AUTH-01 | The system shall provide user registration functionality. |
| FR-AUTH-02 | The system shall provide user login functionality. |
| FR-AUTH-03 | The system shall validate authentication credentials. |
| FR-AUTH-04 | Protected endpoints shall require appropriate authentication. |
| FR-AUTH-05 | The system shall provide logout functionality if session management is enabled. |

### B2.2 Role-Based Access Control Requirements

| ID | Requirement |
|---|---|
| FR-RBAC-01 | The system shall distinguish between regular users and administrators. |
| FR-RBAC-02 | Administrative endpoints shall require administrator authorization. |
| FR-RBAC-03 | Group owners shall be able to manage group resources. |
| FR-RBAC-04 | Group members shall access resources according to assigned permissions. |
| FR-RBAC-05 | Unauthorized requests shall be rejected. |

### B2.3 Administrative Requirements

| ID | Requirement |
|---|---|
| FR-ADM-01 | Administrators shall be able to retrieve user information. |
| FR-ADM-02 | Administrators shall be able to view platform statistics. |
| FR-ADM-03 | Administrators shall be able to ban and unban users. |
| FR-ADM-04 | Administrators shall be able to change user roles. |
| FR-ADM-05 | Administrators shall be able to revoke user sessions. |
| FR-ADM-06 | Administrators shall be able to retrieve audit logs. |
| FR-ADM-07 | Administrators shall be able to retrieve security logs. |

### B2.4 Domain Requirements

| ID | Requirement |
|---|---|
| FR-DOMAIN-01 | Users shall be able to create item records. |
| FR-DOMAIN-02 | Users shall be able to retrieve item records. |
| FR-DOMAIN-03 | Users shall be able to update item records. |
| FR-DOMAIN-04 | Users shall be able to delete item records. |
| FR-DOMAIN-05 | Authenticated users shall be able to create and manage groups. |
| FR-DOMAIN-06 | Group owners shall be able to manage group membership. |
| FR-DOMAIN-07 | Group members shall have permission-controlled access to group items. |

## B3. Non-Functional Requirements

| ID | Requirement | Expected Quality |
|---|---|---|
| NFR-01 | Performance | Normal API requests should respond within an acceptable time under ordinary load. |
| NFR-02 | Security | Protected resources must reject unauthorized requests. |
| NFR-03 | Usability | The application should provide a simple and understandable interface. |
| NFR-04 | Maintainability | Frontend and backend responsibilities should be separated into modules. |
| NFR-05 | Reliability | Database errors should be handled without exposing sensitive information. |
| NFR-06 | Availability | The deployed application should be accessible through its production URL when hosting services are operational. |
| NFR-07 | Compatibility | The application should support modern web browsers. |
| NFR-08 | Data Integrity | Required fields and input data should be validated before database operations. |

## B4. Permission Matrix

### B4.1 General Application Permissions

| Action | Visitor | User | Group Owner | Admin |
|---|---|---|---|---|
| Open application | Yes | Yes | Yes | Yes |
| Register | Yes | Yes | Yes | Yes |
| Access protected features | No | Yes | Yes | Yes |
| Manage own records | No | Verify | Verify | Based on implementation |
| Access admin endpoints | No | No | No | Yes |

### B4.2 Group Permissions

| Action | Owner | Member with Permission | Member without Permission |
|---|---|---|---|
| View group items | Yes | According to permission | No |
| Create group items | Yes | If enabled | No |
| Update group items | Yes | If enabled | No |
| Delete group items | Yes | If enabled | No |
| Manage members | Yes | No | No |
| Change member permissions | Yes | No | No |

### B4.3 Administrative Permissions

| Action | Regular User | Administrator |
|---|---|---|
| View administrative statistics | No | Yes |
| Search platform users | No | Yes |
| Ban users | No | Yes |
| Unban users | No | Yes |
| Change user roles | No | Yes |
| Revoke user sessions | No | Yes |
| View audit logs | No | Yes |
| View security logs | No | Yes |

## B5. Use Cases

### UC-01: User Registration

**Actor:** Visitor

**Precondition:** The visitor can access the application.

**Main Flow:**
1. The visitor opens the registration page.
2. The visitor enters the required information.
3. The system validates the submitted information.
4. The system processes the registration request.
5. The user receives a response.

**Postcondition:** A user account is created if registration succeeds.

### UC-02: User Login

**Actor:** Registered User

**Precondition:** The user has an account.

**Main Flow:**
1. The user opens the login page.
2. The user enters login credentials.
3. The system validates the credentials.
4. The system processes authentication.
5. The user receives access if authentication succeeds.

### UC-03: Create Item Record

**Actor:** User

**Precondition:** The user has access to the item creation functionality.

**Main Flow:**
1. The user opens the item form.
2. The user enters the item title and other details.
3. The user selects Lost or Found status.
4. The user submits the form.
5. The backend validates and stores the record.
6. The application displays the result.

### UC-04: Update Item Record

**Actor:** Authorized User

**Precondition:** The item exists and the user is authorized to update it.

**Main Flow:**
1. The user selects an item.
2. The user chooses the edit option.
3. The user modifies the information.
4. The system validates the updated information.
5. The backend processes the update.
6. The application displays the updated record.

### UC-05: Manage Group

**Actor:** Group Owner

**Precondition:** The user is authenticated and has group ownership privileges.

**Main Flow:**
1. The owner opens group management.
2. The owner creates or selects a group.
3. The owner performs an available group management action.
4. The backend validates the request.
5. The application displays the result.

### UC-06: Administrative User Management

**Actor:** Administrator

**Precondition:** The administrator is authenticated and authorized.

**Main Flow:**
1. The administrator opens the admin functionality.
2. The administrator retrieves user information.
3. The administrator selects a user.
4. The administrator performs an authorized management action.
5. The backend processes the request and records relevant audit information where implemented.

## B6. Acceptance Criteria

### AC-01: Registration

- Given a visitor is on the registration page,
- When valid registration information is submitted,
- Then the system should process the registration request successfully.

### AC-02: Login

- Given a registered user,
- When valid credentials are submitted,
- Then the system should authenticate the user.

### AC-03: Invalid Authentication

- Given a user submits invalid credentials,
- When the login request is processed,
- Then the system should reject the request.

### AC-04: Item Creation

- Given an authorized user,
- When valid item information is submitted,
- Then a new item record should be created.

### AC-05: Item Update

- Given an existing item record,
- When an authorized update request is submitted,
- Then the record should be updated.

### AC-06: Unauthorized Administrative Access

- Given a regular user,
- When the user attempts to access an administrator-only endpoint,
- Then the system should reject the request.

### AC-07: Group Permission

- Given a group member without the required permission,
- When the member attempts a restricted group operation,
- Then the backend should deny the operation.

## B7. Requirements Traceability Matrix

| Requirement | Related Component | Verification Method |
|---|---|---|
| FR-AUTH-01 | Authentication routes and signup interface | Registration test |
| FR-AUTH-02 | Authentication routes and login interface | Login test |
| FR-AUTH-04 | Authentication dependencies | Protected endpoint test |
| FR-RBAC-01 | RBAC module | Role validation test |
| FR-RBAC-02 | Admin routes | Admin authorization test |
| FR-RBAC-03 | Group routes | Group ownership test |
| FR-RBAC-04 | Group permission module | Permission test |
| FR-ADM-01 | GET /api/admin/users | API test |
| FR-ADM-02 | GET /api/admin/stats | API test |
| FR-ADM-03 | User ban/unban endpoints | API test |
| FR-ADM-04 | User role endpoint | API test |
| FR-ADM-06 | GET /api/admin/audit-logs | API test |
| FR-ADM-07 | GET /api/admin/security-logs | API test |
| FR-DOMAIN-01 | POST /api/items | Item creation test |
| FR-DOMAIN-02 | GET /api/items | Item retrieval test |
| FR-DOMAIN-03 | Item update endpoint | Item update test |
| FR-DOMAIN-04 | Item deletion endpoint | Item deletion test |
| FR-DOMAIN-05 | Group routes | Group creation test |

**Note:** The final verification column should be updated with actual automated test results and screenshot references before submission.

---

# 4. Part C: Technical Design Document (TDD)

## C1. Technology Stack

The Lost & Found Platform uses a modern web development stack consisting of frontend, backend, database, and deployment technologies.

| Technology | Purpose | Reason for Selection |
|---|---|---|
| React | Frontend development | Component-based user interface development |
| TypeScript | Frontend programming language | Static typing and improved maintainability |
| Vite | Frontend build tool | Fast development server and build process |
| Python | Backend programming language | Readable syntax and backend development support |
| FastAPI | Backend framework | REST API development and automatic API documentation |
| Supabase PostgreSQL | Database | Relational data storage and SQL support |
| Vercel | Deployment platform | Hosting and deployment of the web application |
| Git | Version control | Tracking source-code changes |
| GitHub | Source-code hosting | Collaboration and project management |

### C1.1 Frontend

The frontend is developed using React and TypeScript. React components are used to organize the user interface into reusable sections.

Vite is used as the frontend development and build tool.

The main frontend responsibilities include:
- Displaying the application interface.
- Collecting user input.
- Displaying item records.
- Communicating with backend API endpoints.
- Displaying authentication and group management interfaces.
- Presenting administrative functionality through dashboard components.

### C1.2 Backend

The backend is developed using Python and FastAPI.

FastAPI handles incoming HTTP requests, validates request data, communicates with the database, and returns JSON responses.

The backend is organized into separate modules for authentication, authorization, CRUD operations, administration, and application routes.

### C1.3 Database

Supabase PostgreSQL is used as the relational database.

The database stores application information, including item records and other application data required by the backend.

The backend connects to the database through the `DATABASE_URL` environment variable.

### C1.4 Deployment

The application is deployed through Vercel.

The frontend and backend are integrated through deployment routing configuration. API requests beginning with `/api/` are routed to the FastAPI backend.

---

## C2. System Architecture

The application follows a client-server architecture.

The frontend communicates with the backend through HTTP requests. The backend processes the requests and communicates with the PostgreSQL database.

### C2.1 Architecture Diagram

```text
             USER
               |
               v
       React + TypeScript
          Frontend
               |
               | HTTP / REST API
               v
          FastAPI
          Backend
               |
       +-------+--------+
       |       |        |
       v       v        v
    Auth &   CRUD     Admin
    RBAC    Modules   Routes
       |       |        |
       +-------+--------+
               |
               v
        Supabase
        PostgreSQL
```

### C2.2 Architecture Explanation

**Frontend Layer:**

The frontend is responsible for user interaction and displaying application data. React components are used to separate different interface features.

**Backend Layer:**

The FastAPI backend receives requests from the frontend. It validates incoming data, processes application logic, checks authorization where required, and communicates with the database.

**Authentication and Authorization Layer:**

Authentication-related modules handle identity verification and token-related operations. The RBAC module supports role and permission checks.

**Database Layer:**

Supabase PostgreSQL stores application records. The backend performs database operations through its CRUD modules.

**Deployment Layer:**

Vercel hosts the deployed application and handles frontend and API routing.

---

## C3. Project Folder Structure

The project is organized into separate frontend and backend directories.

### C3.1 Backend Structure

```text
backend/
│
├── main.py
├── requirements.txt
├── schemas.py
│
├── admin/
│   └── routes.py
│
├── auth/
│   ├── config.py
│   ├── dependencies.py
│   ├── passwords.py
│   ├── rbac.py
│   ├── routes.py
│   ├── schemas.py
│   └── tokens.py
│
├── crud/
│   ├── audit_crud.py
│   ├── group_crud.py
│   ├── item_crud.py
│   ├── security_crud.py
│   ├── session_crud.py
│   └── user_crud.py
│
├── models/
│   └── user.py
│
├── routers/
│   ├── groups.py
│   └── items.py
│
├── services/
│   └── item_service.py
│
└── tests/
    └── test_rbac.py
```

### C3.2 Frontend Structure

```text
frontend/
│
├── src/
│   ├── App.tsx
│   ├── index.css
│   ├── main.tsx
│   │
│   ├── components/
│   │   ├── GroupManagement.tsx
│   │   ├── ItemCard.tsx
│   │   ├── ItemDetails.tsx
│   │   ├── ItemForm.tsx
│   │   ├── ItemList.tsx
│   │   │
│   │   ├── admin/
│   │   │   └── AdminDashboard.tsx
│   │   │
│   │   └── auth/
│   │       ├── Login.tsx
│   │       └── Signup.tsx
│   │
│   ├── services/
│   │   └── api.ts
│   │
│   └── types/
│       └── item.ts
│
└── vite.config.ts
```

### C3.3 Benefits of the Folder Structure

The modular folder structure provides several advantages:

- Improves code readability.
- Separates frontend and backend responsibilities.
- Makes individual components easier to maintain.
- Keeps authentication and authorization logic organized.
- Makes future development easier.
- Improves project presentation and collaboration.

---

## C4. Database Design

The project uses Supabase PostgreSQL as its database system.

### C4.1 Item Table

The `public.items` table stores lost and found item information.

| Column | Data Type | Description |
|---|---|---|
| id | Database-defined type | Unique item identifier |
| title | Database-defined type | Item title |
| description | Database-defined type | Item description |
| category | Database-defined type | Item category |
| status | Database-defined type | Lost or Found status |
| location | Database-defined type | Item location |
| contact_info | Database-defined type | Contact information |
| created_at | Database-defined type | Record creation timestamp |

**Note:** Exact PostgreSQL data types, primary-key definitions, foreign keys, indexes, and constraints must be verified from the actual Supabase database schema before submission.

### C4.2 Database Operations

The backend uses CRUD operations to manage application records.

| Operation | Description |
|---|---|
| Create | Insert a new item record |
| Read | Retrieve item information |
| Update | Modify an existing item |
| Delete | Remove an item record |

### C4.3 Database Connection

The backend uses the `DATABASE_URL` environment variable to connect to the Supabase PostgreSQL database.

Sensitive database credentials are stored in deployment environment variables rather than being included directly in source code.

---

## C5. API Design

The application uses REST API endpoints to connect the frontend with the backend.

The API communicates using HTTP methods and JSON request/response data.

### C5.1 General API Endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/api/health` | Health check |
| GET | `/api/hello` | Basic API response |
| GET | `/api/db-test` | Database connectivity test |
| GET | `/api/items` | Retrieve item records |
| POST | `/api/items` | Create an item record |
| GET | `/api/docs` | Interactive API documentation |
| GET | `/api/openapi.json` | OpenAPI specification |

### C5.2 Group API Endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| POST | `/api/groups/` | Create a group |
| GET | `/api/groups/` | Retrieve groups |
| GET | `/api/groups/{group_id}` | Retrieve a specific group |
| PUT | `/api/groups/{group_id}` | Update a group |
| DELETE | `/api/groups/{group_id}` | Delete a group |
| POST | `/api/groups/{group_id}/members` | Add a group member |
| GET | `/api/groups/{group_id}/members` | Retrieve group members |
| PUT | `/api/groups/{group_id}/members/{member_id}/permissions` | Update member permissions |
| DELETE | `/api/groups/{group_id}/members/{member_id}` | Remove a group member |
| POST | `/api/groups/{group_id}/items` | Add a group item |
| GET | `/api/groups/{group_id}/items` | Retrieve group items |
| PUT | `/api/groups/{group_id}/items/{item_id}` | Update a group item |
| DELETE | `/api/groups/{group_id}/items/{item_id}` | Delete a group item |

### C5.3 Administrative API Endpoints

All administrative routes are protected by administrator authorization.

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/api/admin/users` | Retrieve users with search and pagination |
| GET | `/api/admin/stats` | Retrieve administrative statistics |
| POST | `/api/admin/users/{user_id}/ban` | Ban a user |
| POST | `/api/admin/users/{user_id}/unban` | Unban a user |
| PATCH | `/api/admin/users/{user_id}/role` | Change a user's role |
| POST | `/api/admin/users/{user_id}/revoke-sessions` | Revoke user sessions |
| GET | `/api/admin/audit-logs` | Retrieve audit logs |
| GET | `/api/admin/security-logs` | Retrieve security logs |

### C5.4 API Response and Error Handling

The backend uses HTTP status codes to communicate the result of API requests.

Common HTTP status codes include:

| Status Code | Meaning |
|---|---|
| 200 | Request successful |
| 201 | Resource created successfully, where applicable |
| 400 | Bad request |
| 401 | Authentication required or invalid |
| 403 | Access forbidden |
| 404 | Resource not found |
| 422 | Request validation error |
| 500 | Internal server error |

The actual response status depends on the endpoint implementation and request result.

---

## C6. Authentication and JWT Design

The backend contains separate authentication modules for handling authentication-related operations.

Important modules include:

- `auth/routes.py`
- `auth/dependencies.py`
- `auth/passwords.py`
- `auth/tokens.py`
- `auth/config.py`
- `auth/schemas.py`

### C6.1 Authentication Flow

The general authentication process is:

```text
User
 |
 v
Frontend Login Interface
 |
 v
Authentication API
 |
 v
Credential Validation
 |
 v
Token / Session Processing
 |
 v
Protected API Access
```

### C6.2 JWT Configuration

The project contains a token management module at `auth/tokens.py`.

The authentication configuration is maintained separately in `auth/config.py`.

The following implementation details must be confirmed from the actual source code before final submission:

| Configuration | Value |
|---|---|
| JWT signing algorithm | Verify in source code |
| Access token lifetime | Verify in source code |
| Refresh token lifetime | Verify in source code |
| Token storage mechanism | Verify in frontend and backend |
| Refresh token cookie settings | Verify in source code |
| CSRF protection mechanism | Verify in source code |

The production secret values must never be included in this report or GitHub repository.

### C6.3 Password Security

The backend includes a password-related module named `auth/passwords.py`.

The application also uses a `PASSWORD_PEPPER` environment variable.

The exact password hashing algorithm and configuration should be verified from the implementation.

### C6.4 Authentication Error Handling

Protected API endpoints should reject requests that do not satisfy the required authentication conditions.

Authentication-related errors may include:

- Missing authentication credentials.
- Invalid credentials.
- Expired authentication token.
- Unauthorized access.

The exact refresh-token and cookie behavior must be documented according to the implemented code.

---

## C7. Role-Based Access Control (RBAC)

Role-Based Access Control is used to restrict access to application functionality.

The backend includes an RBAC module:

`auth/rbac.py`

Authentication dependencies are maintained in:

`auth/dependencies.py`

### C7.1 Main Roles

The application distinguishes between regular users and administrators. Group functionality also includes group ownership and member permissions.

| Role | Responsibility |
|---|---|
| User | Uses regular application functionality |
| Group Owner | Manages group-related resources |
| Group Member | Accesses permitted group resources |
| Admin | Performs administrative operations |

### C7.2 Group Permission System

The group permission system uses the following permission flags:

- `can_read_items`
- `can_create_items`
- `can_update_items`
- `can_delete_items`

A group owner receives all permissions when the group is created.

Group members can perform operations according to their assigned permissions.

### C7.3 RBAC Request Flow

```text
Client Request
      |
      v
Authentication Check
      |
      v
Identify User Role
      |
      v
Check Required Permission
      |
   +--+--+
   |     |
Allowed  Denied
   |     |
   v     v
Execute  Return
Action   Forbidden
```

### C7.4 Administrative Authorization

Administrative routes use the `require_admin` dependency.

This ensures that administrative operations are restricted to users who satisfy the administrator authorization requirement.

---

## C8. Administrative Functionality

The backend contains an administrative route module:

`admin/routes.py`

The administrative API provides user management and monitoring-related operations.

### C8.1 Administrative Features

| Feature | Description |
|---|---|
| User Listing | Retrieves registered user information |
| User Search | Supports searching users |
| Pagination | Supports limit and offset parameters |
| Statistics | Retrieves platform statistics |
| User Ban | Allows administrators to ban users |
| User Unban | Allows administrators to restore user access |
| Role Management | Allows administrators to change user roles |
| Session Revocation | Allows administrators to revoke user sessions |
| Audit Logs | Retrieves administrative audit records |
| Security Logs | Retrieves security-related records |

### C8.2 User Management

The user listing endpoint supports pagination through:

- `limit`
- `offset`

The default limit is 20, and the maximum limit is 100.

### C8.3 Audit Logging

The backend contains an audit CRUD module:

`crud/audit_crud.py`

Administrative actions include audit event identifiers such as:

- `USER_BANNED`
- `USER_UNBANNED`
- `USER_ROLE_CHANGED`
- `USER_SESSIONS_REVOKED`

These event names help identify important administrative operations.

### C8.4 Security Monitoring

The backend also contains a security CRUD module:

`crud/security_crud.py`

Security-related information can be retrieved through the administrative security-log endpoint.

The exact fields, filters, and frontend display behavior should be verified before submission.

---

## C9. Security Considerations and Threat Analysis

Security is an important consideration for the Lost & Found Platform.

The application includes authentication, authorization, administrative access restrictions, and security-related backend modules.

| Threat | Possible Impact | Mitigation |
|---|---|---|
| Unauthorized API Access | Access to restricted resources | Authentication dependencies |
| Privilege Escalation | Unauthorized administrative actions | Role-based access control |
| Invalid User Input | Incorrect or unsafe data | Request validation |
| Unauthorized Group Access | Access to restricted group resources | Ownership and permission checks |
| Credential Exposure | Account compromise | Secure handling of credentials and secrets |
| Database Credential Exposure | Unauthorized database access | Environment variables |
| Brute-force Attempts | Repeated login attempts | Verify implemented rate limiting and security controls |
| Session Misuse | Unauthorized session access | Verify session management and revocation behavior |

### C9.1 Environment Variable Security

The application uses environment variables for sensitive configuration.

The known variable names include:

- `DATABASE_URL`
- `JWT_SECRET_KEY`
- `PASSWORD_PEPPER`

Their actual values must never