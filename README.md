# cf_scan_443

# Termux 
  # Installation 
  ```
  pkg update && pkg install openssl wget python3 git -y && pip3 install waiting ipaddress alive-progress bs4 requests && wget -N https://raw.githubusercontent.com/SuspectWorkers/cf_scan_443/main/scan.py && wget -N https://raw.githubusercontent.com/SuspectWorkers/cf_scan_443/main/config.py && wget -N https://raw.githubusercontent.com/SuspectWorkers/cf_scan_443/main/fastly_ranges.txt && python3 scan.py
  ```

  # Start
  ```
  python3 scan.py
  ```

  # Output Result :
  Results saved to file (cflare_output.txt; cfront_output...)
