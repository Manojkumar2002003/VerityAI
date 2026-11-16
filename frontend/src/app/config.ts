/**
 * VerityAI Frontend Configuration Module.
 *
 * Centralizes and validates client-side environment settings. All frontend
 * variables use Vite's `VITE_` prefix and are publicly accessible in the browser.
 * Never place private keys, passwords, or server-side secrets here.
 */

export interface AppConfig {
  /** Base URL for the VerityAI FastAPI backend service. */
  apiBaseUrl: string;
}

export const DEFAULT_API_BASE_URL = 'http://localhost:8000';

/**
 * Validates and normalizes an API base URL string.
 *
 * @param urlStr - Raw URL string from environment variables.
 * @returns Normalized URL string without trailing slash.
 * @throws Error if the string is present but is not a valid http(s) URL.
 */
export function validateApiBaseUrl(urlStr: string | undefined): string {
  if (!urlStr || typeof urlStr !== 'string' || !urlStr.trim()) {
    return DEFAULT_API_BASE_URL;
  }

  const trimmed = urlStr.trim();

  try {
    const parsed = new URL(trimmed);
    if (parsed.protocol !== 'http:' && parsed.protocol !== 'https:') {
      throw new Error(
        `Invalid protocol '${parsed.protocol}'. API base URL must use http or https.`
      );
    }
  } catch (err) {
    if (err instanceof TypeError) {
      throw new Error(
        `Malformed VITE_API_BASE_URL: '${trimmed}' is not a valid absolute URL.`
      );
    }
    throw err;
  }

  // Strip trailing slash for consistent route composition
  return trimmed.endsWith('/') ? trimmed.slice(0, -1) : trimmed;
}

/**
 * Loads and validates frontend configuration from an environment dictionary.
 *
 * @param env - Environment variables dictionary (defaults to import.meta.env).
 * @returns Validated AppConfig object.
 */
export function getAppConfig(
  env: Record<string, string | undefined> = import.meta.env
): AppConfig {
  return {
    apiBaseUrl: validateApiBaseUrl(env.VITE_API_BASE_URL),
  };
}

export const appConfig = getAppConfig();
