# Pharmacy Inventory Management — Agile Backlog
**Lab 2**

**Name:** Nayana SM | **SRN:** PES1UG24AM174 | **Campus:** PES University, RR

## 1. Scope and source
This backlog translates the Lab 1 requirements into a set of Epics and user Stories. It covers medicine-batch expiry visibility, FEFO dispensing, stock-triggered purchasing, supplier access to dispatched orders and service availability.

## 2. Requirement-to-story mapping

| Lab 1 reference | Required capability | Priority | Linked Story |
|---|---|---|---|
| FR-001 | Choose the valid batch with the closest expiry at checkout using FEFO. | High | US-02 |
| FR-002 | Record batch expiry dates and flag stock expiring within 30 days. | High | US-01 |
| FR-003 | Produce a clerk-facing dispensing list ordered by earliest valid expiry. | High | US-03 |
| FR-004 | Prepare a draft purchase order when stock falls below its minimum level. | Medium | US-04 |
| FR-005 | Allow suppliers to see purchase orders dispatched to them. | Medium | US-06 |
| NFR-001 | Trigger secure supplier-order generation/dispatch at the safety threshold and assess latency/security under peak load. | High | US-05 |
| NFR-002 | Provide 99.9% availability during pharmacy operating hours, with less than 43 minutes of downtime per month. | High | US-07 |

## 3. Epics

### Epic 1 — Expiry-aware Inventory and Dispensing
This Epic groups the functions needed to monitor expiry dates and ensure stock is issued in the correct FEFO sequence.

### Epic 2 — Replenishment and Supplier Coordination
This Epic covers automatic purchase-order preparation, secure dispatch and supplier visibility of orders.

### Epic 3 — Service Continuity
This Epic addresses the availability target for the stock-management service during pharmacy business hours.

## 4. User stories and acceptance conditions

### US-01 — Identify batches nearing expiry
**As a** pharmacy inventory clerk, **I want** expiry dates to be visible with a warning for batches due to expire within 30 days, **so that** I can identify stock that needs attention.

- Priority: High | Estimate: 3 points | Requirement: FR-002
- Every medicine batch has an expiry date recorded.
- A visible warning is shown when a batch is within 30 days of expiry.
- Staff viewing the relevant batch list can see the warning.

### US-02 — Apply FEFO during checkout
**As a** pharmacy clerk, **I want** checkout to choose the available valid batch with the earliest expiry, **so that** dispensing follows First-Expired-First-Out.

- Priority: High | Estimate: 5 points | Requirement: FR-001 | Dependency: US-01
- The system checks the expiry dates of available, valid batches for the medicine.
- The eligible batch with the earliest expiry is selected first.
- A later-expiring batch is not chosen while an earlier-expiring unexpired batch remains available.

### US-03 — Display a FEFO picking list
**As a** pharmacy clerk, **I want** a dispensing list arranged by expiry date, **so that** I can pick medicines in the intended FEFO order.

- Priority: High | Estimate: 3 points | Requirement: FR-003 | Dependency: US-01
- The system can generate a dispensing list for the clerk.
- The closest valid expiry dates are listed first.
- The list is sorted in ascending expiry-date order.

### US-04 — Prepare a purchase-order draft at the minimum level
**As an** inventory manager, **I want** a draft purchase order to be created when an item's stock drops below its configured minimum, **so that** replenishment can be reviewed before a shortage occurs.

- Priority: Medium | Estimate: 5 points | Requirement: FR-004
- Staff can configure a minimum stock threshold for an item.
- Crossing below that threshold creates a draft purchase order immediately.
- The draft records the item and the stock condition that triggered it.

### US-05 — Dispatch supplier orders securely
**As a** purchasing manager, **I want** a supplier purchase-order request to be generated and dispatched when stock crosses the safety threshold, **so that** replenishment requests are sent consistently and securely.

- Priority: High | Estimate: 8 points | Requirement: NFR-001 | Dependency: US-04
- The system generates and dispatches the supplier request automatically at the safety threshold.
- Performance is assessed using a simulated peak-load test.
- Latency and security results are compared with targets agreed by the team/instructor. Lab 1 does not provide numeric targets, so none are assumed here.

### US-06 — View dispatched orders as a supplier
**As a** supplier, **I want** to see purchase orders dispatched to my account, **so that** I can identify orders that need action.

- Priority: Medium | Estimate: 3 points | Requirement: FR-005 | Dependency: US-05
- The supplier interface lists dispatched purchase orders.
- Orders dispatched by the system are available in that supplier-facing view.
- Dispatched orders are identifiable in the list.

### US-07 — Maintain availability during pharmacy hours
**As a** pharmacy administrator, **I want** the stock-management engine to achieve 99.9% availability during pharmacy operating hours, **so that** stock operations can continue reliably.

- Priority: High | Estimate: 8 points | Requirement: NFR-002
- Availability is monitored or logged during operating hours.
- Evidence is collected to assess the 99.9% uptime objective.
- Monthly downtime remains below 43 minutes.

## 5. Estimate summary and suggested order

| Sequence | Story | Priority | Points |
|---:|---|---|---:|
| 1 | US-01 — Near-expiry identification | High | 3 |
| 2 | US-02 — FEFO checkout | High | 5 |
| 3 | US-03 — FEFO picking list | High | 3 |
| 4 | US-05 — Secure supplier dispatch | High | 8 |
| 5 | US-07 — Operating-hours availability | High | 8 |
| 6 | US-04 — Draft purchase order | Medium | 5 |
| 7 | US-06 — Supplier order view | Medium | 3 |
| | **Total estimate** | | **35** |

These are planning estimates, not measured effort or recorded Planning Poker votes. The team should validate them during backlog refinement.

## 6. Proposed sprint allocation

### Sprint 1 — Expiry and FEFO workflow
- Planned duration: one week; proposed dates 2–9 November 2026, subject to confirmation.
- Goal: record batch expiry dates, flag batches due within 30 days, select the earliest valid batch at checkout and provide an expiry-sorted clerk list.
- Stories: US-01 (3) + US-02 (5) + US-03 (3) = **11 points**.
- Rationale: these High-priority items form a connected workflow. US-01 supplies expiry information needed by US-02 and US-03.

### Sprint 2 — Purchasing and supplier workflow
- Planned duration: one week; dates to be agreed with the team.
- Goal: create a draft order at the minimum threshold, dispatch the supplier request securely and display dispatched orders to suppliers.
- Stories: US-04 (5) + US-05 (8) + US-06 (3) = **16 points**.
- Dependency sequence: US-04 → US-05 → US-06.
- Capacity note: 16 points is a proposed load, not an established team velocity. If it is too large, move US-06 or another Story to a later sprint. US-07 may remain in the backlog.

The Lab 2 activity calls for two sprints. The proposed allocation is a plan; actual completion must be judged from Jira issue states and sprint reports.

## 7. Jira setup and evidence
The recorded Jira board is `Pharmacy Lab 2 - Scrum Board` in the existing `SE-Labwork (SL)` project. It is not a separate pharmacy project. The three Epics and seven Stories have been created, with priorities and Story Point estimates recorded.

For the final evidence set, capture the actual Jira backlog, Story Point fields, Active Sprint views and Burndown Chart reports. Genuine screenshots are still outstanding; do not represent generated illustrations as Jira screenshots.
