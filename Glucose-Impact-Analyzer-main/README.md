# Glucose Impact Analyzer AI

An educational web application that estimates the glucose impact of meals and visualizes a predicted short-term glucose response using an explainable AI model.

This project is designed for learning, experimentation, and personal insight. It is not a medical device and does not provide medical advice.

## ⚠️ Usage Notice

This repository is public for visibility and reference only.

Please **do not use, copy, modify, deploy, or redistribute this project without contacting me first**.

If you are interested in using this project, integrating it into a product, or collaborating, reach out via the link in my bio so I can assist and approve proper usage.

---

## Overview

Glucose Impact Analyzer AI helps users understand how different meals may affect blood glucose levels by analyzing macronutrients and simple contextual factors.

Users input meal information and receive:

- A glucose impact score from 0 to 100  
- An estimated peak glucose rise  
- A 2-hour predicted glucose curve  
- A clear explanation of how the estimate was calculated  

The system is intentionally transparent and modular so the prediction model can be improved over time.

## Features

- Meal macronutrient input (carbs, fiber, protein, fat)
- Glucose impact score calculation
- Predicted glucose curve visualization
- Explainable baseline prediction model
- FastAPI backend
- Next.js frontend
- Docker support for local development

## Tech Stack

### Frontend
- Next.js (App Router)
- React
- Recharts

### Backend
- FastAPI
- Python
- NumPy
- SQLModel (SQLite)

### Infrastructure
- Docker
- Docker Compose

## About

A simple, educational web app that estimates the glucose impact of a meal and predicts a short glucose curve.

## Topics

ai  
health  
analysis  
web  
