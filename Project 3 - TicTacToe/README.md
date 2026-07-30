# Tic Tac Toe - Professional Python Implementation

A feature-rich, text-based Tic Tac Toe game with AI opponents, statistics tracking, and clean architecture.

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Quick Start](#quick-start)
- [Game Modes](#game-modes)
- [AI Difficulty](#ai-difficulty)
- [Project Structure](#project-structure)
- [How to Play](#how-to-play)
- [Testing](#testing)
- [License](#license)

---

## Overview

This is a professional implementation of Tic Tac Toe built with Python. It demonstrates:

- **Clean Architecture**: MVC pattern with separation of concerns
- **AI Implementation**: Minimax algorithm with alpha-beta pruning
- **Modern Python**: Dataclasses, type hints, and enums
- **Professional Code**: Comprehensive testing and documentation

---

## Features

### Core Features
- ✅ Player vs Player (2-player mode)
- ✅ Player vs AI (3 difficulty levels)
- ✅ AI vs AI (watch AI battle itself)
- ✅ Persistent statistics tracking
- ✅ Clean, intuitive console interface

### AI Capabilities
| Difficulty | Strategy | Description |
|-----------|----------|-------------|
| Easy | Random | Makes random valid moves |
| Medium | Heuristic | Detects wins and blocks opponent |
| Hard | Minimax | Unbeatable perfect play |

### Statistics
- Track wins, losses, and draws per player
- Win rate percentages
- Automatic save/load to JSON

---

## Quick Start

### Prerequisites
- Python 3.8 or higher

### Installation

```bash
# Clone the repository
git clone https://github.com/BrunoDS99/Portfolio/tree/main/Project%203%20-%20TicTacToe

# Run the game
python main.py