# Page Replacement Algorithm Simulator

A simple, beginner-friendly web application that simulates three classic
Operating Systems **Page Replacement Algorithms**: **FIFO**, **LRU**, and
**Optimal**. Built as a college mini project using **Python (Flask)** for
the backend and plain **HTML, CSS, and JavaScript** for the frontend
(no frameworks, no database).

---

## Project Overview

Page replacement algorithms decide which memory page to remove when a new
page needs to be loaded and all frames are full. This simulator lets a user
enter a reference string and a number of frames, choose an algorithm, and
watch a step-by-step table showing how pages move in and out of frames,
along with the total number of page hits and faults.

---

## Features

- Three page replacement algorithms: **FIFO**, **LRU**, **Optimal**
- Step-by-step simulation table showing frame contents after every reference
- Page faults highlighted in **red**, page hits highlighted in **green**
- Live statistics: Total Hits, Total Faults, Hit Ratio, Fault Ratio
- Execution time of the algorithm displayed in milliseconds
- Smooth fade-in animation for each row as it appears
- Sample Input button to quickly load a demo reference string
- Reset button to clear the form and results
- Client-side and server-side input validation with clear error messages
- Clean, responsive, mobile-friendly UI (white background, blue theme)
- Algorithm description shown below the dropdown

---

## Technologies Used

- **Backend:** Python 3, Flask
- **Frontend:** HTML5, CSS3, Vanilla JavaScript (Fetch API)
- **No database** — everything is computed on the fly
- **No frontend frameworks** — no React, Bootstrap, or Tailwind

---

## Folder Structure

```
PageReplacementSimulator/
│
├── app.py                 # Flask application (routes)
├── simulator.py            # Core page replacement algorithm logic
├── requirements.txt        # Python dependencies
├── README.md                # Project documentation
│
├── templates/
│   └── index.html          # Main HTML page
│
└── static/
    ├── css/
    │   └── style.css       # Styling for the UI
    │
    └── js/
        └── script.js       # Frontend logic (Fetch API, DOM rendering)
```

---

## Installation Steps

1. Make sure **Python 3.8+** is installed on your system.
2. Download or clone this project folder.
3. Open a terminal inside the `PageReplacementSimulator` folder.
4. (Optional but recommended) Create a virtual environment:
   ```
   python -m venv venv
   ```
   Activate it:
   - Windows: `venv\Scripts\activate`
   - macOS/Linux: `source venv/bin/activate`
5. Install the dependencies:
   ```
   pip install -r requirements.txt
   ```

---

## How to Run

1. From inside the project folder, run:
   ```
   python app.py
   ```
2. You should see output similar to:
   ```
   * Running on http://127.0.0.1:5000
   ```
3. Open your browser and go to:
   ```
   http://127.0.0.1:5000
   ```
4. Enter the number of frames, a reference string, choose an algorithm,
   and click **Start Simulation**.

---

## Sample Input

- **Number of Frames:** `3`
- **Reference String:** `7 0 1 2 0 3 0 4 2 3 0 3 2`
- **Algorithm:** `FIFO`

You can also click the **Sample Input** button on the page to auto-fill
these values.

---

## Sample Output (FIFO, 3 Frames)

| Step | Page | Frame 1 | Frame 2 | Frame 3 | Status |
|------|------|---------|---------|---------|--------|
| 1    | 7    | 7       | -       | -       | Fault  |
| 2    | 0    | 7       | 0       | -       | Fault  |
| 3    | 1    | 7       | 0       | 1       | Fault  |
| 4    | 2    | 2       | 0       | 1       | Fault  |
| 5    | 0    | 2       | 0       | 1       | Hit    |
| 6    | 3    | 2       | 3       | 1       | Fault  |
| 7    | 0    | 2       | 3       | 1       | Hit    |
| 8    | 4    | 2       | 3       | 4       | Fault  |
| ...  | ...  | ...     | ...     | ...     | ...    |

**Overall Statistics:**
- Total Page Faults: `9`
- Total Page Hits: `4`
- Hit Ratio: `30.8%`
- Fault Ratio: `69.2%`

*(Exact hit/fault counts depend on the chosen algorithm.)*

---

## Deploying to Render

1. Push this project folder to a GitHub repository.
2. Go to [render.com](https://render.com) and log in / sign up.
3. Click **New +** → **Web Service**, then connect your GitHub repo.
4. Configure the service:
   - **Environment:** Python 3
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `gunicorn app:app`
   - **Instance Type:** Free (fine for a college project)
5. If Render picks the wrong Python version, add an environment variable:
   - **Key:** `PYTHON_VERSION`
   - **Value:** `3.11.9`
6. Click **Create Web Service**. Render will build and deploy automatically.
7. Once live, your simulator will be available at the `https://your-app-name.onrender.com` URL Render gives you.

The project already includes a `Procfile` (`web: gunicorn app:app`) and `gunicorn` in `requirements.txt`, so no extra setup is needed — just push and connect the repo.

---

## Notes

- This project does not use any database — all computation happens in
  memory for each request.
- Input is validated on both the frontend (JavaScript) and backend (Flask)
  to make sure frames are positive integers and the reference string only
  contains valid numbers.
- The project is intentionally kept simple and well-commented so it is
  easy to understand and present for an Operating Systems mini project.
# PageReplacementSimulator
