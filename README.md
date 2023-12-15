# Graph Drawing Algorithms Implementation

## Overview

This project implements three popular graph drawing algorithms: Fruchterman Reingold, Force Atlas 2, and Kamada Kawai. Graph drawing algorithms aim to visualize graphs in a clear and aesthetically pleasing way.

## Implemented Algorithms

### 1. Fruchterman Reingold

The Fruchterman Reingold algorithm is a force-directed layout algorithm that simulates a physical system where nodes repel each other and edges act like springs. This leads to a visually balanced representation of the graph.

### 2. Force Atlas 2

Force Atlas 2 is another force-directed layout algorithm designed for large-scale graphs. It balances attractive and repulsive forces to achieve a layout that highlights community structures and connectivity.

### 3. Kamada Kawai

The Kamada Kawai algorithm is based on a graph-theoretic approach that minimizes the energy of the graph. It aims to position nodes in a way that minimizes the total edge length, providing a compact and visually appealing representation.

## Getting Started

### Prerequisites

- Python 3.9

### Installation

1. Clone the repository:

   ```bash
   git clone <repository-url>
   cd <repository-directory>

2. Set up virtual environment:

   ```bash
   python -m venv venv
   source venv/bin/activate   

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
