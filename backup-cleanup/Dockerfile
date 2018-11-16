FROM python:3-slim
ADD requierments.txt .
RUN pip install -r requierments.txt
ADD delete.py .
CMD ["/usr/bin/env", "python3", "-u", "delete.py"]
