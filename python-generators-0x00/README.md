# Python Generators

This project demonstrates efficient data streaming from a MySQL database using Python generators. It includes:

- Row-by-row streaming with minimal memory usage
- Batch pagination with lazy loading
- Real-time processing of user ages to compute the average without loading the full dataset
- No use of SQL `AVG()` function — all calculations happen in Python

---

## Features

- **`stream_users()`** — Streams all user records one by one
- **`stream_users_in_batches(batch_size)`** — Streams users in customizable batch sizes
- **`batch_processing(batch_size)`** — Processes each batch, filtering users over age 25
- **`paginate_users(page_size, offset)`** — Fetches a page of users with limit/offset
- **`lazy_paginate(page_size)`** — Lazily paginates users, fetching the next page only when needed
- **`stream_user_ages()`** — Yields user ages one by one
- **`calculate_average_age()`** — Calculates and prints the average user age without loading full data

---

## Requirements

- Python 3.x
- MySQL Server
- `mysql-connector-python` package
- Ensure `user_data.csv` is available in the project directory.

**Install dependencies:**

```bash
pip install mysql-connector-python
```
