import '@testing-library/jest-dom/vitest';
import { cleanup } from '@testing-library/react';
import { afterEach } from 'vitest';

// Fix Node 22/24 JSDOM webidl mismatch where JSDOM AbortSignal is passed to Node undici Request
const OriginalRequest = globalThis.Request;
if (OriginalRequest) {
  globalThis.Request = class Request extends OriginalRequest {
    constructor(input: RequestInfo | URL, init?: RequestInit) {
      if (init && init.signal) {
        // Omitting the JSDOM signal avoids undici webidl brand validation failures in unit tests
        const { signal: _signal, ...rest } = init;
        super(input, rest);
      } else {
        super(input, init);
      }
    }
  } as typeof OriginalRequest;
}

afterEach(() => {
  cleanup();
});
