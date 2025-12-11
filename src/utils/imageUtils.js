/**
 * Utility function to normalize image URLs to work with current host (domain or IP)
 * This ensures images display correctly whether accessed via domain name or IP address
 * 
 * @param {string} imageUrl - The image URL from the backend (can be absolute or relative)
 * @returns {string} - Normalized URL that works with current host
 */
export const normalizeImageUrl = (imageUrl) => {
  if (!imageUrl) return null;
  
  // If it's already a data URL or blob URL, return as is
  if (imageUrl.startsWith('data:') || imageUrl.startsWith('blob:')) {
    return imageUrl;
  }
  
  try {
    // If it's a relative URL (starts with /), make it absolute using current origin
    if (imageUrl.startsWith('/')) {
      return `${window.location.origin}${imageUrl}`;
    }
    
    // If it's an absolute URL, replace the origin with current origin
    const url = new URL(imageUrl, window.location.href);
    // Replace the origin (protocol + host + port) with current window's origin
    return `${window.location.origin}${url.pathname}${url.search}${url.hash}`;
  } catch (error) {
    // If URL parsing fails, try to extract path and use current origin
    console.warn('Failed to parse image URL:', imageUrl, error);
    // If it looks like a path, prepend current origin
    if (imageUrl.startsWith('/')) {
      return `${window.location.origin}${imageUrl}`;
    }
    // Otherwise return as is (might be a relative path without leading slash)
    return imageUrl;
  }
};

