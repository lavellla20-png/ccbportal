import React, { useState, useEffect } from 'react';
import Navbar from './components/Navbar';
import ScrollToTop from './components/ScrollToTop';
import Footer from './components/footer';
import apiService from './services/api';
import './downloads.css';

const Downloads = () => {
  const [isPoliciesVisible, setIsPoliciesVisible] = useState(false);
  const [isFormsVisible, setIsFormsVisible] = useState(false);
  const [downloads, setDownloads] = useState({});
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // Category mapping for display
  const categoryConfig = {
    'forms-enrollment': {
      title: 'Enrollment',
      description: 'These relate to student registration and academic load:',
      icon: 'M14 2H6a2 2 0 00-2 2v16a2 2 0 002 2h12a2 2 0 002-2V8l-6-6z M14 2v6h6 M16 13H8 M16 17H8 M10 9H8'
    },
    'forms-clearance': {
      title: 'Clearance',
      description: 'These are likely used for approvals or exits:',
      icon: 'M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z'
    },
    'forms-request': {
      title: 'Request',
      description: 'These involve formal requests or documentation:',
      icon: 'M19 3H5c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2V5c0-1.1-.9-2-2-2zm-5 14H7v-2h7v2zm3-4H7v-2h10v2zm0-4H7V7h10v2z'
    },
    'forms-shift-change': {
      title: 'Shift / Change',
      description: 'Used for schedule or program adjustments:',
      icon: 'M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z'
    },
    'hr-policies': {
      title: 'HR Policies',
      description: 'Access important HR policies and guidelines',
      icon: 'M14 2H6a2 2 0 00-2 2v16a2 2 0 002 2h12a2 2 0 002-2V8l-6-6z M14 2v6h6 M16 13H8 M16 17H8 M10 9H8'
    },
    'hr-forms': {
      title: 'HR Forms',
      description: 'Downloadable forms for faculty and staff',
      icon: 'M14 2H6a2 2 0 00-2 2v16a2 2 0 002 2h12a2 2 0 002-2V8l-6-6z M14 2v6h6 M16 13H8 M16 17H8 M10 9H8'
    },
    'syllabi': {
      title: 'Syllabi',
      description: 'Course syllabi and academic resources',
      icon: 'M14 2H6a2 2 0 00-2 2v16a2 2 0 002 2h12a2 2 0 002-2V8l-6-6z M14 2v6h6 M16 13H8 M16 17H8 M10 9H8'
    },
    'manuals': {
      title: 'Manuals',
      description: 'Academic and administrative manuals',
      icon: 'M14 2H6a2 2 0 00-2 2v16a2 2 0 002 2h12a2 2 0 002-2V8l-6-6z M14 2v6h6 M16 13H8 M16 17H8 M10 9H8'
    },
    'handbooks': {
      title: 'Handbooks',
      description: 'Student and employee handbooks',
      icon: 'M14 2H6a2 2 0 00-2 2v16a2 2 0 002 2h12a2 2 0 002-2V8l-6-6z M14 2v6h6 M16 13H8 M16 17H8 M10 9H8'
    },
    'other': {
      title: 'Other Downloads',
      description: 'Additional downloadable resources',
      icon: 'M14 2H6a2 2 0 00-2 2v16a2 2 0 002 2h12a2 2 0 002-2V8l-6-6z M14 2v6h6 M16 13H8 M16 17H8 M10 9H8'
    }
  };

  // Fetch downloads on component mount
  useEffect(() => {
    const fetchDownloads = async () => {
      try {
        setLoading(true);
        const response = await apiService.getDownloads();
        if (response.status === 'success') {
          setDownloads(response.downloads || {});
        } else {
          setError('Failed to load downloads');
        }
      } catch (err) {
        console.error('Error fetching downloads:', err);
        setError('Failed to load downloads. Please try again later.');
      } finally {
        setLoading(false);
      }
    };

    fetchDownloads();
  }, []);

  const handleDownload = (fileUrl, title) => {
    if (fileUrl) {
      // Open download in new tab
      window.open(fileUrl, '_blank');
    }
  };

  // Intersection Observer for policies section
  useEffect(() => {
    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            setIsPoliciesVisible(true);
          }
        });
      },
      {
        threshold: 0.1, // Trigger when 10% of the element is visible
        rootMargin: '0px 0px -50px 0px' // Start animation 50px before element comes into view
      }
    );

    const policiesElement = document.querySelector('.policies-grid');
    if (policiesElement) {
      observer.observe(policiesElement);
    }

    return () => {
      if (policiesElement) {
        observer.unobserve(policiesElement);
      }
    };
  }, []);

  // Intersection Observer for forms section
  useEffect(() => {
    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            setIsFormsVisible(true);
          }
        });
      },
      {
        threshold: 0.1, // Trigger when 10% of the element is visible
        rootMargin: '0px 0px -50px 0px' // Start animation 50px before element comes into view
      }
    );

    const formsElement = document.querySelector('.forms-grid');
    if (formsElement) {
      observer.observe(formsElement);
    }

    return () => {
      if (formsElement) {
        observer.unobserve(formsElement);
      }
    };
  }, []);

  return (
    <div className="App downloads-page">
      <Navbar />

      {/* Downloads Hero Section */}
      <section className="news-hero">
        <div className="container">
          <div className="hero-content">
            <h1 className="hero-title">Downloads</h1>
            <p className="hero-subtitle">Find all the recent downloads and resources at City College of Bayawan</p>
            <p className="hero-motto">Explore our updated files, helpful guides, and important downloads</p>
          </div>
        </div>
      </section>

      {/* Forms Section */}
      <section id="forms" className="section forms-section">
        <div className="container">
          <h2 className="section-title">Forms</h2>
          <p className="section-subtitle">Download essential forms for enrollment, clearance, leave, and other academic processes</p>
          
          {loading ? (
            <div style={{ textAlign: 'center', padding: '40px' }}>
              <p>Loading downloads...</p>
            </div>
          ) : error ? (
            <div style={{ textAlign: 'center', padding: '40px', color: '#d32f2f' }}>
              <p>{error}</p>
            </div>
          ) : (
            <div className="downloads-grid">
              {Object.entries(downloads).map(([category, items]) => {
                // Only show form categories in the Forms section
                if (!category.startsWith('forms-')) return null;
                
                const config = categoryConfig[category] || categoryConfig['other'];
                return (
                  <div key={category} className="download-category">
                    <div className="category-icon">
                      <svg viewBox="0 0 24 24" width="48" height="48" fill="currentColor">
                        <path d={config.icon}/>
                      </svg>
                    </div>
                    <h3>{config.title}</h3>
                    <p className="category-description">{config.description}</p>
                    <div className="download-links">
                      {items.map((item) => (
                        <button
                          key={item.id}
                          className="download-link"
                          onClick={() => handleDownload(item.file_url, item.title)}
                        >
                          <svg viewBox="0 0 24 24" width="20" height="20" fill="currentColor">
                            <path d="M5 20h14v-2H5v2zM12 2v12l4-4h-3V2h-2v8H8l4 4z"/>
                          </svg>
                          <div className="download-link-content">
                            <strong>{item.title}</strong>
                            {item.description && <span style={{ display: 'block', fontSize: '0.85em', color: '#666', marginTop: '4px' }}>{item.description}</span>}
                          </div>
                        </button>
                      ))}
                    </div>
                  </div>
                );
              })}
              {Object.keys(downloads).filter(cat => cat.startsWith('forms-')).length === 0 && (
                <div style={{ textAlign: 'center', padding: '40px', gridColumn: '1 / -1' }}>
                  <p>No forms available at this time.</p>
                </div>
              )}
            </div>
          )}
        </div>
      </section>

      {/* HR Policies and Downloadable Forms Section (moved from Faculty & Staff) */}
      <section className="faculty-staff-section hr-section">
        <div className="container">
          <h2 className="section-title">HR Policies and Downloadable Forms</h2>
          <p className="section-subtitle">Access important HR documents, policies, and forms for faculty and staff</p>
          
          {!loading && !error && (
            <div className="hr-content">
              {/* HR Policies */}
              {downloads['hr-policies'] && downloads['hr-policies'].length > 0 && (
                <div className={`policies-grid ${isPoliciesVisible ? 'fade-in-visible' : ''}`}>
                  {downloads['hr-policies'].map((item) => (
                    <div key={item.id} className="policy-card">
                      <div className="policy-icon">
                        <svg viewBox="0 0 24 24" width="48" height="48" fill="currentColor">
                          <path d="M14 2H6a2 2 0 00-2 2v16a2 2 0 002 2h12a2 2 0 002-2V8l-6-6z"/>
                          <path d="M14 2v6h6"/>
                          <path d="M16 13H8"/>
                          <path d="M16 17H8"/>
                          <path d="M10 9H8"/>
                        </svg>
                      </div>
                      <h3>{item.title}</h3>
                      <p>{item.description || 'HR policy document'}</p>
                      <button 
                        className="download-btn"
                        onClick={() => handleDownload(item.file_url, item.title)}
                      >
                        Download {item.file_type || 'PDF'}
                      </button>
                    </div>
                  ))}
                </div>
              )}
              
              {/* HR Forms */}
              {downloads['hr-forms'] && downloads['hr-forms'].length > 0 && (
                <div className="forms-section">
                  <h3>Downloadable Forms</h3>
                  <div className={`forms-grid ${isFormsVisible ? 'fade-in-visible' : ''}`}>
                    {downloads['hr-forms'].map((item) => (
                      <div key={item.id} className="form-card">
                        <h4>{item.title}</h4>
                        <p>{item.description || 'HR form document'}</p>
                        <button 
                          className="form-btn"
                          onClick={() => handleDownload(item.file_url, item.title)}
                        >
                          Download Form
                        </button>
                      </div>
                    ))}
                  </div>
                </div>
              )}
              
              {(!downloads['hr-policies'] || downloads['hr-policies'].length === 0) && 
               (!downloads['hr-forms'] || downloads['hr-forms'].length === 0) && (
                <div style={{ textAlign: 'center', padding: '40px' }}>
                  <p>No HR documents available at this time.</p>
                </div>
              )}
            </div>
          )}
        </div>
      </section>

      {/* Syllabi, Manuals, and Handbooks Section */}
      <section id="documents" className="section documents-section">
        <div className="container">
          <h2 className="section-title">Syllabi, Manuals, and Handbooks</h2>
          <p className="section-subtitle">Access comprehensive academic resources, guidelines, and reference materials</p>
          
          {!loading && !error && (
            <div className="downloads-grid">
              {['syllabi', 'manuals', 'handbooks', 'other'].map((category) => {
                if (!downloads[category] || downloads[category].length === 0) return null;
                
                const config = categoryConfig[category] || categoryConfig['other'];
                return (
                  <div key={category} className="download-category">
                    <div className="category-icon">
                      <svg viewBox="0 0 24 24" width="48" height="48" fill="currentColor">
                        <path d={config.icon}/>
                      </svg>
                    </div>
                    <h3>{config.title}</h3>
                    <p className="category-description">{config.description}</p>
                    <div className="download-links">
                      {downloads[category].map((item) => (
                        <button
                          key={item.id}
                          className="download-link"
                          onClick={() => handleDownload(item.file_url, item.title)}
                        >
                          <svg viewBox="0 0 24 24" width="20" height="20" fill="currentColor">
                            <path d="M5 20h14v-2H5v2zM12 2v12l4-4h-3V2h-2v8H8l4 4z"/>
                          </svg>
                          <div className="download-link-content">
                            <strong>{item.title}</strong>
                            {item.description && <span style={{ display: 'block', fontSize: '0.85em', color: '#666', marginTop: '4px' }}>{item.description}</span>}
                          </div>
                        </button>
                      ))}
                    </div>
                  </div>
                );
              })}
              {['syllabi', 'manuals', 'handbooks', 'other'].every(cat => !downloads[cat] || downloads[cat].length === 0) && (
                <div style={{ textAlign: 'center', padding: '40px', gridColumn: '1 / -1' }}>
                  <p>No documents available at this time.</p>
                </div>
              )}
            </div>
          )}
        </div>
      </section>

      <Footer />

      {/* Scroll to Top Button */}
      <ScrollToTop />
    </div>
  );
};

export default Downloads;