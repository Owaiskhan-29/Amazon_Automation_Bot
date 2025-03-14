# Amazon Automation Bot

This project consists of **two Python scripts** that automate the process of searching for a product on Amazon India and adding it to the cart using Selenium.

## 📌 Project Overview

1. **amazon_bot.py** – Searches for a product and attempts to add it to the cart **without logging in**.
2. **amazon_automation_bot_after_login** – Logs into an Amazon account before searching for a product and adding it to the cart.

These scripts use **Selenium WebDriver** to interact with Amazon's website, mimicking human actions like searching for a product, selecting an item, and adding it to the cart.

---

## 🚀 Features
✅ **Searches for a product** on Amazon.in
✅ **Selects the first available product** from the search results
✅ **Handles multiple product selectors** to find the best match
✅ **Attempts to add the product to the cart** using various strategies
✅ **(For Login Script)** Logs into Amazon before executing the automation
✅ **Bypasses bot detection** using Chrome DevTools Protocol (CDP) modifications

---

## 📂 Files in This Project
| File Name | Description |
|-----------|-------------|
| `amazon_bot.py` | Searches for a product and adds it to the cart **without logging in**. |
| `amazon_automation_bot_after_login` | First logs into an Amazon account, then searches for a product and adds it to the cart. |

---

## 🛠️ Installation & Setup
### **1️⃣ Install Dependencies**
Make sure you have Python installed. Then, install the required packages:
```bash
pip install selenium webdriver-manager
```

### **2️⃣ Install Google Chrome & WebDriver**
Ensure that you have **Google Chrome** installed. Instead of manually downloading `chromedriver.exe`, use WebDriver Manager:

```python
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

driver = webdriver.Chrome(ChromeDriverManager().install())
```

### **3️⃣ Run the Scripts**
- **Run the script without login:**
  ```bash
  python amazon_bot.py
  ```
- **Run the script with login:** (Make sure to update login credentials in the script)
  ```bash
  python amazon_automation_bot_after_login
  ```

---