# Demo & Testing Files
===============================

This folder contains demonstration scripts, testing utilities, and example files that are **NOT required** for production use.

## **Files in This Folder:**

### **Testing & Utilities:**
- **`test_notifications.py`** - Test your notification setup (WhatsApp/Telegram/Email)
- **`cleanup.py`** - Project cleanup utility (for development)
- **`start.sh`** - Quick start script (alternative to `python3 main.py`)

### **Examples & Demos:**
- **`multi_segment_example.py`** - **MAIN DEMO** - Shows multi-segment trading capabilities
- **`readme-documentation-backup.md`** - Backup of old documentation
- **`CLEANUP_COMPLETE.txt`** - Log of cleanup operations

### **Archive:**
- **`old_demo_backup/`** - Empty backup directory (can be deleted)

---

## **How to Use Demo Files:**

### **See Multi-Segment Trading Demo:**
```bash
cd /Users/arawn/Desktop/kitecopytrader/demo
python3 multi_segment_example.py
```
**What it shows:**
- How all 6 trading segments work (NSE/BSE/NFO/MCX/BFO/CDS)
- Sample trade processing across segments
- Risk management for different segments
- Follower configuration examples

### **Test Your Notifications:**
```bash
cd /Users/arawn/Desktop/kitecopytrader/demo
python3 test_notifications.py
```
**What it does:**
- Tests WhatsApp/Telegram/Email notifications
- Sends sample trade alerts
- Verifies your notification setup
- Interactive setup wizard

### **Quick Start Alternative:**
```bash
cd /Users/arawn/Desktop/kitecopytrader/demo
bash start.sh
```
**What it does:**
- Alternative way to start the system
- Includes safety checks and confirmations
- User-friendly startup process

---

## **Important Notes:**

### **For Production Trading:**
- **You DON'T need these files** for actual copy trading
- Main system runs from parent directory: `python3 ../main.py`
- Demo files are purely for learning and testing

### **What's Required for Production:**
```
Parent Directory (kitecopytrader/):
├── main.py              # ← START HERE
├── setup.py             # ← SETUP HERE
├── config.py            
├── master_client.py     
├── follower_client.py   
├── notifications.py     
└── refresh_tokens.py    
```

### **Demo vs Production:**
- **Demo Files** = Learning, testing, examples
- **Production Files** = Actual copy trading system

---

## **Quick Commands:**

### **Run Main Demo:**
```bash
# See how multi-segment trading works
python3 multi_segment_example.py
```

### **Test Notifications:**
```bash
# Test your WhatsApp/Telegram setup
python3 test_notifications.py
```

### **Start Production System:**
```bash
# Go back to main directory and start real system
cd ..
python3 main.py
```

---

## **Can I Delete This Folder?**

**YES!** You can safely delete the entire `demo/` folder if you want a minimal production setup.

The copy trading system will work perfectly without any of these files.

**Keep it if you want to:**
- Learn how the system works
- Test notifications before going live
- See multi-segment trading examples
- Have reference scripts for troubleshooting

---

**Remember: These are just examples and testing tools. The real copy trading magic happens in the parent directory!**
