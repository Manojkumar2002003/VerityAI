import { describe, expect, it } from 'vitest';
import { DEFAULT_API_BASE_URL, getAppConfig, validateApiBaseUrl } from './config';

describe('Frontend Configuration Module', () => {
  describe('validateApiBaseUrl', () => {
    it('returns default URL when input is undefined or empty', () => {
      expect(validateApiBaseUrl(undefined)).toBe(DEFAULT_API_BASE_URL);
      expect(validateApiBaseUrl('')).toBe(DEFAULT_API_BASE_URL);
      expect(validateApiBaseUrl('   ')).toBe(DEFAULT_API_BASE_URL);
    });

    it('accepts valid HTTP and HTTPS URLs and strips trailing slashes', () => {
      expect(validateApiBaseUrl('http://localhost:8000')).toBe('http://localhost:8000');
      expect(validateApiBaseUrl('http://localhost:8000/')).toBe('http://localhost:8000');
      expect(validateApiBaseUrl('https://api.verity.ai/')).toBe('https://api.verity.ai');
      expect(validateApiBaseUrl('https://api.verity.ai:8443')).toBe(
        'https://api.verity.ai:8443'
      );
    });

    it('throws descriptive error on malformed URL string', () => {
      expect(() => validateApiBaseUrl('invalid-url-string')).toThrowError(
        /Malformed VITE_API_BASE_URL/i
      );
    });

    it('throws descriptive error on unsupported protocol', () => {
      expect(() => validateApiBaseUrl('ftp://example.com/api')).toThrowError(
        /Invalid protocol 'ftp:'/i
      );
    });
  });

  describe('getAppConfig', () => {
    it('extracts and validates configuration from environment dictionary', () => {
      const config = getAppConfig({
        VITE_API_BASE_URL: 'https://custom.backend.dev',
      });
      expect(config.apiBaseUrl).toBe('https://custom.backend.dev');
    });

    it('falls back to default if environment variable is omitted', () => {
      const config = getAppConfig({});
      expect(config.apiBaseUrl).toBe(DEFAULT_API_BASE_URL);
    });
  });
});
