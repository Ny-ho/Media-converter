# Asynchronous Media Converter API 🚀

A high-performance, distributed backend service built with **FastAPI**, **Celery**, and **Redis** that handles heavy video processing asynchronously.
his project solves the problem of server blocking during long-running tasks by offloading media transcoding to background workers using **FFmpeg** and **FFprobe**.

## 🛠️ Key Architectural Features & What I Learned

* **Asynchronous Task Offloading:** Learned how to prevent HTTP request timeouts by using **Celery** to instantly return a `202 Accepted`
 tracking token while video processing runs safely in the background.
* **Real-Time Progress Tracking:** Implemented a non-blocking system pipeline using Python's `subprocess.Popen` to read live stream bytes from
   **FFmpeg**, parse frame execution via Regular Expressions (`re`), and stream live completion percentages to a **Redis** metadata scoreboard database.
* **Multi-Format Processing:** Designed dynamic API routes supporting conversion parameters (`?target_format=`) to transmute `.mp4` streams into
  `.avi`, `.mkv`, `.mp3` (audio extraction), or animated `.gif` loops.
* **Automated System Cleanup (Celery Beat):** Configured a scheduled cron-style background task ("The Janitor") that automatically audits storage
   directories on an interval and purges expired temporary media files to prevent disk memory saturation.

## 🏗️ Technology Stack
* **Framework:** FastAPI (Python)
* **Task Queue & Scheduler:** Celery + Celery Beat
* **Message Broker & Results Backend:** Redis
* **System Binary:** FFmpeg & FFprobe
* **Environment:** WSL (Windows Subsystem for Linux) & VS Code

## 🚀 How to Run Locally

1. **Clone the repository:**
   ```bash
   git clone <your-repo-url>
   cd media_converter
