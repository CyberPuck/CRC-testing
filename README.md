# CRC Testing
This repo contains a Python script for testing CRC-7 and CRC-16.  The polynomials in both functions are hardcoded.
Both functions expect an array of "bytes" (8-bit) numbers to calcuate the CRC.

## Purpose
I’m currently implementing a SPI protocol on an Arduino.  The slave device expcets a CRC (7 or 16 depending on the message type) and this Python script is a good model for implementing in C.

## NOTICE
There is a large number of articles online discussing CRC and the techniques that can be deployed.  I'm not smart enough to generate a table,
so I went with the brute force method.  If CRC is needed in production use a different technique or even better, implement in hardware.
