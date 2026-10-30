# Doctor Appointment Booking System

## 1. Business Overview

The Doctor Appointment Booking System allows patients to view doctors' available days and time slots, request appointments, and manage their upcoming bookings. Doctors can review appointment requests and accept or decline them.

The system aims to simplify the appointment booking process while considering patient medical data privacy and usability on mobile devices.

## 2. Twist Rule

**Maximum Upcoming Appointments Rule:** Each patient can have at most **N upcoming appointments** at any given time.

- Pending and Accepted future appointments count toward the limit.
- Declined, Cancelled, and past appointments do not count.
- The value of N is documented in the requirements.

**Chosen N: 4**

## 3. Team Members and Responsibilities

| Student ID | Full Name | Assigned Task | Branch | PR Link |
|---|---|---|---|---|
| 20240062 | Ahmed Elrewiny | Application Implementation | `ahmed` | [PR #3]() |
| 20240658 | Yasmin Mohamed Nabil | Class Diagram & Sequence Diagram | `yasmin` | [PR #1](https://github.com/Angham-maher/doctor-appointment-booking-system/pull/1) – Merged |
| 20242058 | Angham Maher Abdelfattah | Use Cases & Use Case Diagram | `main` | N/A – Direct commits |

- Yasmin worked on the `yasmin` branch and opened Pull Request #1, which was merged into `main`.
- Ahmed and Angham worked directly on the `main` branch and did not submit separate Pull Requests.

## 4. Conflict Drill

**Conflict Drill: Not Performed** – The team merged the Pull Request without encountering merge conflicts.

## 5. Requirements

### Functional Requirements

- **R1:** Patients can view doctors' available days and times.
- **R2:** Patients can book appointments during available time slots.
- **R3:** Doctors can accept or decline appointment requests.
- **R4:** Patients can have at most 4 upcoming appointments.

### Non-Functional Requirements

- **R5:** Patient medical data must be accessible only to authorized staff.
- **R6:** Available appointment times must be displayed within 2 seconds.
- **R7:** The application must be usable on mobile phone screens.

### Implementation Status

`main.py` is a console demonstration, not a full clinic application.

| Requirement | Status in `main.py` |
|---|---|
| R1–R4 | Implemented and shown in the demo. |
| R5 | **Not implemented.** The application stores no medical data and has no staff roles or access control. |
| R6 | **Demonstrated only.** The demo takes a single in-memory timing measurement. This is not a formal verification of the 2-second requirement. |
| R7 | **Not implemented.** The application runs in the console and has no mobile user interface. |

When a doctor declines an appointment, the application prints a console message addressed to the patient. This is a simulated notification; nothing is actually delivered to the patient. The application has no operation for cancelling appointments.

## 6. Project Deliverables

The assignment requires the following files:

| File | Description |
|---|---|
| `1_requirements.md` | Functional and non-functional requirements, including the chosen value of N. |
| `2_use_cases.md` | Patient and doctor use cases, including an alternative flow. |
| `3_candidate_classes.md` | Candidate classes analysis. |
| `4_class_diagram.md` | Mermaid class diagram. |
| `5_sequence_diagram.md` | Mermaid sequence diagram. |
| `main.py` | Python implementation of the system. |
| `6_ai_journal.md` | AI usage journal documenting what was checked, AI mistakes, corrections, and the application output. |

## 7. Development Workflow

1. Yasmin created and worked on the `yasmin` branch.
2. Yasmin submitted Pull Request #1.
3. Pull Request #1 was merged into `main`.
4. Ahmed and Angham contributed directly to `main`.
5. The team worked on the implementation based on the project's requirements and diagrams.

**Note:** Not all team members used separate branches or Pull Requests.

## 8. How to Run the Application

The application is written in Python 3 and uses only the Python standard library, so no additional packages need to be installed.

Check your Python installation:

```bash
python --version
```

Run the application:

```bash
python main.py
```

## 9. Repository

**GitHub Repository:** [doctor-appointment-booking-system](https://github.com/Angham-maher/doctor-appointment-booking-system)