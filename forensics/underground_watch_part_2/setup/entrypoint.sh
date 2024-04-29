#!/bin/bash

# Open dummy TCP listener to simulate tunnel destination
socat TCP-LISTEN:12345,reuseaddr,fork,bind=127.0.0.1 /dev/null &

apache2-foreground
