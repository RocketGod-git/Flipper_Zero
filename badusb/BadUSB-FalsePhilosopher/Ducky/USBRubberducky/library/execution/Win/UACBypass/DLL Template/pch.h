#ifndef PCH_H
#define PCH_H

#include "targetver.h"

#define WIN32_LEAN_AND_MEAN
// Windows Header Files:
#include <windows.h>
#include <tchar.h>
#include <strsafe.h>

// standard library headers
#include <stdlib.h>

// reference additional headers your program requires here


#define OffsetToPointer(Base, Offset) ((PVOID)(((PBYTE)(Base)) + ((UINT_PTR)(Offset))))
#define PointerToOffset(Base, Pointer) ((INT_PTR)(((PBYTE)(Pointer)) - ((PBYTE)(Base))))

#endif
