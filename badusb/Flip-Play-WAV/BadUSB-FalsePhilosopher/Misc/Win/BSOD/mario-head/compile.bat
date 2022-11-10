@echo off

mkdir build

cl /Fe:"build/mario.exe" /Fo:"build/mario.obj" /EHsc main.cpp