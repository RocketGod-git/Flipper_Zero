#pragma once

PVOID __stdcall prx_find_function(WORD ordinal, PVOID *fn);
BOOLEAN __stdcall prx_attach(HINSTANCE instance);
void __stdcall prx_detach(PVOID);
