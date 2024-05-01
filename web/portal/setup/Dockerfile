# Start with the official Python image
FROM python:3.9-slim

ENV FLAG=CCSC{s1d3_t0_s1d3_4ND_fr0n7_tO_b4ck}

# Install Python dependencies
WORKDIR /app
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy the app
COPY flag.txt /app
COPY app.py /app
COPY app-dev-version-abccdef.py /app

EXPOSE 3000

# Command to start services
CMD python3 app-dev-version-abccdef.py & python3 app.py