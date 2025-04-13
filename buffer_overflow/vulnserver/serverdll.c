/**
 * The DLL should be linked to the jumpesp.obj to force a "JUMP ESP" fixed-memory 
 * gadget on the server.exe to emulate a buffer overflow context.
 * ASLR must be set to disabled.
 */

#include <windows.h>

extern void WINAPI _jmp_esp_gadget();

__declspec(dllexport) void WINAPI payload() {
    OutputDebugStringA("Server DLL here ;)\n");
}