/**
 * Frontend security utilities for XSS prevention and input sanitization
 */

/**
 * Sanitize a string to prevent XSS attacks
 * @param {string} str - String to sanitize
 * @param {number} maxLength - Maximum allowed length
 * @returns {string} Sanitized string
 */
export function sanitizeString(str, maxLength = null) {
    if (typeof str !== 'string') {
        str = String(str);
    }
    
    // Remove null bytes
    str = str.replace(/\x00/g, '');
    
    // Trim whitespace
    str = str.trim();
    
    // Limit length
    if (maxLength && str.length > maxLength) {
        str = str.substring(0, maxLength);
    }
    
    // Escape HTML entities to prevent XSS
    const div = document.createElement('div');
    div.textContent = str;
    return div.innerHTML;
}

/**
 * Sanitize text content for display (allows line breaks)
 * @param {string} text - Text to sanitize
 * @param {number} maxLength - Maximum allowed length
 * @returns {string} Sanitized text
 */
export function sanitizeText(text, maxLength = 10000) {
    if (!text) return '';
    
    let sanitized = sanitizeString(text, maxLength);
    
    // Preserve line breaks
    sanitized = sanitized.replace(/\n/g, '<br>');
    
    return sanitized;
}

/**
 * Validate email address
 * @param {string} email - Email to validate
 * @returns {boolean} True if valid
 */
export function validateEmail(email) {
    if (!email) return false;
    
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email.trim().toLowerCase());
}

/**
 * Validate phone number
 * @param {string} phone - Phone number to validate
 * @returns {boolean} True if valid
 */
export function validatePhone(phone) {
    if (!phone) return true; // Phone is optional
    
    // Remove non-digit characters except +
    const digitsOnly = phone.replace(/[^\d+]/g, '');
    const digits = digitsOnly.replace(/[^\d]/g, '');
    
    // Should be between 10-15 digits
    return digits.length >= 10 && digits.length <= 15;
}

/**
 * Sanitize URL to prevent XSS
 * @param {string} url - URL to sanitize
 * @returns {string} Sanitized URL or empty string
 */
export function sanitizeUrl(url) {
    if (!url) return '';
    
    // Only allow http, https, or relative URLs
    if (!url.match(/^(https?:\/\/|\/)/)) {
        return '';
    }
    
    // Escape special characters
    return encodeURI(url);
}

/**
 * Sanitize form data object
 * @param {Object} data - Form data to sanitize
 * @param {Object} schema - Schema defining field types and max lengths
 * @returns {Object} Sanitized form data
 */
export function sanitizeFormData(data, schema = {}) {
    const sanitized = {};
    
    for (const [key, value] of Object.entries(data)) {
        const fieldSchema = schema[key] || {};
        const maxLength = fieldSchema.maxLength || null;
        const type = fieldSchema.type || 'string';
        
        if (type === 'email') {
            sanitized[key] = value ? value.trim().toLowerCase() : '';
        } else if (type === 'text') {
            sanitized[key] = sanitizeText(value, maxLength);
        } else if (type === 'number') {
            sanitized[key] = isNaN(value) ? 0 : Number(value);
        } else {
            sanitized[key] = sanitizeString(value, maxLength);
        }
    }
    
    return sanitized;
}

/**
 * Get CSRF token from cookies
 * @returns {string|null} CSRF token or null
 */
export function getCsrfToken() {
    const name = 'csrftoken';
    const cookies = document.cookie.split(';');
    
    for (let cookie of cookies) {
        const [key, value] = cookie.trim().split('=');
        if (key === name) {
            return decodeURIComponent(value);
        }
    }
    
    return null;
}

/**
 * Set CSRF token in request headers
 * @param {Object} headers - Request headers object
 * @returns {Object} Headers with CSRF token
 */
export function addCsrfToken(headers = {}) {
    const token = getCsrfToken();
    if (token) {
        headers['X-CSRFToken'] = token;
    }
    return headers;
}
