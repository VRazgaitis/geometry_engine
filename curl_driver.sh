#!/bin/bash
curl -X POST http://127.0.0.1:5000/check_convex -H "Content-Type: application/json" -d '{"mesh": [[0, 0, 1],[2, 0, 2],[2, 1, 1],[1, 1, 3],[1, 2, 1],[2, 2, 3],[2, 3, 1],[0, 3, 3],[0, 0, 1]]}'
