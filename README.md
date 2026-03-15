# 🛡️ SSH Honeypot

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![Platform](https://img.shields.io/badge/Platform-Linux-green)
![Security](https://img.shields.io/badge/Field-Cybersecurity-red)
![Status](https://img.shields.io/badge/Project-Active-success)
![License](https://img.shields.io/badge/License-MIT-yellow)

> A lightweight **SSH honeypot written in Python** designed to capture and analyze unauthorized login attempts.

This project simulates an SSH server to observe attacker behavior, collect credential attempts, and generate real-time analytics.

---

# 📌 About This Project

The goal of this project is to explore **offensive security techniques from a defensive perspective**.

By creating a honeypot, we intentionally expose a fake SSH service that attackers or automated bots may attempt to compromise. Every interaction is logged and analyzed, allowing us to better understand:

* Common credential brute-force patterns
* Popular usernames and passwords used by attackers
* Automation behavior from brute-force tools
* Geographic origin of attacks
* SSH client fingerprints

This project was built as part of my journey into **ethical hacking, cybersecurity, and threat analysis**.

---

# 🔐 What is SSH?

**SSH (Secure Shell)** is a cryptographic network protocol used to securely access remote systems over an unsecured network.

It is commonly used by:

* System administrators
* DevOps engineers
* Cloud infrastructure teams
* Security professionals

SSH typically runs on **port 22**, but attackers frequently scan the internet looking for exposed SSH services to attempt **brute-force authentication attacks**.

Because of this, SSH is one of the **most targeted services on the internet**.

---

# 🍯 What is a Honeypot?

A **honeypot** is a security mechanism designed to **attract attackers** in order to study their behavior.

Instead of protecting a real system, a honeypot:

* Simulates a vulnerable service
* Logs attacker activity
* Collects intelligence about attack techniques

Security teams use honeypots to understand:

* Attack patterns
* Malware behavior
* Botnet scanning activity
* Credential harvesting attempts

This project implements a **low-interaction SSH honeypot**.

---

# ⚙️ Features

### 🔑 Credential Capture

Logs all authentication attempts including:

* Username
* Password
* Source IP
* Source Port
* SSH Client Version

---

### 🌍 Geolocation Intelligence

Each attacking IP is enriched with:

* Country
* City
* Latitude / Longitude
* ISP
* ASN (Autonomous System Number)

This helps identify **where attacks originate from**.

---

### 📊 Real-Time Analytics

The honeypot tracks:

* Attempts per IP
* Most common usernames
* Most common passwords
* Top attacking IPs
* Total attempts recorded

Example statistics dashboard:

```
┌─────────────────────────────────────┐
│        SSH HONEYPOT STATS           │
├─────────────────────────────────────┤

Top Usernames
1. root        (14)
2. admin       (9)
3. ubuntu      (5)

Top Passwords
1. 123456      (11)
2. password    (7)
3. admin       (6)

Top Attacking IPs
1. 185.23.44.11 (14)
2. 45.77.21.10  (9)

Total Attempts: 30

└─────────────────────────────────────┘
```

---

### 🤖 Automated Attack Detection

The honeypot detects suspicious automation by analyzing:

* Time between login attempts
* Repeated credential patterns

Possible brute-force automation is flagged automatically.

---

### 🧠 Persistent Attack Logging

All attacks are saved in structured JSON logs:

```
logs/attacks.json
```

Example log entry:

```json
{
  "ip": "185.23.44.11",
  "port": 54213,
  "username": "root",
  "password": "admin",
  "ssh_client_version": "SSH-2.0-OpenSSH_8.2"
}
```

This allows future **forensics and data analysis**.

---

# 🖥️ Example Output

```
================ SSH HONEYPOT ALERT ================

[Network Information]
    IP Address        : 185.23.44.11
    Source Port       : 54213
    SSH Client        : SSH-2.0-OpenSSH_8.2

[Geolocation]
    Country           : Russia
    City              : Moscow
    Coordinates       : 55.7558, 37.6173
    ISP               : Rostelecom
    ASN               : AS12389

[Credentials Captured]
    Username          : root
    Password          : admin

[Attack Statistics]
    Attempts from IP  : 5
    Time since last   : 0.42s

⚠ Possible automated brute-force detected

====================================================
```

---

# 🧰 Tech Stack

This project uses:

* **Python**
* **Paramiko** (SSH protocol implementation)
* **Requests** (IP geolocation API)
* **JSON logging**
* **Custom analytics engine**

---

# 📂 Project Structure

```
ssh-honeypot
│
├── core
│   ├── server.py          # TCP listener that wraps incoming connections into a Paramiko SSH transport
│   ├── key_manager.py     # Host key generation and loading
│   ├── analytics.py       # Attack statistics and analytics engine
│   ├── geoip.py           # IP geolocation lookup
│   ├── ssh_server.py      # Implements a fake SSH server using Paramiko.
│   ├── logger.py          # Handles persistent logging of SSH attack attempts in JSON format..
│
├── logs
│   └── attacks.json       # Persistent attack logs
│
├── main.py                # Honeypot entry point
└── README.md
```

Each module has a specific responsibility to keep the honeypot **modular and maintainable**.

---

# 🚀 Running the Honeypot

Clone the repository:

```
git clone https://github.com/INGmoono/HoneypotSSH.git
```

Enter the project directory:

```
cd ssh-honeypot
```

Create and activate a virtual environment:

```
python -m venv venv
source venv/bin/activate
```

Install dependencies:

```
pip install -r requirements.txt
```

Run the honeypot:

```
python main.py
```

The honeypot will start listening on:

```
0.0.0.0:2222
```

if you want a try (In local) in another terminal do:

```
ssh root@localhost -p 2222
```
---

# ⚠️ Security Notice

This project is intended for:

* Educational purposes
* Security research
* Ethical hacking learning

Do **not deploy honeypots irresponsibly** or without understanding the risks of exposing services to the internet.

---

# 🎯 Learning Goals

This project helped me practice and explore:

* Python network programming
* SSH protocol behavior
* Brute-force attack patterns
* Security logging and analytics
* Threat intelligence enrichment
* Honeypot architecture

---

# 👨‍💻 Author

**Julian Camacho**

Cybersecurity student passionate about **ethical hacking and offensive security**.

I enjoy building projects that simulate real-world attack scenarios in order to better understand how systems are compromised and how they can be defended.

My goal is to continue growing in:

* Offensive Security
* Threat Analysis
* Security Research
* Defensive Engineering

---

# 📈 Future Improvements

Planned upgrades for this honeypot:

* Fake interactive SSH shell
* Command logging
* Attacker tool fingerprinting
* Attack world map visualization
* Threat intelligence dashboards

---

# 📜 License

This project is released under the **MIT License**.

You are free to use, modify, and distribute this project for educational and research purposes.

---

⭐ If you found this project interesting, consider giving it a **star on GitHub**.
