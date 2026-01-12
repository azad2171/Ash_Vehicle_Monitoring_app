
# 🚚 Vehicle Delivery & Ash Monitoring MVP

A centralized digital platform to replace manual Excel-based monitoring of ash generation, storage, and dispatch operations at a power plant.

This MVP focuses on **correct operational flow**, **minimal data entry**, and **automatic stock calculation**, while remaining simple enough for real users to adopt immediately.

---

## 🎯 What This MVP Solves

This system automates and replaces:

- Manual Excel monitoring sheets
- Opening / closing stock carry-forward
- Dispatch counting and MT calculations
- Party-wise and mode-wise reconciliation

### Core Principle
>
> **Users only record events.  
The system does all calculations automatically.**

---

## 🧠 Core Concepts

| Concept | Description |
|------|------------|
| **Silo** | Physical ash storage units (e.g. ST-I, ST-II) |
| **Inflow** | Ash generated into a silo during plant operation |
| **Trip** | One dispatch movement (Truck / Bulker / Rake) |
| **Daily Balance** | Auto-calculated daily stock & dispatch summary |

---

## 👥 Intended Users

### Shift Operators

- Record ash inflow (shift-wise / time-based)
- Record dispatch trips

### Supervisors / In-Charge

- Monitor daily stock & dispatch
- Review totals and closing stock
- (Future) Close / lock the day

---

## 🔁 Daily Operational Flow

### 1️⃣ Start of the Day

- **No manual opening stock entry**
- Opening stock is automatically derived from the previous day’s closing stock

✔ No Excel carry-forward  
✔ No manual reconciliation

---

### 2️⃣ Record Ash Generation (Silo Inflow)

**When:**  

- Whenever ash is generated (typically shift-wise)

**User enters:**

- Silo (ST-I / ST-II)
- Quantity (MT)
- Optional remarks

**System does:**

- Adds ash into the selected silo
- Supports multiple inflow entries per day
- Stores exact timestamps

---

### 3️⃣ Record Dispatch (Trips)

**When:**  

- Every truck / bulker / rake dispatch

**User enters:**

- Truck
- Trip type (BAGGING / BULKERS / RAKE)
- Source silo
- Party (destination)
- Ash quantity
- Gate in / out time (optional in MVP)

**System does:**

- Deducts ash from the correct silo
- Links dispatch to party
- Automatically updates totals

Each trip represents **one real physical movement**.

---

### 4️⃣ Monitor the Day (Live)

The **Daily Monitoring page** shows, in real time:

#### A. Silo-wise Stock

| Silo | Opening | Inflow | Dispatch | Closing |
|----|--------|--------|---------|--------|

- Updates automatically
- No manual edits
- Always consistent

#### B. Dispatch Summary (Excel-like)

| Type | Trips (Nos) | Quantity (MT) |
|----|------------|---------------|
| BAGGING | Auto | Auto |
| BULKERS | Auto | Auto |
| RAKE | Auto | Auto |
| TOTAL | Auto | Auto |

This directly replaces the existing monitoring sheet.

---

### 5️⃣ End of Day Review

- Supervisor reviews inflow, dispatch, and closing stock
- (Future) Day can be closed/locked for audit safety

---

## ❌ What Users No Longer Do

- Maintain Excel formulas
- Manually calculate totals
- Carry forward opening stock
- Reconcile party-wise numbers
- Fix Excel errors at end of day

---

## ✅ Why This MVP Is Easy to Use

- Familiar terminology (ST-I, ST-II, BAGGING, RAKE)
- Minimal data entry
- No calculations required
- Forgiving (multiple inflows, flexible timing)
- Real-time visibility

---

## 🧪 How to Demo This MVP Live

Recommended demo flow (5 minutes):

1. Add a **silo inflow**
2. Add a **dispatch trip**
3. Open **Daily Monitoring**
4. Show automatic stock update
5. Show dispatch summary

This immediately demonstrates value and accuracy.

---

## ⚠️ MVP Scope & Limitations

Current MVP does **not** include:

- Role-based authentication
- Approval workflows
- Excel export
- Automatic day locking

These are **planned enhancements**, not redesigns.

---

## 🏗️ System Architecture (High Level)

- **Silo** → Master data
- **Party** → Master data
- **Silo Inflow** → Ash generation events
- **Trip** → Dispatch events
- **Daily Silo Balance** → Auto-calculated daily summary

Stock is never edited directly — it is always **derived from events**.

---

## 🚀 Future Enhancements

- Simple input forms for non-technical users
- Day close & lock
- Party-wise reports
- Excel / CSV export
- Trend charts (silo utilization, dispatch trends)
- QR-based truck entry

---

## 📌 Summary

This MVP is not just a prototype — it is a **correct operational foundation**:

- Accurate
- Auditable
- Scalable
- Familiar to users

It can be safely extended into a full production system without rework.

---

**Built to replace Excel — not imitate it.**
