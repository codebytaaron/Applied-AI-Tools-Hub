# Simple Password Manager

Password Manager (Python)

A simple command-line password manager built with Python.

This project focuses on core security concepts, clean structure, and safe handling of sensitive data.

## ⚠️ Usage Notice

This repository is public for visibility and reference only.

Please **do not use, copy, modify, deploy, or redistribute this project without contacting me first**.

If you are interested in using this project, adapting it, or collaborating, reach out via the link in my bio so I can assist and approve proper usage.

---

## Overview

This password manager allows users to securely store and retrieve passwords locally.

Passwords are never stored in plain text.  
All entries are hashed before being written to disk.

## What it does

- Stores passwords locally  
- Hashes passwords using SHA-256 before saving  
- Retrieves stored password hashes by service name  
- Uses a simple, readable command-line interface  

## Features

- CLI-based workflow  
- SHA-256 password hashing  
- JSON file storage  
- Add and retrieve credentials  
- Minimal and easy-to-follow code  

## Requirements

- Python 3.x  
- No external libraries required  

## Usage

Run the program:

```bash
python password_manager.py
