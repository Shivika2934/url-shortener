# URL Shortener
A simple and lightweight web application to shorten long URLs into compact, shareable links.
<img width="1366" height="415" alt="image" src="https://github.com/user-attachments/assets/006164c7-5f42-4a0c-ac48-9b76ebe9161a" />
<img width="1366" height="336" alt="image" src="https://github.com/user-attachments/assets/96bcf6c0-653a-45da-a623-c218d076825c" />
[URL Shortener on Render](https://url-shortener-1-jaan.onrender.com/)
---

## Features

- Generate short aliases for long URLs  
- Redirect users with HTTP 301 (or 302) status  
- Prevent duplicate shortened links for identical URLs (optional)  
- Track basic analytics (e.g., click count, timestamps) (optional)  
- (Optional) Provide a minimal web UI for submitting URLs  

## Demo

*(If you have a live demo, include here with link and screenshots/GIFs.)*

---

## Tech Stack

- **Python** – Core programming language  
- **Flask** – Web framework for routing & handling HTTP requests  
- **SQLite** (or MySQL, PostgreSQL) – Persistent storage for URLs  
- **Requirements** – Listed in `requirements.txt`  
- **Deployment-ready** – Includes `runtime.txt` for platform compatibility  

---

## Installation

1. **Clone the repository**  
   ```bash
   git clone https://github.com/Shivika2934/url-shortener.git
   cd url-shortener
