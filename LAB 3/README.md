# Lab 3 — Component Modelling & Architectural Pattern

This folder contains the architecture deliverables for the Pharmacy Expiry & Re-order Dispatch Engine continued from Lab 1.

## Deliverables
- `Component_Diagram.pdf` — UML component diagram (PNG source also included).
- `Component_Diagram.png` — high-resolution diagram image.
- `Architecture_Justification.pdf` — one-page architecture selection and justification.

## Architecture
The system uses a layered architecture with Presentation, Application/Business, and Data layers. The eight components are Pharmacy Staff Dashboard, Supplier Portal, Inventory & Batch Management, FEFO Stock Allocation, Expiry Monitoring & Alerts, Purchase Order Management, Reporting & Performance Monitor, and Pharmacy Database.

The diagram shows labelled component interactions for stock and batch queries, FEFO allocation, eligible-batch lookup, expiry updates, minimum-stock replenishment triggers, dispatched purchase-order access, reporting, and database persistence. Solid arrows indicate service/data-flow interactions; dashed arrows indicate usage dependencies on the database.

## Requirement traceability
The design reflects the Lab 1 workflows: FEFO selection of the earliest-expiring valid batch, near-expiry monitoring (30-day warning), checkout batch rejection and recalculation, minimum-stock purchase-order drafting, supplier access to dispatched orders, inventory status visibility, and operational performance/availability monitoring.
