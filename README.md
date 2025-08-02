# 🏛️ Court Case Metadata Fetcher (District Courts – India)

This is a Flask-based web application that lets users input **Case Type**, **Case Number**, and **Filing Year**, and retrieves metadata about the case from the Indian eCourts portal. It displays:

- Petitioner/Respondent names
- Filing date
- Next hearing date
- Latest available order/judgment PDF (if any)

---

## ✅ Features

- Clean, responsive UI with HTML + CSS
- Backend automation using Selenium (see notes below)
- Each query logged in SQLite database (`queries.db`)
- Parsed result shown in UI
- Handles CAPTCHA via manual or fallback approach

---

## 🏛️ Court Selected

- **State**: Haryana  
- **District**: Faridabad  
- **Court Complex**: District Court, Faridabad  
- **Example Case (Real)**:
  - Case Type: `CHL`
  - Case Number: `2418`
  - Filing Year: `2023`

---

## ⚠️ CAPTCHA & Automation Limitations

The eCourts portal enforces strict **client-side validation and CAPTCHA**, making it **infeasible to fully automate** the scraping process end-to-end.

### Here's what was done:
- A full Selenium-based scraper (`scraper_selenium.py`) was built.
- It successfully navigates to:
  `https://services.ecourts.gov.in/ecourtindia_v6/?p=casestatus/index`
- It auto-fills:
  - State, District, Court
  - Case Type, Number, Year
- BUT: After entering CAPTCHA manually and clicking “Go,” the scraper crashes due to **session tokens**, **dynamic JS**, and **form revalidation**.

### 🛠 Current workaround:
- We provide a **simulated result** using `scraper.py` for the sake of UI demo.
- Full scraper logic is archived in `scraper_selenium.py` for future work.

---

## 🧪 How to Run

```bash
pip install -r requirements.txt
python app.py

Then go to:
http://127.0.0.1:5000


##  Project Structure
.
├── app.py                 # Flask web app
├── scraper.py             # Fallback demo logic
├── scraper_selenium.py    # (Optional) Full scraper attempt
├── db.py                  # Logs queries to SQLite
├── queries.db             # SQLite database
├── templates/
│   └── index.html         # Frontend HTML
├── static/ (optional)
│   └── style.css          # Styles if separated
├── requirements.txt
└── README.md


###  Tech Stack
	•	Python 3
	•	Flask
	•	Selenium (fallback)
	•	SQLite
	•	HTML + CSS
Notes
	•	CAPTCHA automation is intentionally not attempted
	•	All scraping behavior is documented and safely handled
	•	Simulated output is clearly marked
