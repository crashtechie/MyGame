# Issue 0000001: Pygame reports a failed module during startup

**Status:** Resolved (2026-10-06)  
**Priority:** Urgent  
**First observed:** 2026-10-06 at 17:00 (CDT)

## Resolution

**Root cause:** `pygame.get_error()` reported `dsp: No such audio device`. The environment has no audio device, so the mixer module failed to initialize, which accounted for the 1 failed module. Display initialization was not affected.

**Fix:** `main.py` now sets `SDL_AUDIODRIVER` to `dummy` (via `os.environ.setdefault`) before importing pygame. SDL then uses a silent audio driver when no sound device exists, and the mixer initializes normally. A value already set in the environment takes precedence. `main.py` also captures `pygame.get_error()` after `pygame.init()` and prints it when initialization fails.

**Verification:** After the change, all 5 modules initialize successfully with 0 failures.

**Note:** The dummy driver produces no sound. When real audio output is needed, remove the override or set `SDL_AUDIODRIVER` to a real driver.

## Summary

Starting the game prints a Pygame initialization failure: four modules initialize successfully and one fails. The game continues running after the message, but the report does not identify the failed module or confirm whether the game window appears. The process was stopped manually with Ctrl+C.

## Environment

- Python 3.12.13
- Pygame 2.6.1
- SDL 2.28.4
- Operating system and display/audio environment: not recorded

## Steps to reproduce

1. From the project directory, run `uv run main.py`.

## Actual result

The startup output includes:

```text
pygame 2.6.1 (SDL 2.28.4, Python 3.12.13)
Hello from the pygame community. https://www.pygame.org/contribute.html
Pygame failed to initialize properly. 4 successful and 1 failed modules.
```

The program then remains in the event loop until interrupted. Ctrl+C produces a `KeyboardInterrupt` at `pygame.event.get()` in `main.py`. This indicates the process was still running; it does not by itself establish that the window or game failed to start.

## Expected result

The game initializes the subsystems it requires, opens an 800 × 600 window, and runs its event loop. If an optional subsystem cannot initialize, the game should report which one failed and continue only when doing so is safe.

## Recommendations

1. **Identify the failed subsystem before changing startup behavior.** Capture `pygame.get_error()` immediately after initialization, and log the initialization state of the subsystems the game uses (in particular, display and mixer). The current success/failure counts do not name the failed module.
2. **Check required subsystems explicitly.** Treat display initialization as required for this windowed game and report a clear startup error if it is unavailable. Do not treat a failure in an optional subsystem as proof that all of Pygame failed.
3. **Investigate the runtime environment based on the diagnostic.** If display initialization failed, record the operating system, whether a graphical session is available, and relevant SDL video-driver settings. If the failed subsystem is audio and audio is not currently needed, keep it optional rather than blocking window startup.
4. **Retest from the same environment** with `uv run main.py`; confirm the window opens, remains responsive, and closes cleanly.

## Acceptance criteria

- Startup diagnostics identify the failing subsystem and include the underlying Pygame/SDL error when initialization fails.
- A failure of a required subsystem is reported clearly and stops startup cleanly.
- A failure of an optional subsystem does not prevent the window and event loop from starting.
- Successful startup opens the window and exits cleanly when it is closed.
