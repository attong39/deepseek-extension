JSC-PD wrapper usage and diagnostics
===================================

Tóm tắt nhanh
-------------

- `scripts/check_duplicates.py` là wrapper gọi `jscpd` (qua `npx` hoặc local binary) và lưu logs/summary vào `reports/duplicates`.

- Script giờ ghi header chi tiết cho cả Initial run và Retry run trong `jscpd-run.log` (timestamp, RC, STDOUT, STDERR).

Các file/đường dẫn quan trọng
----------------------------

- Log file: `reports/duplicates/jscpd-run.log`

- Output folder (reports): `reports/duplicates/jscpd`

- JSON summary (if produced): `reports/duplicates/jscpd_summary.json`

Đọc log nhanh
--------------

1. Mở file log:

- PowerShell: `Get-Content .\reports\duplicates\jscpd-run.log -Raw`

2. Log có hai header chính (nếu retry xảy ra):

- `INITIAL RUN AT <timestamp>`: thông tin rc/stdout/stderr của lần chạy ban đầu.

- `RETRY RUN AT <timestamp>`: thông tin rc/stdout/stderr của lần retry với thresholds thấp hơn.

3. Nếu không thấy file JSON trong `reports/duplicates/jscpd`, xem phần `--- STDERR ---` để biết lỗi reporter hoặc phụ thuộc bị thiếu.

Chạy wrapper (PowerShell)
-------------------------

```powershell
.\.venv\Scripts\python.exe .\scripts\check_duplicates.py --jscpd-only --report-dir .\reports\duplicates
```

Chạy jscpd thủ công (nếu cần debug reporter)
---------------------------------------------

1. Copy command được in bởi wrapper (dòng bắt đầu `Running:`) và chạy trực tiếp trong PowerShell.

2. Nếu jscpd báo thiếu reporter package, cài reporter JSON ví dụ:

- `npm i -g @jscpd/json`

- hoặc cài `jscpd` local: `npm i -D jscpd`

Tùy chọn test nhanh
---------------------

- Chạy 3 unit tests nhỏ thêm về jscpd wrapper:

```powershell
.\.venv\Scripts\python.exe -m pytest -q zeta_vn/tests/test_check_duplicates.py
```

Kontrol biến môi trường cho test nặng
------------------------------------

- Để skip các test nặng (mặc định), không cần thiết làm gì. Nếu muốn chạy toàn bộ test bao gồm `smoke`, `integration`, v.v., set:

  - Windows PowerShell:

   ```powershell
   $env:RUN_HEAVY_TESTS = '1'
   ```

  - Sau đó chạy `pytest` bình thường.

Ghi chú
------

- Tài liệu này chỉ là hướng dẫn nhanh; nếu bạn muốn mình tạo một script tiện lợi (ví dụ `scripts/show_jscpd_report.ps1`) để mở log và liệt kê output, mình có thể tạo thêm.
