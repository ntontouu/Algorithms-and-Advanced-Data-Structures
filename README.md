[![University](https://img.shields.io/badge/University-University%20of%20Ioannina-blue.svg)](https://www.uoi.gr)
[![Course](https://img.shields.io/badge/Course-Algorithms%20%26%20Adv.%20Data%20Structures-orange.svg)](https://ecourse.uoi.gr/)
[![Topic](https://img.shields.io/badge/Topic-Probabilistic%20Data%20Structures-success.svg)]()
[![Language](https://img.shields.io/badge/Language-Python-blueviolet.svg)](https://www.python.org/)

# Bloom Filters and Bloom Filters with Counters
A  Python implementation of a standard Bloom Filter and a Counting Bloom Filter. Developed as Assignment 13 for the Algorithms and Data Structures course to demonstrate space/time trade-offs in hash coding.

## 📚 Table of Contents
- [Overview](#-overview)
- [Theoretical Background](#-theoretical-background)
- [Project Structure & Code Architecture](#-project-structure--code-architecture)
- [Experimental Results & Analysis](#-experimental-results--analysis)
- [Getting Started & Execution](#-getting-started--execution)
- [Author & Credits](#-author--credits)

## 🔍 Overview
This project implements probabilistic data structures designed to test whether an element is a member of a set. It guarantees no false negatives while allowing a highly controllable, extremely small rate of false positives. The project extends the classic architecture by implementing a Counting Bloom Filter, which replaces static bits with counters to support item deletion without corrupting the overall dataset.

## 📐 Theoretical Background

**Double Hashing & MD5 (Hash Functions)**
Instead of generating $k$ independent hash functions computationally, the system utilizes Double Hashing. It computes a single 32-character MD5 hash, splits it into two 16-character integers ($h_1$ and $h_2$), and mathematically generates $k$ hash values using the formula:  
$h_i(x) = (h_1(x) + i \cdot h_2(x)) \pmod m$

**Standard Bloom Filter**
Utilizes a highly memory-efficient array of bits (initialized to 0). During insertion, $k$ array positions are flipped to 1. Queries check if all $k$ positions are 1.

**Counting Bloom Filter**
Replaces the binary array with an array of small integers. Insertions increment the corresponding $k$ indices by 1, while deletions safely decrement them, allowing dynamic set modifications.

## 🛠️ Project Structure & Code Architecture

| File | Description |
| :--- | :--- |
| `ntontouu.py` | Python script containing the `BloomFilter` and `CountingBloomFilter` classes, double hashing logic, and all experimental pipelines. |
| `ΑΚΠΔΔ1_ΝΤΟΝΤΟΥ.pdf` | Detailed report documenting theoretical design, structural choices, and experimental analysis. |
| `README.md` | This file, containing execution instructions and project overview. |
| `README-el.md` | Same as this file but the execution instructions are in Greek :greece:. |
| `Figure_1.png` | Graphs of a run. |

## 📊 Experimental Results & Observations
The structures were rigorously tested against multiple scenarios:

- **Correctness Scenarios:** Successfully validates the insertion of "apple", "banana", and "cherry". The Counting filter correctly drops "apple" upon deletion (returns False) while retaining "banana" (returns True).
- **False Positive Analysis (10,000 insertions, 1,000 queries):**
  - **m = 50,000 (k = 3):** Achieves ~9.2% FP rate.
  - **m = 100,000 (k = 6):** Achieves ~1.2% FP rate.
  - **m = 200,000 (k = 13):** Achieves ~0.0% FP rate.
- **Python `set` Comparison:** While native Python `set` objects perform insertions and lookups marginally faster due to underlying C optimizations, the Bloom Filter achieves massive memory efficiency (~12.5 KB compared to >500 KB for 10,000 strings).

## 🚀 Getting Started & Execution

**Prerequisites:** 
Ensure Python 3.6+ is installed on your environment. To generate the performance visualizations, you must install the required external libraries:
```bash
pip install matplotlib numpy
```
The rest of the code relies entirely on standard Python libraries (hashlib, random, time, sys).

**Execution:**
```bash
python ntontouu.py 
```
## 📝 Author & Academic Use

**Student:** Maria Alexandra Ntontou (ΜΑΡΙΑ ΑΛΕΞΑΝΔΡΑ ΝΤΟΝΤΟΥ)  
**Student ID:** 263 
**Institution:** University of Ioannina — Department of Informatics and Telecommunications  

*This repository is maintained for academic reference and educational purposes.*
