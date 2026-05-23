Shaheer Mumtaz Baig - bscs23125

# PDC-Sp24: Building Resilient Distributed Systems

This repository contains a FastAPI-based implementation of a **Circuit Breaker** pattern, designed to handle fault tolerance in a distributed system environment. This solution prevents slow external API calls (simulated LLM) from blocking the server's thread pool and causing a cascading failure.

##How to Run the Code

Follow these steps to set up the environment and start the server:

1. **Clone or Download this repository** into a folder named `PDC-Sp24-bscs23125-Baig`.
2. **Navigate into the directory**:

cd PDC-Sp24-bscs23125-Baig



3. **Create a Virtual Environment**:


python -m venv venv


4. **Activate the Virtual Environment**:

.\venv\Scripts\activate



5. **Install Required Dependencies**:

pip install fastapi uvicorn httpx pydantic




6. **Run the FastAPI Server**:

uvicorn main:app --reload




The server will be live at `http://127.0.0.1:8000`.


##How to Test

### 1. Verification of Custom Middleware Header

* Open your browser and go to `http://127.0.0.1:8000/health`.
* Open **Developer Tools** (F12) and go to the **Network** tab.
* Refresh the page, click on the `health` request, and look at the **Response Headers**.
* You must see: `X-Student-ID: bscs23125`.

### 2. Simulating the Fault Tolerance (Circuit Breaker)

* **Step 1: The Initial Failures**
Go to `http://127.0.0.1:8000/generate`. The request will simulate a slow LLM call (5-second delay) and then fail with an error.
* **Step 2: Tripping the Circuit**
Refresh the `/generate` page **3 times**. These requests are slow because the server is still trying to connect to the "broken" service.
* **Step 3: The "Open" State**
On the **4th attempt**, the response will be **instant**. The Circuit Breaker has tripped. It will now return a fallback message without attempting the LLM call, saving the server's threads.
* **Step 4: Proving Fault Tolerance**
While the circuit is "Open," visit `http://127.0.0.1:8000/health`. It will load immediately, proving that the failing LLM service is no longer blocking the rest of the application.

---
